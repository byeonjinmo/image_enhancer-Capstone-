from django.shortcuts import redirect
from django.core.files.base import ContentFile
from PIL import Image as PilImage
import io
from .models import Image
from django.shortcuts import get_object_or_404
# views.p
from django.shortcuts import render

# GAN 기능 임포트
import torch
from torchvision.transforms import functional as TF

# GAN 모델을 초기화하고 가중치를 불러온다.
from .models.dcgan import DCGAN
from .models.srgan1.model_srgan import GeneratorResNet
# 체크포인트 파일 로드
checkpoint = torch.load(srgan_checkpoint_path, map_location=torch.device('cpu'))

# 체크포인트에 포함된 키 출력
print(checkpoint.keys())

# 상태 불러오기
srgan_instance.load_state_dict(checkpoint['generator'])  # 'model_state_dict' 대신 실제 키 사용
srgan_instance.eval()

try:
    srgan_instance.load_state_dict(checkpoint['model_state_dict'])
except KeyError:
    print("Error: 'model_state_dict' key is not found. Available keys:", checkpoint.keys())
