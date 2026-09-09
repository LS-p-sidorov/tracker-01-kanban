from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Board, Profile, Task


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username",)


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ("title",)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "description", "board", "status")
        widgets = {
            "board": forms.Select(attrs={"class": "field"}),
            "title": forms.TextInput(attrs={"class": "field"}),
            "description": forms.Textarea(attrs={"class": "field", "rows": 4}),
            "status": forms.Select(attrs={"class": "field"}),
        }


class RoleForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("role",)
        widgets = {"role": forms.Select(attrs={"class": "field"})}
