# Real-Time Facial Emotion Recognition System  
**Computer Vision + Deep Learning + Real-Time Application**

This project implements a **real-time facial emotion recognition** system capable of identifying **seven emotional states** from live video or still images.  
It combines **facial detection, head pose estimation, image preprocessing, deep learning classification**, and a **desktop application interface**.

### Recognized Emotions:
Happiness • Sadness • Anger • Fear • Disgust • Surprise • Neutral

---

## ✨ Key Features
| Feature | Description |
|--------|-------------|
| **Real-Time Detection** | Classifies emotions from live webcam feed with low latency |
| **Head Pose Estimation** | Detects face orientation to improve recognition robustness |
| **Custom CNN Model** | ~2.28M parameters, optimized for performance & generalization |
| **Dataset Fusion** | Combined samples from multiple datasets to increase diversity |
| **Data Augmentation Pipeline** | Rotation, brightness normalization, structural preservation |
| **Desktop Application** | Built using Tkinter + OpenCV, no browser required |

---
Camera → Face Detection (MediaPipe) → ROI Extraction →
Preprocessing (Grayscale, 224×224 Resize) → CNN Model →
Emotion Prediction → GUI Display (Tkinter)

## 🧠 System Architecture

---

## 🗂 Dataset
This project merges and processes samples from:

- **FER-Plus**
- **RAF-DB**

### Dataset Processing:
- Removed images without valid detected faces
- Converted all images to **grayscale**
- Resized to **224×224**
- Balanced & expanded classes using augmentation

---

## 🧬 Data Preprocessing & Augmentation
To improve generalization and deal with class imbalance:

- Horizontal Flip
- Controlled Angle Rotations
- Morphological Closing to maintain structure
- Brightness Normalization based on median luminance

These steps helped the model perform reliably in **real-world lighting and pose variations**.

---

