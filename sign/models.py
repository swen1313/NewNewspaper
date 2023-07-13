from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")


    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "email",
                  "password1",
                  "password2", )



# Create your models here.
