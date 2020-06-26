from django import forms
from AdminFunc.models import Student_Details, Employee_Details, Classes, Institute_Info
from django.contrib.auth.models import User

class Student_Detail_Form(forms.ModelForm):
	Gender = [('Male','Male'),('Female','Female'),('Others','Others')]
	Nation = [('Indian','Indian'),('Other','Other')]
	gender = forms.CharField(widget=forms.Select(choices=Gender),required = False)
	nationality = forms.CharField(widget=forms.Select(choices=Nation))
	img = forms.ImageField(required=False)
	alt_no = forms.IntegerField(required=False)
	father_name = forms.CharField(required=False)
	mother_name = forms.CharField(required=False)
	father_occupation = forms.CharField(required=False)
	mother_occupation = forms.CharField(required=False)
	class Meta():
		model = Student_Details
		fields = '__all__'
		exclude = ['student','img']

class Employee_Detail_Form(forms.ModelForm):
	Gender = [('Male','Male'),('Female','Female'),('Others','Others')]
	EMP = [('Teaching','Teaching'),('Non-Teaching','Non-Teaching')]
	Nation = [('Indian','Indian'),('Other','Other')]
	gender = forms.CharField(widget=forms.Select(choices=Gender),required = False)
	emp_type = forms.CharField(widget=forms.Select(choices=EMP))
	nationality = forms.CharField(widget=forms.Select(choices=Nation))
	alt_ph = forms.IntegerField(required=False)
	img = forms.ImageField(required=False)
	class Meta():
		model = Employee_Details
		fields = '__all__'
		exclude = ['employee','img']

class SignUpFormStu(forms.ModelForm):
    class Meta:
        model=User
        #fields='__all__'
        fields='__all__'
        exclude = ['last_login','is_active','date_joined','is_superuser','is_staff']
        widgets={'password':forms.PasswordInput()}

class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        #fields='__all__'
        fields='__all__'
        exclude = ['last_login','is_active','is_superuser']
        widgets={'password':forms.PasswordInput()}

class ClassesForm(forms.ModelForm):
    class Meta:
        model=Classes
        #fields='__all__'
        fields='__all__'
        exclude = ['added_by']

class Institute_Info_Form(forms.ModelForm):
	alt_contact = forms.CharField(required = False)
	class Meta:
		model = Institute_Info
		fields='__all__'
		exclude = ['logo']
		widgets={'rules':forms.Textarea()}