from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from PIL import Image as PilImage
import io
import subprocess
from .models import Image
import torch
from torchvision.transforms import functional as TF
import os
from django.conf import settings
from django.shortcuts import render
import os
from django.core.files import File

output_directory = 'C:/Users/user/Desktop/chat_jin/image_enhancer-Capstone--JM/image_enhancer/media/enhanced'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Image
import os

@require_POST
def delete_image(request):
    image_id = request.POST.get('image_id')
    if image_id:
        image = Image.objects.get(id=image_id)
        if image.original_image:
            if os.path.exists(image.original_image.path):
                os.remove(image.original_image.path)  # 파일 시스템에서 이미지 삭제
            image.original_image.delete()  # Django에서 파일 필드 삭제
        image.delete()  # 이미지 레코드 삭제
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def save_image_to_model(image_path, title):
    # Image 모델 인스턴스 생성
    image_instance = Image(title=title)

    # 파일 시스템에서 이미지 파일 열기
    with open(image_path, 'rb') as file:
        django_file = File(file)
        image_instance.original_image.save(os.path.basename(image_path), django_file)

    image_instance.save()
    return image_instance.id

def upload_image_view(request):
    if request.method == 'POST' and request.FILES['original_image']:
        title = request.POST.get('title', '')
        original_image = request.FILES['original_image']
        image_instance = Image(title=title)
        image_instance.original_image.save(original_image.name, original_image)

        # 외부 스크립트 실행
        script_path = 'C:/Users/user/Desktop/chat_jin/srgan_1(jin)/srgan.py'
        output_image_path = os.path.join(output_directory, 'enhanced_' + original_image.name)

        subprocess.run([
            'python', script_path,
            # '--input_image', input_image_path,
            # '--output_image', output_image_path,
            # '--checkpoint', model_checkpoint_path
        ], check=True)

        # 이미지 URL 업데이트
        #image_instance.enhanced_image = output_image_path
        #image_instance.save()

        # 이미지가 저장된 경로
        image_path = 'C:/Users/user/Desktop/chat_jin/image_enhancer-Capstone--JM/image_enhancer/media/enhanced/0_.png'
        image_title = 'Generated Image'

        # 이미지 파일을 `enhanced_image` 필드에 저장
        image_instance.enhanced_image.save('enhanced_' + original_image.name, File(open(image_path, 'rb')))
        image_instance.save()
        #image_id = save_image_to_model(image_path, image_title)
        return redirect('image_detail', image_id=image_instance.id)

    return render(request, 'enhancer/upload.html')


def image_detail_view(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    return render(request, 'enhancer/image_detail.html', {'image': image})


def index_view(request):
    return render(request, 'index.html')