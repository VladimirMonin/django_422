# Импортируем класссы форм и модели
import re
from django import forms
from .models import Post, Category, Tag

# Обычная НЕ связанная с моделью
class TagForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        min_length=2,
        label="Название",
        help_text="Введите название тега",
        required=True,
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        if Tag.objects.filter(name=name).exists():
            raise forms.ValidationError('Тег с таким названием уже существует')
        return name

    class Meta:
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }

        error_messages = {
            "name": {
                "min_length": "Название должно быть не менее 2 символов",
                "max_length": "Название должно быть не более 200 символов",
                "required": "Название обязательно для заполнения",
            }
        }

