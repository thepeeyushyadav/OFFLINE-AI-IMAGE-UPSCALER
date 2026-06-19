import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import sys
from torchvision.transforms import functional as F
# Monkey-patch: fixes basicsr/realesrgan bug with torchvision >= 0.20
sys.modules['torchvision.transforms.functional_tensor'] = F

import streamlit as st
from PIL import Image
import time
import io
from upscaler import get_device, load_model, enhance_image
import torch

st.set_page_config(page_title="AI Image Upscaler", page_icon="🪄", layout="wide")

# Custom CSS for aesthetics (Day 6 Project)
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

st.title("🪄 Offline AI Image Upscaler")
st.markdown("### Powered by Real-ESRGAN and your local RTX 3050 GPU")

# Check and display the active device
dev = get_device()
if dev.type == 'cuda':
    st.success(f"🚀 GPU Active: **{torch.cuda.get_device_name(0)}** is ready to accelerate!")
else:
    st.warning("⚠️ Running on CPU. It will take a bit longer. (Check if PyTorch with CUDA is installed)")

# Cache the model loading so it doesn't reload on every UI interaction
@st.cache_resource
def get_upsampler():
    return load_model(dev)

# Only load model if we are ready
try:
    with st.spinner("Loading AI Model into Memory..."):
        upsampler = get_upsampler()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

uploaded_file = st.file_uploader("Drop a blurry or low-res image here", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image
    original_image = Image.open(uploaded_file).convert("RGB")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔍 Original Image")
        st.image(original_image, use_container_width=True)
        st.caption(f"Size: {original_image.size[0]} x {original_image.size[1]} pixels")
    
    with col2:
        st.markdown("#### ✨ Enhanced Image (4x)")
        
        # We need a placeholder for the output while it's processing
        output_placeholder = st.empty()
        
        if 'upscaled_image' not in st.session_state or st.session_state.get('last_uploaded') != uploaded_file.name:
            if st.button("🚀 Enhance Now!"):
                with st.spinner("AI is working its magic... (Might take a few seconds)"):
                    start_time = time.time()
                    
                    try:
                        # Call our backend function
                        upscaled = enhance_image(original_image, upsampler)
                        
                        end_time = time.time()
                        
                        # Save in session state so it doesn't disappear
                        st.session_state['upscaled_image'] = upscaled
                        st.session_state['last_uploaded'] = uploaded_file.name
                        st.session_state['time_taken'] = round(end_time - start_time, 2)
                        
                    except RuntimeError as e:
                        if "out of memory" in str(e).lower():
                            st.error("GPU Out of Memory! The image might be too large. Try a smaller one or enable tiling in upscaler.py.")
                        else:
                            st.error(f"Error: {e}")
        
        # Display the upscaled image if it exists in session state
        if 'upscaled_image' in st.session_state and st.session_state.get('last_uploaded') == uploaded_file.name:
            result_img = st.session_state['upscaled_image']
            time_taken = st.session_state['time_taken']
            
            output_placeholder.image(result_img, use_container_width=True)
            st.caption(f"Size: {result_img.size[0]} x {result_img.size[1]} pixels (Took {time_taken} seconds)")
            
            # Prepare for download
            buf = io.BytesIO()
            result_img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="💾 Download Enhanced Image",
                data=byte_im,
                file_name=f"upscaled_{uploaded_file.name}.png",
                mime="image/png"
            )
