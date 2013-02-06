from django.forms import ModelForm
from timerecords.models import Project, Record

class RecordForm(ModelForm):
    class Meta:
        model = Record