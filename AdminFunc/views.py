from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from AdminFunc.forms import Student_Detail_Form, SignUpForm, Employee_Detail_Form, SignUpFormStu, ClassesForm, Institute_Info_Form
from AdminFunc.models import Student_Details, Employee_Details, Classes, Subjects, Institute_Info
from django.contrib import messages
from MajorSys1.utils import render_to_pdf
from django.template.loader import get_template

# Create your views here.

def AdminHome(request):
	return render(request,'AdminFunc/adminhome.html')

def Add_Student(request):
	if request.method == "POST":
		signup = SignUpFormStu(request.POST)
		student_form = Student_Detail_Form(request.POST)
		if signup.is_valid() and student_form.is_valid():
			signup_data = signup.save(commit=False)
			signup_data.set_password(signup_data.password)
			signup_data.save()
			student_save=student_form.save(commit=False)
			student_save.student = signup_data
			student_save.save()
			return render(request,'AdminFunc/new_student.html',{'msg':"Student Created Successfully"})
	else:
		return render(request,'AdminFunc/new_student.html')

def Show_Students(request):
	students = Student_Details.objects.all()
	return render(request,'AdminFunc/show_students_employee.html',{'student':students})

def validate_username(request):
	uname = request.GET.get('username')
	data={ 'is_exist':User.objects.filter(username__iexact=uname).exists()}
	return JsonResponse(data)

def validate_email(request):
	email = request.GET.get('email')
	data={ 'is_exist':User.objects.filter(email__iexact=email).exists()}
	return JsonResponse(data)

def Add_Employee(request):
	if request.method == "POST":
		signup = SignUpForm(request.POST)
		faculty_form = Employee_Detail_Form(request.POST)
		if signup.is_valid() and faculty_form.is_valid():
			signup_data = signup.save(commit=False)
			signup_data.set_password(signup_data.password)
			signup_data.save()

			faculty_save=faculty_form.save(commit=False)
			faculty_save.employee = signup_data
			faculty_save.save()
			return render(request,'AdminFunc/new_employee.html',{'msg':"Employee Created Successfully"})
		else:
			print(signup.errors,faculty_form.errors)
	else:
		return render(request,'AdminFunc/new_employee.html')

def Show_Employees(request):
	emp = Employee_Details.objects.all()
	return render(request,'AdminFunc/show_students_employee.html',{'employee':emp})

def Show_classes(request):
	data = Classes.objects.all()
	return render(request,'AdminFunc/show_classes.html',{'data':data})

def Add_Classes(request):
	if request.method=='POST':
		class_form = ClassesForm(request.POST)
		if class_form.is_valid():
			class_data = class_form.save(commit=False)
			class_data.added_by=request.user
			class_data.save()
			return render(request,'AdminFunc/add_class.html',{'data':'Class created Successfully'})
		else:
			print('*'*50,class_form.errors)
	else:
		return render(request,'AdminFunc/add_class.html')

def Edit_Classes(request,id):
	class_data = Classes.objects.get(id=id)
	if request.method=='POST':
		topic = request.POST['topic']
		fees = request.POST['fees']
		class_data.update(topic= topic, fees= fees)
		return render(request,'AdminFunc/add_class.html',{'data':'Class updated Successfully'})
	else:
		return render(request,'AdminFunc/add_class.html',{'update':class_data})

def Delete_Classes(request):
	id_val = request.GET.get('id')
	data = Classes.objects.filter(id=id_val).delete()
	print(data)
	data_resp = {'resp': True}
	return JsonResponse(data_resp)

def Delete_Subject(request):
	id_val = request.GET.get('id')
	data = Subjects.objects.filter(id=id_val).delete()
	data_resp = {'resp': True}
	return JsonResponse(data_resp)

def Add_Subjects(request,id):
	ca = Classes.objects.get(id=id)
	if request.method=="POST":
		ite = request.POST['x_value']
		for i in range(int(ite)):
			topics = request.POST['topic'+str(i+1)]
			mark = request.POST['marks'+str(i+1)]
			data=Subjects(topic=topics, weightage=mark, added_by=request.user, class_assigned=ca).save()
		return render(request,'AdminFunc/edit_add_subjects.html',{'ca':ca,'data':'Subject/s added Successfully'})
	else:
		return render(request,'AdminFunc/edit_add_subjects.html',{'ca':ca})

def Edit_Subjects(request,id):
	so = Subjects.objects.get(id=id)
	if request.method=="POST":
		top = request.POST['topic']
		mark = request.POST['marks']
		so.update(topic=top, weightage=mark)
		return render(request,'AdminFunc/edit_add_subjects.html',{'data':'Subject updated Successfully'})
	else:
		return render(request,'AdminFunc/edit_add_subjects.html',{'update':so})

