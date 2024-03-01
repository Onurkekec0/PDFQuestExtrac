from django import forms

class SoruForm(forms.Form):
    soru = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    cevap = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[('A', 'A) Kırmızı ve beyaz'), ('B', 'B) Mavi ve yeşil'), ('C', 'C) Sarı ve siyah'), ('D', 'D) Sarı ve siyah')]
    )