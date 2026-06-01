import numpy as np
import cv2
import os
import concurrent.futures

# --- Configuration & Model Setup ---
size = globals().get('size', 32)

# Detect whether the CNN and classifier models (and label encoder) are available
try:
    _ = cnn_model  # type: ignore
    _ = model  # type: ignore
    _ = continuing_model  # type: ignore
    _ = le  # type: ignore
    MODELS_AVAILABLE = True
except Exception:
    MODELS_AVAILABLE = False
    print("Note: AI model objects not found — falling back to color-only detection.")

# Configuration for N-Frame Rule
REQUIRED_CONSECUTIVE_FRAMES = 3

################################
#  IMAGE CLASSIFICATION LOGIC  #
################################

def detect_fire_by_color_frequency(image_bgr, threshold_ratio=0.0018):
    """Detects fire using STRICTER HSV color boundaries."""
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    
    lower_fire = np.array([0, 150, 150]) 
    upper_fire = np.array([30, 255, 255])
    mask1 = cv2.inRange(hsv, lower_fire, upper_fire)
    
    lower_red = np.array([160, 150, 150])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    
    combined_mask = cv2.bitwise_or(mask1, mask2)
    
    total_pixels = image_bgr.shape[0] * image_bgr.shape[1]
    fire_pixels = cv2.countNonZero(combined_mask)
    
    return (fire_pixels / total_pixels) > threshold_ratio

def analyze_frame_for_fire(user_img):
    """
    Analyzes an in-memory frame. Returns True if fire is detected.
    """
    # 1. Run Color Analysis
    is_fire_color = detect_fire_by_color_frequency(user_img)
    
    if not MODELS_AVAILABLE:
        return is_fire_color

    # 2. Process image for AI Models
    user_img_resized = cv2.resize(user_img, (size, size))
    user_img_rgb = cv2.cvtColor(user_img_resized, cv2.COLOR_BGR2RGB)
    user_img_norm = user_img_rgb.astype('float32') / 255.0

    # CNN prediction
    input_img = np.expand_dims(user_img_norm, axis=0)
    probs = cnn_model.predict(input_img, verbose=0)
    pred_cnn = np.argmax(probs, axis=-1)
    try:
        pred_cnn_label = le.inverse_transform(pred_cnn)[0]
    except Exception:
        pred_cnn_label = str(pred_cnn[0])

    # Classifier prediction
    features = model.predict(input_img, verbose=0)
    try:
        pred_cl = continuing_model.predict(features)
        pred_cl_label = le.inverse_transform(pred_cl)[0]
    except Exception:
        pred_cl_label = str(continuing_model.predict(features))

    is_fire_model = (
        str(pred_cnn_label).strip().lower() == 'fire' or
        str(pred_cl_label).strip().lower() == 'fire'
    )

    return bool(is_fire_model and is_fire_color)

################################
#  ASYNC VIDEO PROCESSING LOGIC #
################################

def process_video_for_fire(video_path, output_dir=None, max_workers=4):
    """
    Reads a video, processes frames asynchronously in memory, 
    and saves frames only if the consecutive frame rule triggers.
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file {video_path} not found.")
        return

    if output_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "fire_frames")

    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    
    consecutive_fire_count = 0
    warning_frames_buffer = []
    
    # We use a rolling queue to prevent RAM overload on large videos.
    # We will submit frames up to this limit before waiting on the oldest one.
    max_queue_size = max_workers * 3 
    futures_queue = []
    
    frame_idx = 0
    alarm_triggered = False

    print(f"Starting async analysis on '{video_path}'...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        
        while cap.isOpened() and not alarm_triggered:
            ret, frame = cap.read()
            
            # If we successfully read a frame, submit it to the pool
            if ret:
                # IMPORTANT: copy() prevents OpenCV from overwriting the memory buffer 
                # while the background thread is still processing it.
                frame_copy = frame.copy()
                future = executor.submit(analyze_frame_for_fire, frame_copy)
                futures_queue.append((frame_idx, frame_copy, future))
                frame_idx += 1
            
            # Process the oldest frame if our queue is full, OR if the video is finished (not ret)
            while len(futures_queue) >= max_queue_size or (not ret and len(futures_queue) > 0):
                # Pop the oldest chronological task
                oldest_idx, oldest_frame, oldest_future = futures_queue.pop(0)
                
                try:
                    # .result() will wait for this specific frame if it's not done yet
                    is_fire_present = oldest_future.result()
                    print(f"Analyzing frame_{oldest_idx}... ", end="")
                    
                    if is_fire_present:
                        consecutive_fire_count += 1
                        warning_frames_buffer.append((oldest_idx, oldest_frame))
                        print(f"WARNING! (Count: {consecutive_fire_count}/{REQUIRED_CONSECUTIVE_FRAMES})")
                        
                        if consecutive_fire_count >= REQUIRED_CONSECUTIVE_FRAMES:
                            print(f"\n🔥 ALARM TRIGGERED! Fire verified across {REQUIRED_CONSECUTIVE_FRAMES} frames.")
                            print("Saving confirmed fire frames to disk...")
                            
                            for buf_idx, buf_frame in warning_frames_buffer:
                                save_path = os.path.join(output_dir, f"CONFIRMED_FIRE_frame_{buf_idx}.jpg")
                                cv2.imwrite(save_path, buf_frame)
                            
                            alarm_triggered = True
                            
                            # Cancel pending tasks in the background
                            for _, _, p_future in futures_queue:
                                p_future.cancel()
                                
                            break # Break the validation loop
                            
                    else:
                        if consecutive_fire_count > 0:
                            print(f"Clear. (Streak broken, count reset to 0)")
                        else:
                            print("Clear.")
                        
                        consecutive_fire_count = 0
                        warning_frames_buffer.clear()
                        
                except Exception as e:
                    print(f"Error processing frame_{oldest_idx}: {e}")

            # If the video ended and we processed the remaining queue, exit loop
            if not ret:
                break
                
    cap.release()
    if not alarm_triggered:
        print("\nVideo analysis complete. No sustained fire detected.")

# ==========================================
# --- SCRIPT EXECUTION                   ---
# ==========================================
if __name__ == "__main__":
    # Specify your target video here:
    TARGET_VIDEO = r"C:\Users\akshar Patel\Downloads\firewatch-main_1_image_detect\firewatch-main\lift_fire.mp4" 
    
    # Run the combined pipeline
    process_video_for_fire(TARGET_VIDEO, max_workers=4)