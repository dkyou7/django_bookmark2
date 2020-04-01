from django import forms

class PostSearchForm(forms.Form):
    search_world = forms.CharField(label='Search Word')