from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import * 

class RegisterForm(UserCreationForm):
	email = forms.EmailField()
	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
			
	class Meta: 
		model = CustomUser
		fields = ["username", "email" , "password1", "password2"]
 


