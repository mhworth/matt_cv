from django import forms

class ContactForm(forms.Form):
    sender = forms.EmailField(required=False,help_text="An email address (optional)")
    name = forms.CharField(max_length=150,required=False,help_text="Your name (optional)")
    subject = forms.CharField(max_length=250,required=False,help_text="")
    message = forms.CharField(widget=forms.Textarea)