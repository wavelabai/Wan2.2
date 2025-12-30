#!/bin/bash

# Food I2V Generation Script for A100 GPU
# 음식 촬영용 Image-to-Video 생성

echo "Starting Food I2V Generation..."
echo "GPU: A100-1G.10GB"
echo ""

# CUDA 설정 확인
nvidia-smi

echo ""
echo "Running Python script..."
python run_food_i2v.py

echo ""
echo "Done!"
