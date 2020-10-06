from django import forms
from .models import New
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class NewForm(forms.ModelForm):
    class Meta:
        model = New
        fields = ['title', 'text', 'section', 'picture']
        widgets = {'text': forms.Textarea(attrs={'cols': 90, 'rows': 30, 'class': 'createnew_textfield'}),
                   'title': forms.TextInput(attrs={'color': 'white', })
                   }


class SearchForm(forms.Form):
    look_for = forms.CharField(max_length=100)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
