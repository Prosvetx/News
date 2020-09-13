from django import forms
from .models import New


# p =

class NewForm(forms.ModelForm):
    class Meta:
        model = New
        fields = ['title', 'text', 'section','picture']
        widgets = {'text': forms.Textarea(attrs={'cols': 90, 'rows': 30, 'class': 'createnew_textfield'}),
                   'title': forms.TextInput(attrs={'color': 'white',
                                                   })
                   }
