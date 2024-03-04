from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image_view, name='upload_image'),
    # 여기서 정의한 'upload/'는 'enhancer/' URL 패턴 뒤에 붙으므로,
    # 실제 URL은 http://127.0.0.1:8000/enhancer/upload/ 로 접속해야 함.
    # 이미지 상세 보기 URL 추가.
    path('image/<int:image_id>/', views.image_detail_view, name='image_detail'),
]
