from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=255)
    original_image = models.ImageField(upload_to='images/')
    enhanced_image = models.ImageField(upload_to='enhanced/', blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # 이 모델은 원본 이미지(original_image), 개선된 이미지(enhanced_image),
    # 그리고 이미지 제목(title)을 포함함. upload_to 옵션은 업로드된 파일을 저장할 하위 디렉토리를 지정함.