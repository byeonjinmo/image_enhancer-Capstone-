from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from .models import Image
from PIL import Image as PilImage
import io
from django.shortcuts import render, get_object_or_404
# views.py
from django.shortcuts import render

# 여기에 GAN 처리를 위한 함수들을 추가합니다.
def process_with_gan(image_file):
    # GAN 처리 로직을 구현합니다.
    # 여기서는 가상의 코드로, 실제 구현이 필요합니다.
    return processed_image_stream

def process_with_advanced_gan(image_file):
    # 고급 GAN 처리 로직을 구현합니다.
    # 여기서는 가상의 코드로, 실제 구현이 필요합니다.
    return processed_image_stream

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
            # 무료 GAN 처리
            processed_image_stream = process_with_gan(original_image)
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



