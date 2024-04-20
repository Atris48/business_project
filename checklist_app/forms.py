from django import forms

from checklist_app.models import Checklist


class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        exclude = ('order',)
