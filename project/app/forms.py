from django.forms import ModelForm
from django import forms

from .models import Note


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = [
            'title', 'tags', 'markdown_content',
        ]
        required = {
            'title':True,
            'tags':False,
            'markdown_content':True,
        }