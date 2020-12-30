from django.urls import path
from .views import listfunc, formfunc, detailfunc, mybpmfunc, updataformfunc
from note.views import NoteList

urlpatterns = [
    path('list/', listfunc, name='list'),
    ##path('', listfunc, name='list'),
    path('form/', formfunc, name='form'),
    path('updata/<int:note_id>', updataformfunc, name='updata'),
    ##path('detail/<int:pk>', detailfunc, name='detail'),
    path('mybpm/', mybpmfunc, name='mybpm'),
]