## 🏗 Model Architecture (CNN)
- Depthwise-Separable Convolutions (MobileNet-inspired)
- ~**2.28 million** trainable parameters
- Softmax output for 7 emotion classes
- Designed for **real-time inference** on CPU

Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 conv2d (Conv2D)             (None, 112, 112, 32)      320       
                                                                 
 batch_normalization (Batch  (None, 112, 112, 32)      128       
 Normalization)                                                  
                                                                 
 re_lu (ReLU)                (None, 112, 112, 32)      0         
                                                                 
 depthwise_conv2d (Depthwis  (None, 112, 112, 32)      320       
 eConv2D)                                                        
                                                                 
 batch_normalization_1 (Bat  (None, 112, 112, 32)      128       
 chNormalization)                                                
                                                                 
 re_lu_1 (ReLU)              (None, 112, 112, 32)      0         
                                                                 
 conv2d_1 (Conv2D)           (None, 112, 112, 64)      2112      
                                                                 
 batch_normalization_2 (Bat  (None, 112, 112, 64)      256       
 chNormalization)                                                
                                                                 
 re_lu_2 (ReLU)              (None, 112, 112, 64)      0         
                                                                 
 depthwise_conv2d_1 (Depthw  (None, 56, 56, 64)        640       
 iseConv2D)                                                      
                                                                 
 batch_normalization_3 (Bat  (None, 56, 56, 64)        256       
 chNormalization)                                                
                                                                 
 re_lu_3 (ReLU)              (None, 56, 56, 64)        0         
                                                                 
 conv2d_2 (Conv2D)           (None, 56, 56, 128)       8320      
                                                                 
 batch_normalization_4 (Bat  (None, 56, 56, 128)       512       
 chNormalization)                                                
                                                                 
 re_lu_4 (ReLU)              (None, 56, 56, 128)       0         
                                                                 
 depthwise_conv2d_2 (Depthw  (None, 56, 56, 128)       1280      
 iseConv2D)                                                      
                                                                 
 batch_normalization_5 (Bat  (None, 56, 56, 128)       512       
 chNormalization)                                                
                                                                 
 re_lu_5 (ReLU)              (None, 56, 56, 128)       0         
                                                                 
 conv2d_3 (Conv2D)           (None, 56, 56, 128)       16512     
                                                                 
 batch_normalization_6 (Bat  (None, 56, 56, 128)       512       
 chNormalization)                                                
                                                                 
 re_lu_6 (ReLU)              (None, 56, 56, 128)       0         
                                                                 
 depthwise_conv2d_3 (Depthw  (None, 28, 28, 128)       1280      
 iseConv2D)                                                      
                                                                 
 batch_normalization_7 (Bat  (None, 28, 28, 128)       512       
 chNormalization)                                                
                                                                 
 re_lu_7 (ReLU)              (None, 28, 28, 128)       0         
                                                                 
 conv2d_4 (Conv2D)           (None, 28, 28, 256)       33024     
                                                                 
 batch_normalization_8 (Bat  (None, 28, 28, 256)       1024      
 chNormalization)                                                
                                                                 
 re_lu_8 (ReLU)              (None, 28, 28, 256)       0         
                                                                 
 depthwise_conv2d_4 (Depthw  (None, 28, 28, 256)       2560      
 iseConv2D)                                                      
                                                                 
 batch_normalization_9 (Bat  (None, 28, 28, 256)       1024      
 chNormalization)                                                
                                                                 
 re_lu_9 (ReLU)              (None, 28, 28, 256)       0         
                                                                 
 conv2d_5 (Conv2D)           (None, 28, 28, 512)       131584    
                                                                 
 batch_normalization_10 (Ba  (None, 28, 28, 512)       2048      
 tchNormalization)                                               
                                                                 
 re_lu_10 (ReLU)             (None, 28, 28, 512)       0         
                                                                 
 depthwise_conv2d_5 (Depthw  (None, 14, 14, 512)       5120      
 iseConv2D)                                                      
                                                                 
 batch_normalization_11 (Ba  (None, 14, 14, 512)       2048      
 tchNormalization)                                               
                                                                 
 re_lu_11 (ReLU)             (None, 14, 14, 512)       0         
                                                                 
 conv2d_6 (Conv2D)           (None, 14, 14, 512)       262656    
                                                                 
 batch_normalization_12 (Ba  (None, 14, 14, 512)       2048      
 tchNormalization)                                               
                                                                 
 re_lu_12 (ReLU)             (None, 14, 14, 512)       0         
                                                                 
 depthwise_conv2d_6 (Depthw  (None, 14, 14, 512)       5120      
 iseConv2D)                                                      
                                                                 
 batch_normalization_13 (Ba  (None, 14, 14, 512)       2048      
 tchNormalization)                                               
                                                                 
 re_lu_13 (ReLU)             (None, 14, 14, 512)       0         
                                                                 
 conv2d_7 (Conv2D)           (None, 14, 14, 512)       262656    
                                                                 
 batch_normalization_14 (Ba  (None, 14, 14, 512)       2048      
 tchNormalization)                                               
                                                                 
 re_lu_14 (ReLU)             (None, 14, 14, 512)       0         
                                                                 
 depthwise_conv2d_7 (Depthw  (None, 14, 14, 512)       5120      
 iseConv2D)                                                      
                                                                 
 batch_normalization_15 (Ba  (None, 14, 14, 512)       2048      
 tchNormalization)                                               
                                                                 
 re_lu_15 (ReLU)             (None, 14, 14, 512)       0         
                                                                 
 conv2d_8 (Conv2D)           (None, 14, 14, 512)       262656    
                                                                 
 batch_normalization_16 (Ba  (None, 14, 14, 512)       2048      
 tchNormalization)                                               
                                                                 
 re_lu_16 (ReLU)             (None, 14, 14, 512)       0         
                                                                 
 depthwise_conv2d_8 (Depthw  (None, 14, 14, 512)       5120      
 iseConv2D)                                                      
                                                                 
 batch_normalization_17 (Ba  (None, 14, 14, 512)       2048      
 tchNormalization)                                               
                                                                 
 re_lu_17 (ReLU)             (None, 14, 14, 512)       0         
                                                                 
 depthwise_conv2d_9 (Depthw  (None, 7, 7, 512)         5120      
 iseConv2D)                                                      
                                                                 
 batch_normalization_18 (Ba  (None, 7, 7, 512)         2048      
 tchNormalization)                                               
                                                                 
 re_lu_18 (ReLU)             (None, 7, 7, 512)         0         
                                                                 
 conv2d_9 (Conv2D)           (None, 7, 7, 1024)        525312    
                                                                 
 batch_normalization_19 (Ba  (None, 7, 7, 1024)        4096      
 tchNormalization)                                               
                                                                 
 re_lu_19 (ReLU)             (None, 7, 7, 1024)        0         
                                                                 
 average_pooling2d (Average  (None, 1, 1, 1024)        0         
 Pooling2D)                                                      
                                                                 
 dense (Dense)               (None, 1, 1, 700)         717500    
                                                                 
 dropout (Dropout)           (None, 1, 1, 700)         0         
                                                                 
 flatten (Flatten)           (None, 700)               0         
                                                                 
 dense_1 (Dense)             (None, 7)                 4907      
                                                                 
=================================================================
Total params: 2286631 (8.72 MB)
Trainable params: 2272935 (8.67 MB)
Non-trainable params: 13696 (53.50 KB)



---

## ⚙️ Training Configuration
| Parameter | Value |
|---------|-------|
| Epochs | 100 |
| Optimizer | RMSProp |
| Loss | Categorical Crossentropy |
| LR Schedule | Reduce on Plateau |
| Early Stopping | Patience = 5 |
| Input Size | **224×224**, Grayscale |

---

## 📊 Evaluation
| Metric | Value |
|--------|-------|
| **Validation Accuracy** | **~79%** |
| **Test Accuracy** | Similar performance across classes |

Add later:
- Accuracy Curve
- Loss Curve
- Confusion Matrix

---

## 💻 Real-Time Desktop Application
The application interface was built using **Tkinter**, with **OpenCV** handling frame capture and processing.

### Main Capabilities:
- Live webcam emotion recognition
- Image and video file support
- Display of predicted emotion in real time


---

## 🚀 How to Run
```bash
pip install -r requirements.txt
python app.py

Ensure your webcam is connected.

