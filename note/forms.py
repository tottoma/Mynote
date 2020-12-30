from django import forms
from .models import Note

"""ノート用のフォーム"""
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'category', 'content')
