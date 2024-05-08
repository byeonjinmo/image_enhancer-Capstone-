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
# 이미지 처리 함수
def enhance_image(image_file, size):
    # 이미지 크기를 조정하는 로직
    if size == "original":
        pil_image = PilImage.open(image_file)
    else:
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

        # 이미지 저장 및 상세 페이지로 리디렉션
        image_instance.save()
        # 선택된 옵션에 따라 이미지 처리
        enhance_option = request.POST.get('enhance_option')
        if enhance_option == 'gan':
            def load_pretrained_weights(self,generator_weights):
                self.generator.load_weights(generator_weights)
            # DCGAN 인스턴스 생성
            dcgan_instance = DCGAN()
            dcgan_instance.load_pretrained_weights('/Users/mac/Desktop/24년 대학/image_enhancer/celebA_5epoch_pth/generator_weights.pth')

            # 업로드된 이미지 객체 가져오기
            input_pil_image = PilImage.open(original_image).convert("RGB")

            # DCGAN을 사용하여 이미지 개선
            enhanced_pil_image = dcgan_instance.generate_image(input_pil_image)

            # 개선된 이미지를 바이트 스트림으로 변환
            processed_image_stream = io.BytesIO()
            enhanced_pil_image.save(processed_image_stream, format='JPEG', quality=90)
            processed_image_stream.seek(0)

            # 바이트 스트림에서 Django 이미지 필드에 저장할 수 있는 ContentFile 생성
            processed_image_file = ContentFile(processed_image_stream.read(), name="enhanced_" + original_image.name)

            # 개선된 이미지 저장
            image_instance.enhanced_image.save(processed_image_file.name, processed_image_file)

            # 이미지 인스턴스 저장 및 상세 페이지로 리디렉션
            image_instance.save()
            return redirect('image_detail', image_id=image_instance.id)


        elif enhance_option == 'advanced_gan':
            def load_pretrained_weights(model, weights_path):
                model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))

                model.eval()

            # 유료 고급 GAN 처리

            iterations = int(request.POST.get('iterations', 10))  # 사용자 입력 반복 횟수

            srgan_instance = GeneratorResNet()

            load_pretrained_weights(srgan_instance, '/Users/mac/Desktop/24년 대학/image_enhancer/celebA_5epoch_pth/M_generator_900.pth')

            input_pil_image = PilImage.open(original_image).convert("L") # RGB -> L

            # 반복적 이미지 향상

            for _ in range(iterations):
                input_tensor = TF.to_tensor(input_pil_image).unsqueeze(0)

                with torch.no_grad():
                    enhanced_tensor = srgan_instance(input_tensor)

                enhanced_tensor = (enhanced_tensor.squeeze().detach() + 1) / 2

                input_pil_image = TF.to_pil_image(enhanced_tensor)

            save_enhanced_image(input_pil_image, "enhanced_srgan_" + original_image.name, image_instance)

        # 이미지 인스턴스 저장 및 상세 페이지로 리디렉션

        return redirect('image_detail', image_id=image_instance.id)

    return render(request, 'enhancer/upload.html')


def save_enhanced_image(enhanced_pil_image, filename, image_instance):
    processed_image_stream = io.BytesIO()

    enhanced_pil_image.save(processed_image_stream, format='JPEG', quality=90)

    processed_image_stream.seek(0)

    processed_image_file = ContentFile(processed_image_stream.read(), name=filename)

    image_instance.enhanced_image.save(processed_image_file.name, processed_image_file)

    image_instance.save()



# 이미지 상세 보기 뷰
def image_detail_view(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    return render(request, 'enhancer/image_detail.html', {'image': image})

# 시작 화면
def index_view(request):
    return render(request, 'index.html')
