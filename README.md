# Advanced Fire Detection System Using Computer Vision and Deep Learning

Complete open-source project with full source code. Combines CNN models, machine learning, and HSV color analysis for real-time flame identification in video streams and images.

---

## Keywords

Fire detection, fire detection project, fire detection with source code, computer vision fire detection, Python fire detection, OpenCV fire detection, TensorFlow fire detection, real-time detection, deep learning detection, CNN object detection, image classification, video analysis, machine learning project, open source

---

## Quick Links

- [Features](#features) | [Installation](#installation) | [Usage](#usage) | [Documentation](#documentation) | [Contributing](#contributing) | [License](#license)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation and Setup](#installation-and-setup)
- [Quick Start Guide](#quick-start-guide)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Detection Methods](#detection-methods)
- [Configuration](#configuration)
- [Video Processing](#video-processing)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Firewatch is an open-source fire detection system using artificial intelligence and computer vision. The system identifies fire hazards in video streams, images, and live camera feeds using real-time processing.

### Key Capabilities

- Real-time video analysis and frame-by-frame processing
- Multi-algorithm detection using hybrid color and AI methods
- CNN and machine learning classifier models with 95 percent accuracy
- Consecutive frame verification to reduce false alerts
- Batch processing for multiple video files
- Detailed reports and visualization of results

---

## Features

### Detection Methods

| Method | Description | Accuracy |
|--------|-------------|----------|
| Color-Based Detection | HSV color space analysis for fire spectrum identification | Fast and reliable |
| CNN Model | Convolutional Neural Network for visual pattern recognition | 92-95 percent |
| ML Classifier | Machine Learning classifier for fire detection classification | 90-94 percent |
| N-Frame Rule | Requires 3 consecutive frames to confirm fire detection | Eliminates false positives |

### Processing Capabilities

- Video input support for MP4, AVI, MOV file formats
- Frame rate control and adjustable processing speed
- Multi-threaded processing for concurrent frame analysis
- Real-time fire detection alerts with timestamps
- Complete analysis reports and logging

### Visualization and Output

- Frame-by-frame fire detection visualization
- Confidence score analysis
- Detection timeline visualization
- Frame exports with annotations
- Performance metrics reporting

## Technology Stack

### Core Technologies

- Programming Language: Python 3.8 and higher
- Computer Vision: OpenCV
- Deep Learning Framework: TensorFlow and Keras
- Machine Learning: scikit-learn
- Data Processing: NumPy and Pandas
- Visualization: Matplotlib and Seaborn

### Required Dependencies

| Package | Purpose |
|---------|---------|
| numpy | Numerical computing and data arrays |
| pandas | Data manipulation and analysis |
| opencv-python | Image and video processing |
| scikit-image | Image processing algorithms |
| scikit-learn | Machine learning algorithms |
| keras | Neural network development |
| tensorflow | Deep learning framework |
| seaborn | Statistical data visualization |
| matplotlib | Plotting and visualization |

---

## Installation and Setup

### Step 1: Check Python Installation

Verify you have Python 3.8 or higher installed.

```
python --version
pip --version
```

### Step 2: Clone the Repository

```
git clone https://github.com/your-org/firewatch.git
cd firewatch-main
```

### Step 3: Create Virtual Environment

Windows:
```
python -m venv myenv
myenv\Scripts\activate
```

macOS and Linux:
```
python -m venv myenv
source myenv/bin/activate
```

### Step 4: Install Dependencies

```
pip install -r requirements.txt
```

### Step 5: Verify Installation

```
python -c "import cv2, tensorflow, keras; print('Installation successful')"
```

---

## Quick Start Guide

### Single Image Analysis

```python
import cv2
from Code import analyze_frame_for_fire

image = cv2.imread('fire_sample.jpg')
is_fire_detected = analyze_frame_for_fire(image)
print(f"Fire Detected: {is_fire_detected}")
```

### Video File Processing

```python
import cv2
from Code import analyze_frame_for_fire

video_path = 'video.mp4'
cap = cv2.VideoCapture(video_path)

frame_count = 0
fire_frames = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    if analyze_frame_for_fire(frame):
        fire_frames.append(frame_count)
    
    frame_count += 1

cap.release()
print(f"Fire detected in {len(fire_frames)} frames")
```

### Real-Time Camera Detection

```python
import cv2
from Code import analyze_frame_for_fire

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if analyze_frame_for_fire(frame):
        print("FIRE ALERT")
        cv2.putText(frame, 'FIRE DETECTED', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.imshow('Fire Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Project Structure

```
firewatch-main/
|
|-- Code.py                    Main fire detection engine
|-- README.md                  Project documentation
|-- requirements.txt           Python dependencies
|-- code_run.txt              Execution logs
|
|-- fire_frames/              Sample detection frames
|-- plots/                    Visualization outputs
|-- myenv/                    Virtual environment
|-- lift_fire.mp4             Sample video for testing
|-- Presentation.pptx         Project presentation
```

---

## How It Works

### Fire Detection Pipeline

The system processes frames through multiple stages:

**Stage 1: Color-Based Detection**
- Convert image to HSV color space
- Analyze fire color spectrum
- Identify fire-colored pixels
- Fast initial filtering

**Stage 2: AI Model Analysis**
- Apply CNN feature extraction
- Run machine learning classifier
- Calculate confidence scores
- Verify detection patterns

**Stage 3: Frame Verification**
- Check 3 consecutive frames
- Eliminate false positives
- Confirm detection patterns
- Generate alert if confirmed

**Output: Fire Detected or Not Detected**

### Color Detection Algorithm

Fire detection uses HSV color space analysis:

- Orange and Yellow: Hue 0-30 degrees, Saturation 150-255, Value 150-255
- Red: Hue 160-180 degrees, Saturation 150-255, Value 150-255
- Pixel threshold: Greater than 0.18 percent of frame pixels

---

## Detection Methods

### Method 1: Convolutional Neural Network

Deep learning model for visual pattern recognition. Processes input through multiple layers:

- Convolution layers: Extract spatial features
- Pooling layers: Reduce dimensionality
- Dense layers: Classification
- Accuracy: 92-95 percent

### Method 2: Machine Learning Classifier

Binary classification model using scikit-learn:

- Feature preprocessing
- Model training on fire and non-fire data
- Binary prediction output
- Accuracy: 90-94 percent

### Method 3: Hybrid Color and AI Approach

Combined confidence scoring:

- Color Score: 40 percent weight
- CNN Score: 30 percent weight
- ML Classifier Score: 30 percent weight
- Threshold: 0.65 confidence for detection

---

## Configuration

### Adjustable Parameters

Located in Code.py:

```python
FIRE_COLOR_THRESHOLD = 0.0018
HSV_LOWER_FIRE = [0, 150, 150]
HSV_UPPER_FIRE = [30, 255, 255]
HSV_LOWER_RED = [160, 150, 150]
HSV_UPPER_RED = [180, 255, 255]
REQUIRED_CONSECUTIVE_FRAMES = 3
FRAME_SIZE = 32
BATCH_SIZE = 32
CONFIDENCE_THRESHOLD = 0.65
```

### Tuning Guide

Lower threshold value for increased sensitivity:
```
threshold_ratio = 0.001  (detects smaller fires)
```

Higher threshold value for reduced false positives:
```
threshold_ratio = 0.005  (fewer false alerts)
```

---

## Video Processing

### Batch Processing Multiple Videos

```python
import concurrent.futures
from Code import analyze_frame_for_fire

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fire_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if analyze_frame_for_fire(frame):
            fire_count += 1
    
    cap.release()
    return {'file': video_path, 'fire_frames': fire_count}

video_files = ['video1.mp4', 'video2.mp4', 'video3.mp4']

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_video, video_files))

for result in results:
    print(f"{result['file']}: {result['fire_frames']} frames")
```

---

## Documentation

### Main Guides

- Installation Guide: Complete setup instructions
- Usage Guide: How to use the fire detection system
- API Reference: Function documentation and parameters
- FAQ: Frequently asked questions and troubleshooting

---

## Contributing

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

### Contribution Areas

- Performance optimization
- Model improvements
- Documentation enhancement
- Bug fixes
- Feature requests
- Testing and quality assurance

---

## License

This project uses the MIT License. See the LICENSE file for complete details.

### MIT License Terms

- Commercial use permitted
- Modification allowed
- Distribution allowed
- Private use allowed
- Liability excluded
- Warranty excluded

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Detection Accuracy | 92-95 percent |
| False Positive Rate | Less than 5 percent |
| Processing Speed | 30-50 milliseconds per frame |
| Memory Usage | Approximately 500 megabytes |
| GPU Memory | Approximately 2 gigabytes |
| Maximum Frame Rate | 30 frames per second |

---

## Support and Contact

### Getting Help

- Documentation: Check included guides
- Issues: Open GitHub issues for bugs
- Community: Join project discussions
- Email: contact@firewatch-project.com

### External Resources

- OpenCV Documentation
- TensorFlow Guide
- Scikit-Learn Documentation
- Computer Vision Fundamentals

---

## Additional Information

### Educational Concepts

**Computer Vision:** Technology that enables machines to interpret and understand digital images and videos. Used for automated decision making and analysis.

**HSV Color Space:** Color model that separates color from intensity. More intuitive than RGB for color-based object detection and filtering.

**Convolutional Neural Networks:** Deep learning architecture that automatically learns hierarchical feature representations from raw image data.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | January 2024 | Initial release with color and CNN detection |
| 1.1.0 | February 2024 | Added ML classifier and N-Frame verification |
| 1.2.0 | March 2024 | Performance optimization and batch processing |

---

Made with care for fire safety and prevention.

For questions or suggestions, please open an issue on GitHub.

[Back to Top](#firewatch---ai-powered-real-time-fire-detection-system)" 
"# Fire-Detection" 
