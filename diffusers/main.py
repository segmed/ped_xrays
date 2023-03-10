import os
import sys
import subprocess
new_path = os.getcwd()

print(f"current path {os.getcwd()}")
print(f"to change to path {new_path}")

if "diffusers" not in new_path:
    os.chdir(f"{new_path}/diffusers")
    # implement pip as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    '.'])

print(f"current path {os.getcwd()}")




import streamlit as st
from diffusers import StableDiffusionPipeline
import torch
from pathlib import Path
from tqdm import tqdm
tqdm(disable=True, total=0)

st.header('stable diffusion generating xrays')

model_name= "stabilityai/stable-diffusion-2"
model_path = f"{Path.cwd()}/ped-xray-model-lora"    

pipe = StableDiffusionPipeline.from_pretrained(model_name, torch_dtype=torch.float32)
pipe.unet.load_attn_procs(model_path)

with st.form("my_form"):
    sel_col, _  =st.columns(2)
    prompt_label = sel_col.selectbox("Pick an input prompt", options=["normal", "bacteria", "virus"])
    guidance_scale = sel_col.slider("What is the gudiance", min_value=4, max_value=20)

    print("before submit")
    submitted = st.form_submit_button("Submit")
    print("after submit")

    if submitted:
        print("submitted")

        try:
            print("before pipe")
            image = pipe(prompt_label, num_inference_steps=30, guidance_scale=guidance_scale).images[0]
            print("after pipe")
            st.image(image)        
            print("after image")
        except: 
            print("Unexpected error:", sys.exc_info()[0])
        finally:
            print('in finally block')

