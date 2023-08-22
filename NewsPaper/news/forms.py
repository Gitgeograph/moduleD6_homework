from django.forms import ModelForm
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth.models import Group
from django import forms
from .models import Post

class PostForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ("author", "title", "categoryType", "postCategory", 'text')
        widgets = {
            'author': forms.Select(attrs={
            'class': 'form-control',
            }),
            'title': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter title'
            }),
            'categoryType': forms.Select(attrs={
            'class': 'form-control',
            }),
            "postCategory": forms.CheckboxSelectMultiple(attrs={
            "class": 'flex-check',
            }),
            'text': forms.Textarea(attrs={
            'class': 'form-control',
            }),
        }


class BasicSignupForm(SignupForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class':'form-control',}))
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})
    
  
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get_or_create(name='common')[0]
        basic_group.user_set.add(user)
        return user
    

class BasicLoginForm(LoginForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
            
    def __init__(self, *args, **kwargs):
        super(BasicLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'class':'form-control'})

    def save(self, request):
        user = super(BasicLoginForm, self).save(request)
        basic_group = Group.objects.get_or_create(name='common')[0]
        basic_group.user_set.add(user)
        return user