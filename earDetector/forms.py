from django import forms


class PhotoUpload(forms.Form):
    image = forms.ImageField(label='image')
    xml_left = forms.CharField(label='xml_left', max_length=100, required=True)
    xml_right = forms.CharField(label='xml_right', max_length=100, required=True)
    cascade = forms.BooleanField(required=False)
    ellipse_find = forms.BooleanField(required=False)
    do_rotation = forms.BooleanField(required=False)
    rotation = forms.IntegerField(required=False, min_value=0, max_value=360)

    def clean_field(self,field_name):
        if self.cleaned_data[field_name] is None:
            return self.fields[field_name].initial
        return self.cleaned_data[field_name]
