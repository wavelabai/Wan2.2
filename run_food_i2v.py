#!/usr/bin/env python
# Copyright 2024-2025 Food I2V Generation Script
"""
음식 촬영용 Image-to-Video 생성 스크립트
Motion: very slow handheld orbital pan around food,
15–30 degrees rotation, natural micro-shake,
phone or mirrorless camera vibe, real restaurant depth,
9:16, locked dish position, only camera moves, 4K realistic textures
"""

import os
import subprocess
import sys
from pathlib import Path

# 프롬프트 설정 - 음식 촬영용 카메라 움직임 설명
FOOD_CAMERA_PROMPT = (
    "A very slow handheld orbital camera movement panning around the food dish, "
    "rotating 15 to 30 degrees with subtle natural micro-shake and gentle drift. "
    "Shot with a phone or mirrorless camera capturing real restaurant depth of field. "
    "The food dish remains perfectly still and centered while only the camera moves smoothly around it. "
    "Soft natural lighting with bokeh background, professional food photography style, "
    "9:16 vertical aspect ratio, 4K resolution with hyper-realistic textures and appetizing presentation."
)

# 설정
IMAGES_DIR = "images"
CKPT_DIR = "checkpoints"  # 체크포인트 경로 (실제 경로로 수정 필요)
OUTPUT_DIR = "outputs"
SIZE = "720*1280"  # 9:16 세로 비율
FRAME_NUM = 81  # 4n+1 규칙
SAMPLE_STEPS = 40
SAMPLE_SHIFT = 5.0
GUIDE_SCALE = 5.0

def run_i2v_generation(image_path, output_name=None):
    """단일 이미지에 대해 i2v 생성 실행"""

    if output_name is None:
        output_name = f"{Path(image_path).stem}_food_motion.mp4"

    output_path = os.path.join(OUTPUT_DIR, output_name)

    # Python 명령어 구성
    cmd = [
        sys.executable,  # 현재 Python 인터프리터
        "generate.py",
        "--task", "i2v-A14B",
        "--ckpt_dir", CKPT_DIR,
        "--image", image_path,
        "--prompt", FOOD_CAMERA_PROMPT,
        "--size", SIZE,
        "--frame_num", str(FRAME_NUM),
        "--sample_steps", str(SAMPLE_STEPS),
        "--sample_shift", str(SAMPLE_SHIFT),
        "--sample_guide_scale", str(GUIDE_SCALE),
        "--save_file", output_path,
        "--offload_model", "True",  # GPU 메모리 절약
    ]

    print(f"\n{'='*80}")
    print(f"Processing: {image_path}")
    print(f"Output: {output_path}")
    print(f"{'='*80}\n")
    print(f"Command: {' '.join(cmd)}\n")

    # 실행
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✓ Successfully generated: {output_path}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error generating video from {image_path}: {e}\n")
        return False

def main():
    # Output 디렉토리 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # images 폴더의 모든 이미지 찾기
    image_extensions = {'.png', '.jpg', '.jpeg', '.JPG', '.PNG', '.JPEG'}
    images_path = Path(IMAGES_DIR)

    if not images_path.exists():
        print(f"Error: {IMAGES_DIR} directory not found!")
        return

    image_files = [
        f for f in images_path.iterdir()
        if f.suffix in image_extensions
    ]

    if not image_files:
        print(f"No images found in {IMAGES_DIR}/")
        return

    print(f"\nFound {len(image_files)} image(s) in {IMAGES_DIR}/")
    print(f"Checkpoint directory: {CKPT_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"\nPrompt: {FOOD_CAMERA_PROMPT}\n")

    # 각 이미지에 대해 생성
    successful = 0
    failed = 0

    for idx, image_file in enumerate(image_files, 1):
        print(f"\n[{idx}/{len(image_files)}] Processing {image_file.name}...")

        if run_i2v_generation(str(image_file)):
            successful += 1
        else:
            failed += 1

    # 결과 요약
    print(f"\n{'='*80}")
    print(f"Generation Complete!")
    print(f"{'='*80}")
    print(f"Successful: {successful}/{len(image_files)}")
    print(f"Failed: {failed}/{len(image_files)}")
    print(f"Outputs saved to: {OUTPUT_DIR}/")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
