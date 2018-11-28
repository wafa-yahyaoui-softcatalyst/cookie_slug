from django import forms

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


class FeedbackForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    feedback = forms.CharField(widget=forms.Textarea)

    def clean_email(self):
        data = self.cleaned_data['email']
        domain = data.split('@')[1]
        domain_list = ["softcatalyst.com", ]
        if domain not in domain_list:
            raise forms.ValidationError("Email is invalid. The email should be a softcatalyst email")
        return data

