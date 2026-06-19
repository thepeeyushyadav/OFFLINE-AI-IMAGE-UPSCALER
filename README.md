<div align="center">

# 🪄 Offline AI Image Upscaler

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://offline-ai-image-upscaler-izhsuhcptv5gwxaawoswei.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](#)
[![PyTorch](https://img.shields.io/badge/PyTorch-AI-ee4c2c?logo=pytorch&logoColor=white)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#)

**Developed by: Piyush**

A powerful, easy-to-use **AI Image Upscaler** built with Streamlit and Real-ESRGAN. <br> Enhance, sharpen, and upscale your low-resolution or blurry images by 4x without losing quality!

<h3><a href="https://offline-ai-image-upscaler-izhsuhcptv5gwxaawoswei.streamlit.app/">🔴 CLICK HERE FOR LIVE DEMO 🔴</a></h3>

</div>

---

<div align="center">
  <img src="./image.png" alt="App Screenshot" width="800" style="border-radius: 10px; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);">
</div>

---

## ✨ Key Features

- **🌐 Live Cloud Version:** Instantly accessible via Streamlit Community Cloud.
- **⚡ AI-Powered Upscaling:** Utilizes the state-of-the-art `RealESRGAN_x4plus` model for stunning image enhancement.
- **💻 100% Offline Capability:** Can be run completely offline on your local machine.
- **🎮 GPU Acceleration (CUDA):** Automatically detects and uses your NVIDIA GPU (like RTX 3050) for blazing-fast processing locally.
- **🧩 Memory Optimized:** Smart image tiling prevents Out-Of-Memory (OOM) crashes on systems with limited VRAM.
- **🎨 Interactive UI:** A clean, modern, and beautiful web interface.
- **🔍 Side-by-Side Comparison:** Compare the original and upscaled images with dynamic dimensions before saving.

---

## 🚀 How to Run Locally

Want to run it on your own PC for maximum privacy and GPU speed? Follow these steps:

### Prerequisites
- Python 3.8 to 3.11 installed.
- (Optional but Recommended) An NVIDIA GPU with updated drivers for fast upscaling.

### 1. Clone the repository

```bash
git clone https://github.com/thepeeyushyadav/OFFLINE-AI-IMAGE-UPSCALER.git
cd OFFLINE-AI-IMAGE-UPSCALER
```

### 2. Install Dependencies

Install the required Python packages. 

```bash
pip install -r requirements.txt
```
*(Note: To use GPU acceleration locally, you may need to install the CUDA version of PyTorch separately using `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121`)*

### 3. Start the App

```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** - For the interactive web interface.
- **[Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)** - Core AI algorithms.
- **[PyTorch](https://pytorch.org/)** - Deep learning backend.
- **[OpenCV](https://opencv.org/)** & **[Pillow](https://python-pillow.org/)** - Image processing and manipulation.

---

<div align="center">
  Made with ❤️ by <b>Piyush</b>
</div>
