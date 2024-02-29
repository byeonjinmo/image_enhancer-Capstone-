"""
URL configuration for image_enhancer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, include  # include를 추가로 임포트합니다.

    # enhancer 앱의 URL을 포함
urlpatterns = [
    path('admin/', admin.site.urls),
    path('enhancer/', include('enhancer.urls')),  # enhancer 앱의 URL 포함
    #  http://127.0.0.1:8000/enhancer/upload/ 주소로 접속
]

 # 미디어 파일 URL을 추가
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
