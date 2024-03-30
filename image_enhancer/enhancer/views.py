from django.shortcuts import redirect
from django.core.files.base import ContentFile
from .models import Image
from PIL import Image as PilImage
import io
from django.shortcuts import get_object_or_404
# views.py
from django.shortcuts import render

# GAN 기능 임포트
import os
import argparse
import torch.nn as nn
import torch
from torchvision.transforms import functional as TF

from .models.dcgan import DCGAN
# GAN 모델을 초기화하고 가중치를 불러옵니다.
dcgan_instance = DCGAN()

generator = dcgan_instance.generator(128)
generator.load_state_dict(torch.load('../celebA_5epoch_pth/generator_weights.pth', map_location='cpu'))
generator.eval()

# 이미지 처리 함수
def enhance_image(image_file, size):
    # 사용자가 선택한 크기로 이미지 크기를 조정하는 로직
    size = tuple(map(int, size.split('x')))
    pil_image = PilImage.open(image_file)
    pil_image = pil_image.resize(size, PilImage.ANTIALIAS)
    output_io_stream = io.BytesIO()
    pil_image.save(output_io_stream, format='JPEG', quality=90)
    output_io_stream.seek(0)
    return output_io_stream


def upload_image_view(request):
    if request.method == 'POST' and request.FILES['original_image']:
        title = request.POST.get('title', '')
        original_image = request.FILES['original_image']
        enhanced_size = request.POST.get('enhanced_size', '800x600')  # 기본값 설정

        image_instance = Image(title=title)
        image_instance.original_image.save(original_image.name, original_image)

        # 이미지 처리 로직 호출
        enhanced_image_stream = enhance_image(original_image, enhanced_size)
        enhanced_image_file = ContentFile(enhanced_image_stream.read(), name="enhanced_" + original_image.name)
        image_instance.enhanced_image.save(enhanced_image_file.name, enhanced_image_file)

        image_instance.save()

        # 선택된 옵션에 따라 이미지 처리
        enhance_option = request.POST.get('enhance_option')
        if enhance_option == 'gan':
            # 이미지를 전처리
            input_image = TF.to_tensor(PilImage.open(original_image).convert("RGB"))
            input_image = TF.resize(input_image, size=(64, 64))  # DCGAN에 맞는 이미지 사이즈 조절
            input_image = input_image.unsqueeze(0)  # 가짜 배치 차원 추가

            # GAN을 이용하여 이미지를 개선합니다.
            with torch.no_grad():
                generated_image = generator(input_image)

            # 후처리를 거쳐 이미지를 저장합니다.
            processed_image = TF.to_pil_image(generated_image.squeeze(0))
            processed_image_stream = io.BytesIO()
            processed_image.save(processed_image_stream, format='JPEG')
            processed_image_stream.seek(0)
            processed_image_file = ContentFile(processed_image_stream.read(), name="enhanced_" + original_image.name)
            image_instance.enhanced_image.save(processed_image_file.name, processed_image_file)

            # 이미지 인스턴스를 저장하고 상세 페이지로 리디렉트합니다.
            image_instance.save()
            return redirect('image_detail', image_id=image_instance.id)
        elif enhance_option == 'advanced_gan':
            # 유료 고급 GAN 처리
            processed_image_stream = process_with_advanced_gan(original_image)

        image_instance.save()

        return redirect('image_detail', image_id=image_instance.id)

    return render(request, 'enhancer/upload.html')
# 이미지 상세 보기 뷰
def image_detail_view(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    return render(request, 'enhancer/image_detail.html', {'image': image})

# 시작 화면
def index_view(request):
    return render(request, 'index.html')


