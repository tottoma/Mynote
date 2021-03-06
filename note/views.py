from django.shortcuts import render, redirect
from django.http import HttpResponse

import django_filters
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic import ListView
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User

from .models import HeartLog, Note, Category, KeyLog
from .forms import NoteForm

from django.http import JsonResponse
from django.http import QueryDict

#新規    'bootstrap4',           # django-bootstrap4
def formfunc(request):
    if request.method == 'GET':## 新規作成
        form = NoteForm()
    elif request.method == 'POST':## 保存すると「updata/<note_id>」へredirect
        form = NoteForm(request.POST)
        if form.is_valid():##
            note = form.save(commit=False)
            note.user = request.user
            note_id=note.note_id
            note.save()
            return redirect('updata', note_id=note.note_id)
    return render(request, 'form.html', {'form': form})

#編集 & 分析
def updataformfunc(request, note_id):
    note = get_object_or_404(Note, note_id=note_id)# 対象の記事情報を取得
    if request.method == 'POST':# 更新
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note.save()
            return redirect('updata', note_id=note_id)
    else: # GETの場合はデータを表示
        form = NoteForm(instance=note)
    return render(request, 'updata.html', {'form': form, 'note': note})
# ノート削除
def deleteformfunc(request, note_id):
    note = get_object_or_404(Note, note_id=note_id)
    keylogs = KeyLog.objects.filter(note_id=note_id)
    keylogs.delete()
    note.delete()
    notes = Note.objects.all()
    return redirect('list')#render(request, 'list.html', {'notes': notes})
# ノート一覧
@login_required
def listfunc(request):
    notes = Note.objects.filter(user=request.user)
    categories = notes.order_by('category').distinct().values_list("category", flat=True)
    c = Category.objects.filter()
    ##notes = Note.objects.get(user=request.user)
    return render(request, 'list.html', {'notes': notes, 'categories':categories, 'c': c})

# 心拍グラフの表示
def mybpmfunc(request):
    ##bpms = HeartLog.objects.get(user=get_user_model())
    return render(request, 'mybpm.html')

## bpm入出力
class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeartLog
        fields = '__all__'
## 検索 http://<endpoint>/?<fieldname>__gte=YYYY-MM-DD%20HH:mm:ss
class LogFilter(django_filters.FilterSet):
    class Meta:
        model = HeartLog
        fields = {'measured_at': ['gte', ], }
## WebAPIの定義
class LogViewSet(viewsets.ModelViewSet):
    queryset = HeartLog.objects.all().order_by("measured_at")

    serializer_class = LogSerializer
    filter_class = LogFilter

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

## keylog入出力
class KeyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyLog
        fields = '__all__'
## KeyLog検索 http://<endpoint>/?<note_id>__gte=1~
class KeyLogFilter(django_filters.FilterSet):
    class Meta:
        model = KeyLog
        fields = {'note_id': ['gte', ], }
## KeyLog WebAPIの定義
class KeyLogViewSet(viewsets.ModelViewSet):
    queryset = KeyLog.objects.all().order_by("note_id")
    serializer_class = KeyLogSerializer
    filter_class = KeyLogFilter

class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Note.objects.all()
        context['category_list'] = Category.objects.all()
        context['note_list'] = KeyLog.objects.order_by('note_id').distinct().values_list("note_id", flat=True).reverse()[:5]
        return context
