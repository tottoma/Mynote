from django.urls import path
from .views import listfunc, formfunc, mybpmfunc, updataformfunc, deleteformfunc

urlpatterns = [
    path('note/list/', listfunc, name='list'),
    ##path('', listfunc, name='list'),
    path('note/', formfunc, name='form'),
    path('note/<int:note_id>/updata/', updataformfunc, name='updata'),
    path('note/<int:note_id>/delete/', deleteformfunc, name='delete'),
    ##path('detail/<int:pk>', detailfunc, name='detail'),
    path('mybpm/', mybpmfunc, name='mybpm'),
]
