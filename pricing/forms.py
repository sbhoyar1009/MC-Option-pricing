from django import forms
from .models import OptionParameters

class OptionParametersForm(forms.ModelForm):

    class Meta:
        model = OptionParameters
        fields = ['ticker', 'strike_price', 'expiry_date', 'risk_free_rate', 'volatility']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ticker': forms.TextInput(attrs={'class': 'form-control'}),
            'strike_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'risk_free_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'volatility': forms.NumberInput(attrs={'class': 'form-control'}),
        }
