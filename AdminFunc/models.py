from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student_Details(models.Model):
	student = models.OneToOneField(User, on_delete=models.CASCADE)
	created_by = models.CharField(max_length=30)
	dob = models.DateField()
	gender = models.CharField(max_length=6, null=True, blank=True)
	nationality = models.CharField(max_length=20)
	img = models.ImageField(upload_to='student_profile', default='student_profile/default.jpg')
	alt_no = models.CharField(max_length=10, null=True, blank=True)
	father_no = models.CharField(max_length=10)
	mother_no = models.CharField(max_length=10)
	perm_address = models.CharField(max_length=70)
	father_name = models.CharField(max_length=30, null=True, blank=True)
	mother_name = models.CharField(max_length=30, null=True, blank=True)
	father_occupation = models.CharField(max_length=30, null=True, blank=True)
	mother_occupation = models.CharField(max_length=30, null=True, blank=True)

class Employee_Details(models.Model):
	employee = models.OneToOneField(User, on_delete=models.CASCADE)
	created_by = models.CharField(max_length=30)
	experience = models.IntegerField()
	salary = models.DecimalField(max_digits=10, decimal_places=2)
	contact = models.CharField(max_length=10)
	alt_ph = models.CharField(max_length=10 ,null=True, blank=True)
	dob = models.DateField()
	specialization = models.CharField(max_length=50)
	emp_type = models.CharField(max_length=13)
	gender = models.CharField(max_length=6, null=True, blank=True)
	nationality = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	img = models.ImageField(upload_to='teacher_profile', default='teacher_profile/default.jpg')

class Classes(models.Model):
	added_by = models.ForeignKey(User, on_delete=models.CASCADE)
	topic = models.CharField(max_length=20)
	fees = models.DecimalField(max_digits=15, decimal_places=2)

class Subjects(models.Model):
	added_by = models.ForeignKey(User, on_delete=models.CASCADE)
	class_assigned = models.ForeignKey(Classes, on_delete=models.CASCADE)
	topic = models.CharField(max_length=40, unique=False)
	weightage = models.DecimalField(max_digits=4, decimal_places=2)

class Institute_Info(models.Model):
	logo = models.ImageField(upload_to='institute_info', default='institute_info/default.jpg')
	slogan = models.CharField(max_length=250)
	name = models.CharField(max_length=30)
	contact = models.CharField(max_length=10)
	alt_contact = models.CharField(max_length=10, null=True)
	website = models.URLField(max_length=30)
	email = models.EmailField(max_length=100)
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	rules = models.CharField(max_length=10000)