from .models import Application, User
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator

#файл где мы пишем формы которые используются для ввода данных пользователем

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=255, label="Логин"),

    full_name = forms.CharField(max_length=255, label="ФИО"),
    
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Подтвердите пароль")
    email = forms.EmailField(label="Email")
    checkbox = forms.CharField(label='Согласие на обработку персональных данных', widget=forms.CheckboxInput, required=False)

    class Meta:
        model = User
        fields = ('username','email', 'full_name')

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not all(char.isalpha() or char.isspace() or char == '-' for char in full_name):
            raise forms.ValidationError("ФИО должно содержать только кириллические буквы, дефис и пробелы.")
        return full_name

    def clean_username(self):
        username = self.cleaned_data['username']
        if not all(char.isalpha() or char == '-' for char in username):
            raise forms.ValidationError("Логин может содержать только латинские буквы и дефис.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Логин уже занят.")
        return username

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2
    
    def clean_checkbox(self):
        cd = self.cleaned_data
        print(cd['checkbox'])
        if cd['checkbox'] == False:
            raise forms.ValidationError('Подтвердите обработку персональных данных')
        return cd['checkbox']

class ApplicationCreateForm(forms.ModelForm):
    title = forms.CharField(label='Название',widget=forms.TextInput)
    desc = forms.CharField(label='Описание', widget=forms.TextInput)

    
    class Meta:
        model = Application
        fields = ('title', 'desc', 'img')

        # Add some custom validation to our image field
    def clean_img(self):
        img = self.cleaned_data.get('img', False)
        if img:
            if img._size > 2 * 1024 * 1024:
                raise ValidationError("Img file too large ( > 2mb )")
            return img
        else:
            raise ValidationError("Couldn't read uploaded img")

