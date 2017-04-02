from django import forms


class PhotoUpload(forms.Form):
    image = forms.ImageField(label='Select a image')
    xml = forms.CharField(label='xml', max_length=100, required=True)
    cascade = forms.BooleanField(required=False)
    ellipse_find = forms.BooleanField(required=False)

    def clean_field(self,field_name):
        if self.cleaned_data[field_name] is None:
            return self.fields[field_name].initial
        return self.cleaned_data[field_name]