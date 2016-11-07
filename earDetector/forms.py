from django import forms


class PhotoUpload(forms.Form):
    image = forms.ImageField(label='Select a image')