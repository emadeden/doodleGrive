from django import forms
from .models import * 



class FileForm(forms.ModelForm):
  
    class Meta:
        model = File
        fields = ['name', 'file']


    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'




class UpdateFileForm(forms.ModelForm):
  
    class Meta:
        model = File
        fields = ['name', 'file' , 'groups']


    def __init__(self, *args, **kwargs):
        super(UpdateFileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class editForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['content']
    


    def __init__(self, *args, **kwargs):
        super(editForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

