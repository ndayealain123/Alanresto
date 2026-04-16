
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Client

class RegistrationUserForm(UserCreationForm):
	nom = forms.CharField(max_length=20)
	prenom = forms.CharField(max_length=20)

	class Meta:
		model = User
		fields = ("username", "nom", "prenom", "password1", "password2")

	def clean_username(self):
		username = self.cleaned_data.get("username", "").strip()
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError("This username already exists.")
		return username

	def clean(self):
		cleaned_data = super().clean()
		password1 = cleaned_data.get("password1")
		password2 = cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords do not match.")
		return cleaned_data

	def save(self, commit=True):
		user = super().save(commit=False)
		user.first_name = self.cleaned_data["nom"]
		user.last_name = self.cleaned_data["prenom"]
		if commit:
			user.save()
		return user

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			css_classes = field.widget.attrs.get("class", "")
			field.widget.attrs["class"] = f"{css_classes} form-control".strip()


class ClientForm(forms.ModelForm):
	birthday = forms.DateField(
		widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
	)

	class Meta:
		model = Client
		fields = ("birthday", "gender", "phone", "address")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			css_classes = field.widget.attrs.get("class", "")
			field.widget.attrs["class"] = f"{css_classes} form-control".strip()

class ConnexionForm(forms.Form):
	username= forms.CharField(widget= forms.TextInput(attrs={
    		'placeholder':'username....',
			'class': 'form-control',
    		}),label="Username :")
	password = forms.CharField(widget= forms.PasswordInput(attrs={
    		'placeholder':'password....',
			'class': 'form-control',
    		}),label="PassWord :")
	
