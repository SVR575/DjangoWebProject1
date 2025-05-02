"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models import Comment, Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class FeedbackForm(forms.Form):
    name = forms.CharField(
        label='Ваше имя',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    design_rating = forms.ChoiceField(
        label='Оценка дизайна',
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    navigation_rating = forms.ChoiceField(
        label='Оценка навигации',
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    liked_features = forms.MultipleChoiceField(
        label='Понравившиеся функции',
        choices=[
            ('design', 'Дизайн'),
            ('content', 'Контент'),
            ('usability', 'Удобство использования'),
            ('speed', 'Скорость работы'),
            ('support', 'Поддержка')
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    visit_frequency = forms.ChoiceField(
        label='Частота посещений',
        choices=[
            ('daily', 'Ежедневно'),
            ('weekly', 'Еженедельно'),
            ('monthly', 'Ежемесячно'),
            ('rarely', 'Редко')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    subscribe_news = forms.BooleanField(
        label='Подписаться на новости',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    suggestions = forms.CharField(
        label='Ваши предложения по улучшению',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        subscribe = self.cleaned_data.get('subscribe_news')
        
        if subscribe and not email:
            raise forms.ValidationError('Email обязателен при подписке на новости')
        return email

class CommentForm (forms.ModelForm):
    
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю формы text

class BlogForm(forms.ModelForm):
    title = forms.CharField(
        label='Заголовок',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label='Краткое содержание',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    content = forms.CharField(
        label='Полное содержание',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8})
    )
    image = forms.ImageField(
        label='Картинка',
        required=False
    )

    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image')
