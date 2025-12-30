# Food I2V Generation Guide

음식 이미지에서 자연스러운 카메라 움직임을 가진 영상을 생성하는 가이드입니다.

## 환경

- **GPU**: A100-1G.10GB (2 vCPU, 24 GiB RAM)
- **CUDA**: 12.4
- **해상도**: 720x1280 (9:16 세로)
- **프레임**: 81 frames

## 카메라 모션 설명

```
Motion: Very slow handheld orbital pan around food
- 15–30도 회전
- 자연스러운 미세 흔들림 (micro-shake)
- 스마트폰/미러리스 느낌
- 실제 레스토랑 깊이감
- 9:16 세로 비율
- 음식은 고정, 카메라만 움직임
- 4K 현실적 텍스처
```

## 사용 방법

### 1. 이미지 준비

`images/` 폴더에 음식 이미지를 넣으세요:
```
images/
├── 1.png
└── 2.png
```

### 2. 체크포인트 경로 확인

`run_food_i2v.py` 파일에서 체크포인트 경로를 실제 경로로 수정하세요:
```python
CKPT_DIR = "checkpoints"  # <- 여기를 수정
```

### 3. 실행

#### 방법 A: Python 스크립트 직접 실행
```bash
python run_food_i2v.py
```

#### 방법 B: Bash 스크립트 실행
```bash
chmod +x run_i2v.sh
./run_i2v.sh
```

#### 방법 C: 단일 이미지 직접 실행
```bash
python generate.py \
  --task i2v-A14B \
  --ckpt_dir checkpoints \
  --image images/1.png \
  --prompt "A very slow handheld orbital camera movement panning around the food dish, rotating 15 to 30 degrees with subtle natural micro-shake and gentle drift. Shot with a phone or mirrorless camera capturing real restaurant depth of field. The food dish remains perfectly still and centered while only the camera moves smoothly around it. Soft natural lighting with bokeh background, professional food photography style, 9:16 vertical aspect ratio, 4K resolution with hyper-realistic textures and appetizing presentation." \
  --size 720*1280 \
  --frame_num 81 \
  --sample_steps 40 \
  --sample_shift 5.0 \
  --sample_guide_scale 5.0 \
  --offload_model True
```

## 출력

생성된 영상은 `outputs/` 폴더에 저장됩니다:
```
outputs/
├── 1_food_motion.mp4
└── 2_food_motion.mp4
```

## 파라미터 설명

| 파라미터 | 값 | 설명 |
|---------|-----|------|
| `--task` | i2v-A14B | Image-to-Video 14B 모델 |
| `--size` | 720*1280 | 9:16 세로 비율 (Instagram/TikTok) |
| `--frame_num` | 81 | 프레임 수 (4n+1 규칙) |
| `--sample_steps` | 40 | 샘플링 스텝 (높을수록 품질 향상) |
| `--sample_shift` | 5.0 | 노이즈 스케줄 (720p에는 3.0 권장) |
| `--sample_guide_scale` | 5.0 | CFG 스케일 (프롬프트 충실도) |
| `--offload_model` | True | GPU 메모리 절약 모드 |

## 프롬프트 커스터마이징

`run_food_i2v.py` 파일에서 `FOOD_CAMERA_PROMPT` 변수를 수정하여 다른 카메라 움직임을 시도할 수 있습니다:

```python
# 예시 1: 더 빠른 움직임
FOOD_CAMERA_PROMPT = (
    "A smooth orbital camera movement panning around the food dish, "
    "rotating 45 degrees with dynamic motion..."
)

# 예시 2: 줌인/줌아웃
FOOD_CAMERA_PROMPT = (
    "A slow push-in camera movement towards the food dish, "
    "gradually revealing details..."
)

# 예시 3: 위에서 아래로
FOOD_CAMERA_PROMPT = (
    "A slow crane down camera movement from top view to eye level, "
    "revealing the food presentation..."
)
```

## 트러블슈팅

### GPU 메모리 부족
- `--offload_model True` 사용 (이미 설정됨)
- `--sample_steps`를 30으로 낮추기
- `--frame_num`을 65로 줄이기

### 품질 개선
- `--sample_steps`를 50으로 높이기
- `--sample_guide_scale`를 7.0으로 높이기
- 프롬프트에 더 구체적인 설명 추가

### 해상도 변경
```python
# 1080p (9:16)
SIZE = "1080*1920"
SAMPLE_SHIFT = 3.0  # 낮은 해상도에는 더 낮은 shift 사용

# 480p (9:16)
SIZE = "480*854"
SAMPLE_SHIFT = 3.0
```

## 참고사항

- 생성 시간: 이미지당 약 5-15분 (GPU 성능에 따라 다름)
- 최적의 입력 이미지: 고해상도, 선명한 음식 사진
- 배경 블러가 있는 이미지가 더 좋은 결과를 냅니다
