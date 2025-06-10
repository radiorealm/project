from django import forms

class GrantSearchForm(forms.Form):
    query = forms.CharField(widget=forms.Textarea, label="Describe your grant needs")