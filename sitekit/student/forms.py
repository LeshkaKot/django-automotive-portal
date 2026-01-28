from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator
from django.utils.deconstruct import deconstructible
from .models import Category, Manual, TagPost, Student


@deconstructible
class EngValidator:
    ALLOWED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789- "
    code = 'eng'


    def __init__(self, message=None):
        self.message = message if message else "Only Eng characters, hyphens and numbers."


    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Not selected")
    manual = forms.ModelChoiceField(queryset=Manual.objects.all(), required=False, empty_label="There is no manual yet")

    class Meta:
        model = Student
        fields = ["title", "slug", "content", "photo", "is_published", "cat", "manual", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 50, "rows": 8}),
        }
        labels={
            "title": "Car Model",
            "is_published": "Post Status",
            "slug": "URL",
        }


    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 50:
            raise ValidationError("Too match letters :)")

        return title



class UploadFileForm(forms.Form):
    file = forms.ImageField(label="File")
    



class ContactForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50)
    email = forms.EmailField(label="Email")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
