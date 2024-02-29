from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from .models import Image
from PIL import Image as PilImage
import io
from django.shortcuts import render, get_object_or_404

# 이미지 처리 함수
def enhance_image(image_file):
    pil_image = PilImage.open(image_file)
    output_io_stream = io.BytesIO()
    pil_image = pil_image.resize((800, 600), PilImage.ANTIALIAS)
    pil_image.save(output_io_stream, format='JPEG', quality=90)
    output_io_stream.seek(0)
    return output_io_stream

def upload_image_view(request):
    if request.method == 'POST' and request.FILES['original_image']:
        title = request.POST.get('title', '')
        original_image = request.FILES['original_image']

        image_instance = Image(title=title)
        image_instance.original_image.save(original_image.name, original_image)

        # 이미지 처리 로직 호출
        enhanced_image_stream = enhance_image(original_image)
        enhanced_image_file = ContentFile(enhanced_image_stream.read(), name="enhanced_" + original_image.name)
        image_instance.enhanced_image.save(enhanced_image_file.name, enhanced_image_file)

        image_instance.save()

        return redirect('image_detail', image_id=image_instance.id)

    return render(request, 'enhancer/upload.html')
# 이미지 상세 보기 뷰
def image_detail_view(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    return render(request, 'enhancer/image_detail.html', {'image': image})
