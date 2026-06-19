import cv2
import torch
import numpy as np
from PIL import Image
import os
import urllib.request
import sys
from torchvision.transforms import functional as F

# Monkey-patch to fix basicsr bug with newer torchvision versions
sys.modules['torchvision.transforms.functional_tensor'] = F

from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

def get_device():
    """Detects if CUDA (NVIDIA GPU) is available and returns the device."""
    if torch.cuda.is_available():
        return torch.device('cuda')
    return torch.device('cpu')

def load_model(device):
    """Loads the Real-ESRGAN model and initializes the upsampler."""
    # We use the standard RealESRGAN_x4plus architecture
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    
    # Path where the model will be stored
    model_path = os.path.join(os.path.dirname(__file__), 'weights', 'RealESRGAN_x4plus.pth')
    
    # Download the weights if they don't exist
    if not os.path.exists(model_path):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        url = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth'
        print(f"Downloading model weights to {model_path}...")
        urllib.request.urlretrieve(url, model_path)
        print("Download complete.")
    
    # Initialize the RealESRGANer
    upsampler = RealESRGANer(
        scale=4,
        model_path=model_path,
        dni_weight=None,
        model=model,
        tile=400, # Set to > 0 if you get Out Of Memory (OOM) errors (e.g., 400)
        tile_pad=10,
        pre_pad=0,
        half=device.type == 'cuda', # Use half-precision on GPU to save VRAM and speed up
        device=device,
    )
    return upsampler

def enhance_image(image_pil: Image.Image, upsampler: RealESRGANer) -> Image.Image:
    """Takes a PIL Image, passes it through the AI, and returns the upscaled PIL Image."""
    # Convert PIL Image (RGB) to OpenCV format (BGR)
    img_cv2 = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
    
    # Enhance the image using the AI
    output, _ = upsampler.enhance(img_cv2, outscale=4)
    
    # Convert back to PIL Image (RGB)
    output_pil = Image.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    return output_pil

if __name__ == "__main__":
    # A simple test block to ensure GPU is detected
    dev = get_device()
    print(f"Testing environment. Detected device: {dev}")
    if dev.type == 'cuda':
        print(f"GPU Name: {torch.cuda.get_device_name(0)}")