def Profile_Student(request,id):
	data = Student_Details.objects.get(id=id)
	user = User.objects.get(id=data.student.id)
	cont_data = {'stud':data,'user':user}
	if request.method=="POST":
		if request.POST['subnum']=='1':
			image = request.FILES['img']
			data.img = image
			data.save()
			messages.success(request, "Picture updated Successfully")
			return HttpResponseRedirect('/adminf/profile_student/'+id+'/')
		elif request.POST['subnum']=='2':
			dataup = Student_Details.objects.filter(id=id)
			userup = User.objects.filter(id=data.student.id)
			userup.update(first_name = request.POST['fname'])
			userup.update(last_name = request.POST['lname'])
			dataup.update(father_name=request.POST['father_name'])
			dataup.update(mother_name=request.POST['mother_name'])
			dataup.update(father_occupation=request.POST['father_occupation'])
			dataup.update(mother_occupation=request.POST['mother_occupation'])
			dataup.update(father_no=request.POST['father_no'])
			dataup.update(mother_no=request.POST['mother_no'])
			dataup.update(alt_no=request.POST['alt_no'])
			dataup.update(perm_address=request.POST['perm_address'])
			dataup.update(dob=request.POST['dob'])
			dataup.update(gender=request.POST['gender'])
			dataup.update(nationality=request.POST['nationality'])
			messages.success(request, "Your data has been saved!")
			return HttpResponseRedirect('/adminf/profile_student/'+id+'/')

	return render(request,'AdminFunc/student_employee_editprofile.html',cont_data)

def Delete_Student(request,id):
	stud = Student_Details.objects.get(id=id)
	User.objects.get(id=stud.student.id).delete()
	messages.success(request, "Your data has been deleted!")
	return HttpResponseRedirect('/adminf/show_students/')

def Institute_info(request):
	exist,create = Institute_Info.objects.get_or_create(id=1)
	if create:
		data = Institute_Info.objects.all()
		if request.method=="POST":
			if request.POST['subnum']=='1':
				img = request.FILES['logo']
				data.logo=img
				data.save()
				messages.success(request, "Picture saved Successfully")
				return HttpResponseRedirect('/adminf/institute_info/')
			else:
				fdata = Institute_Info_Form(request.POST)
				if fdata.is_valid:
					fdata.save()
				messages.success(request, "Data saved Successfully")
				return HttpResponseRedirect('/adminf/institute_info/')
		return render(request,'AdminFunc/institute_info.html',{'data':data})
	else:
		data = Institute_Info.objects.get(id=1)
		if request.method=="POST":
			if request.POST['subnum']=='1':
				img = request.FILES['logo']
				data.logo=img
				data.save()
				messages.success(request, "Picture saved Successfully")
				return HttpResponseRedirect('/adminf/institute_info/')
			elif request.POST['subnum']=='2':
				dataup = Institute_Info.objects.filter(id=1)
				dataup.update(slogan = request.POST['slogan'])
				dataup.update(name = request.POST['name'])
				dataup.update(contact = request.POST['contact'])
				dataup.update(alt_contact = request.POST['alt_contact'])
				dataup.update(website = request.POST['website'])
				dataup.update(email = request.POST['email'])
				dataup.update(address = request.POST['address'])
				dataup.update(city = request.POST['city'])
				dataup.update(state = request.POST['state'])
				dataup.update(country = request.POST['country'])
				dataup.update(rules = request.POST['rules'])
				messages.success(request, "Data saved Successfully")
				return HttpResponseRedirect('/adminf/institute_info/')
		return render(request,'AdminFunc/institute_info.html',{'data':data})
	return render(request,'AdminFunc/institute_info.html',{'data':data})

def Academic_Details(request):
	return render(request,'AdminFunc/student_academics.html/')

def Print_Letter(request,id):
	template = get_template('AdminFunc/student_employee_editprofile.html')
	data = Student_Details.objects.get(id=id)
	user = User.objects.get(id=data.student.id)
	context = {'stud':data,'user':user}
	html = template.render(context)
	return HttpResponse(html)

def Validate_Class_Name(request):
	name = request.GET.get('value')
	data={ 'is_exist':Classes.objects.filter(topic__iexact=name).exists()}
	return JsonResponse(data)

def View_Employees(request):
	return render(request,'AdminFunc/view_employee.html')

def Edit_Employee(request,id):
	data = Employee_Details.objects.get(id=id)
	user = User.objects.get(id=data.employee.id)
	cont_data = {'employee':data,'user':user}
	if request.method=="POST":
		if request.POST['subnum']=='1':
			image = request.FILES['img']
			data.img = image
			data.save()
			messages.success(request, "Picture saved Successfully")
			return HttpResponseRedirect('/adminf/edit_employee/'+id+'/')
		elif request.POST['subnum']=='2':
			dataup = Employee_Details.objects.filter(id=id)
			userup = User.objects.filter(id=data.employee.id)
			userup.update(first_name = request.POST['fname'])
			userup.update(last_name = request.POST['lname'])
			dataup.update(experience=request.POST['experience'])
			dataup.update(emp_type=request.POST['emp_type'])
			dataup.update(salary=request.POST['salary'])
			dataup.update(specialization=request.POST['specialization'])
			dataup.update(contact=request.POST['contact'])
			dataup.update(alt_ph=request.POST['alt_ph'])
			dataup.update(address=request.POST['address'])
			dataup.update(dob=request.POST['dob'])
			dataup.update(gender=request.POST['gender'])
			dataup.update(nationality=request.POST['nationality'])
			messages.success(request, "Your data has been saved!")
			return HttpResponseRedirect('/adminf/edit_employee/'+id+'/')
	else:
		return render(request,'AdminFunc/student_employee_editprofile.html',cont_data)

def Delete_Employee(request,id):
	emp = Employee_Details.objects.get(id=id)
	User.objects.get(id=emp.employee.id).delete()
	messages.success(request, "Deleted Successfully")
	return HttpResponseRedirect('/adminf/show_employees/')