from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from PIL import Image as PilImage
import io
from .models import Image
import torch
from torchvision.transforms import functional as TF
from .models.dcgan import DCGAN
from .models.medical_srgan.models import GeneratorResNet

def enhance_image(image_file, size):
    if size == "original":
        pil_image = PilImage.open(image_file)
    else:
        size = tuple(map(int, size.split('x')))
        pil_image = PilImage.open(image_file).resize(size, PilImage.ANTIALIAS)
    output_io_stream = io.BytesIO()
    pil_image.save(output_io_stream, format='JPEG', quality=90)
    output_io_stream.seek(0)
    return output_io_stream
def load_model(checkpoint_path):
    model = GeneratorResNet()
    checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['generator_state_dict'])
    #model.eval()
    return model

def process_single_image(model, image_file):
    input_pil_image = PilImage.open(image_file).convert("L")
    input_tensor = TF.to_tensor(input_pil_image).unsqueeze(0)
    with torch.no_grad():
        enhanced_tensor = model(input_tensor)
    enhanced_tensor = (enhanced_tensor.squeeze().detach() + 1) / 2
    enhanced_pil_image = TF.to_pil_image(enhanced_tensor)
    output_io_stream = io.BytesIO()
    enhanced_pil_image.save(output_io_stream, format='JPEG', quality=90)
    output_io_stream.seek(0)
    return output_io_stream

def upload_image_view(request):
    if request.method == 'POST' and request.FILES['original_image']:
        title = request.POST.get('title', '')
        original_image = request.FILES['original_image']
        image_instance = Image(title=title)
        image_instance.original_image.save(original_image.name, original_image)

        # 이미지 파일 스트림을 처리하기 전에 seek(0)을 호출
        original_image.seek(0)
        model = load_model('/Users/mac/Desktop/24년 대학/image_enhancer/checkpoints/ckpt_epoch_50.pth')
        enhanced_image_stream = process_single_image(model, original_image)

        enhanced_image_file = ContentFile(enhanced_image_stream.read(), name="enhanced_" + original_image.name)
        image_instance.enhanced_image.save(enhanced_image_file.name, enhanced_image_file)
        image_instance.save()
        return redirect('image_detail', image_id=image_instance.id)

    return render(request, 'enhancer/upload.html')

def image_detail_view(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    return render(request, 'enhancer/image_detail.html', {'image': image})

def index_view(request):
    return render(request, 'index.html')


