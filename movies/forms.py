from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'class':'search-box','min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'class':'search-box','rows': 4,'placeholder': 'Write your review here...'}),
        }
        labels = {
            'rating': 'Rating (1-5)',
            'text': 'Your Review',
        }