# Импортируем класссы форм и модели
import re
from django import forms
from .models import Post, Category, Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            'name': 'Название',
        }
        help_texts = {
            'name': 'Введите название тега',
        }
        error_messages = {
            'name': {
                'min_length': 'Название должно быть не менее 2 символов',
                'max_length': 'Название должно быть не более 200 символов',
                'required': 'Название обязательно для заполнения',
            },
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Python',
                'id': 'tag-name'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Tag.objects.filter(name=name).exists():
            raise forms.ValidationError('Тег с таким названием уже существует')
        return name
    