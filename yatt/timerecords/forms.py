from timerecords.models import Project, Record
from django import forms

class RecordForm(forms.ModelForm):

    project=forms.ModelChoiceField(queryset=None, empty_label=None)
    class Meta:
        model = Record
        exclude={'user'}
        widgets={'start_time': forms.widgets.SplitDateTimeWidget(),}
    
    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        try:
            self.fields['project'].queryset = Project.objects.filter(user = self.instance.user)
        except:
            pass