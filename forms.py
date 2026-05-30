from django import forms
from .models import Recipe, RewardClaim

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['cuisine', 'subcuisine', 'title', 'region', 'description', 'photo', 'video', 'ingredients', 'instructions']
        widgets = {
            'cuisine': forms.Select(attrs={'class': 'form-control'}),
            'subcuisine': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make photo and video optional
        self.fields['photo'].required = False
        self.fields['video'].required = False
        self.fields['region'].required = False
        self.fields['description'].required = False


class RewardClaimForm(forms.ModelForm):
    class Meta:
        model = RewardClaim
        fields = [
            'account_holder_name',
            'bank_name',
            'account_number',
            'ifsc_code',
            'contact_email',
            'contact_phone',
        ]
        widgets = {
            'account_holder_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter account holder name'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter bank name'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter account number'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter IFSC code'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact email'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact phone (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact_phone'].required = False
