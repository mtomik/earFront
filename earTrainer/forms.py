from django.contrib.auth.forms import AuthenticationForm
from django import forms


# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class TrainerParams(forms.Form):
    name = forms.CharField(label='name', required= True)
    samplesId = forms.CharField(label='samplesId', max_length=100, required=True)
    negative_samples = forms.IntegerField(label='negative_samples', min_value=100, max_value=150000, initial=150, required=False)
    num_stages = forms.FloatField(label='num_stages', min_value=1, max_value=1000, initial=20, required=False)
    precalcValBuf = forms.FloatField(label='precalcValBuf', min_value=500, max_value=2000, initial=1500, required=False)
    precalcIdxBuf = forms.FloatField(label='precalcIdxBuf', min_value=500, max_value=2000, initial=1000, required=False)
    numThreads = forms.IntegerField(label='numThreads', min_value=1, max_value=15, initial=4, required=False)
    acceptanceBreak = forms.FloatField(label='acceptanceBreak', min_value=0, max_value=0.3, initial=0.0001, required=False)
    bt = forms.CharField(label='bt', initial='RAB', required=False)
    minHitRate = forms.FloatField(label='minHitRate', min_value=0.3, max_value=1, initial=0.998, required=False)
    maxFalseAlarm = forms.FloatField(label='maxFalseAlarm', min_value=0.1, max_value=1, initial=0.35, required=False)
    weightTrimRate = forms.FloatField(label='weightTrimRate', min_value=0.3, max_value=1, initial=0.95, required=False)
    maxDepth = forms.IntegerField(label='maxDepth', max_value=13, min_value=1, initial=1, required=False)
    maxWeakCount = forms.IntegerField(label='maxWeakCount', max_value=300, min_value=20, initial=150, required=False)
    featureType = forms.CharField(label='featureType', initial='LBP', required=False)
    mode = forms.CharField(label='mode', initial='ALL', required=False)

    def clean_field(self,field_name):
        if self.cleaned_data[field_name] is None:
            return self.fields[field_name].initial
        return self.cleaned_data[field_name]

class CreateSamplesForm(forms.Form):
    name = forms.CharField(label='name', required= True)
    positive_samples = forms.IntegerField(label='pos_samples', max_value=100000, min_value=10,required=True)
    x_angle = forms.FloatField(label='x_angle', min_value=0, max_value=2, initial=1.1, required=False) # 0.3
    y_angle = forms.FloatField(label='y_angle', min_value=0, max_value=2, initial=1.1, required=False) # 0.3
    z_angle = forms.FloatField(label='z_angle', min_value=0, max_value=2, initial=0.5, required=False) # 1.0
    max_dev = forms.IntegerField(label='max_dev', min_value=0, max_value=100, initial=40, required=False)
    w = forms.IntegerField(label='w', min_value=10, max_value=1000, initial=20, required=False)
    h = forms.IntegerField(label='h', min_value=10, max_value=1000, initial=40, required=False)

    def clean_field(self,field_name):
        if self.cleaned_data[field_name] is None:
            return self.fields[field_name].initial
        return self.cleaned_data[field_name]

class TesterParams(forms.Form):
    xml_file = forms.CharField(label='xml_file', max_length=100)

    def clean_field(self,field_name):
        if self.cleaned_data[field_name] is None:
            return self.fields[field_name].initial
        return self.cleaned_data[field_name]

