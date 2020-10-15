from django import forms
from .models import Review


class ReviewModelForm(forms.ModelForm):
    description = forms.CharField(label='', 
            widget=forms.Textarea(attrs={'rows': 2,'placeholder': 'Add a review'}))
    class Meta:
        model = Review
        fields = ('title','description','rating')