from django import forms
from .models import Post

class UsernameChangeForm(forms.Form):
    new_username = forms.CharField(max_length=150, label="New Username")
    
    


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image']
        widgets = {
            'caption': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False