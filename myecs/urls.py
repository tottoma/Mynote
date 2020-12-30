"""myecs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

    データベースの作成に関する参考サイト
    https://dot-blog.jp/news/how-to-reset-django-migrations/
"""
from django.conf.urls import url
from django.contrib import admin

from django.urls import path, include
from rest_framework import routers

from note.views import LogViewSet, KeyLogViewSet
from note.views import MainView

router = routers.DefaultRouter()
router.register(r'logs', LogViewSet)
router.register(r'keylogs', KeyLogViewSet)

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('', include('note.urls')),

    url(r'^admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
# ログイン画面のタイトルを変更
admin.site.site_header = 'MyECS'
