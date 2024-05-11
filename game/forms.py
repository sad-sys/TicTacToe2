from django import forms

class CodeForm(forms.Form):
    game_code = forms.CharField(label="make_code", max_length=3)