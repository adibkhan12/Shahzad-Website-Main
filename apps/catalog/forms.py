from django import forms

from .models import QA, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["user", "rating", "text"]
        widgets = {
            "user": forms.TextInput(attrs={"placeholder": "Your name"}),
            "rating": forms.HiddenInput(),
            "text": forms.Textarea(attrs={"rows": 3, "placeholder": "Share your experience…"}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = QA
        fields = ["user", "question"]
        widgets = {
            "user": forms.TextInput(attrs={"placeholder": "Your name"}),
            "question": forms.Textarea(attrs={"rows": 2, "placeholder": "Ask a question about this product…"}),
        }
