from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from AdminFunc.forms import Student_Detail_Form, SignUpForm, Employee_Detail_Form, SignUpFormStu, ClassesForm, Institute_Info_Form
from AdminFunc.models import Student_Details, Employee_Details, Classes, Subjects, Institute_Info, Accounts, Student_Attendance, Employee_Attendance
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date

# Create your views here.

# --------------------------------------------------------------------------------------------------------------------
#  ----------------------------------Dashboard Related Functionalities--------------------------

# Function to reder Admin dashboard page
def AdminHome(request):
	return render(request,'AdminFunc/adminhome.html')

# --------------------------------------------------------------------------------------------------------------------
# ----------------------------------Institute Related Functionalities---------------------------

# This function is to execute all funcnalities of Institute menu
def Institute_info(request):
	# Condition and assignment to check if object is available in database or not
	exist,create = Institute_Info.objects.get_or_create(id=1)
	# If object in database not available
	if create:
		data = Institute_Info.objects.all()  # to get all objects of Institute class
		if request.method=="POST":          # If post request recieved
			if request.POST['subnum']=='1':   # If value of SubmitNumber(subnum) is 1, Update Image
				img = request.FILES['logo']   # Storing Value of image recieved from template
				data.logo=img         # Assigning to data
				data.save()         # Saving updated value
				messages.success(request, "Picture saved Successfully")   # Seding Update message to template
				return HttpResponseRedirect('/adminf/institute_info/')   # Redirecting to Requested page
			else:           # If SubmitNumber(subnum) value is not 1, Update other data
				fdata = Institute_Info_Form(request.POST)  # Getting all data through form
				if fdata.is_valid:     # Validating form data
					fdata.save()     # Saving data
				messages.success(request, "Data saved Successfully")   # Sending success message
				return HttpResponseRedirect('/adminf/institute_info/') # redirecting to desired page
		return render(request,'AdminFunc/institute_info.html',{'data':data}) # If Get Request recieved
	# If  object in database Available
	else:
		data = Institute_Info.objects.get(id=1) # Get all objects with id 1
		if request.method=="POST":           # If Post request recieved
			if request.POST['subnum']=='1':    # If value of subnum is 1 then update image
				img = request.FILES['logo']   # Value of image input from frontend
				data.logo=img   # Assigning value
				data.save()    # Saving value
				messages.success(request, "Picture saved Successfully")  # Sending success message
				return HttpResponseRedirect('/adminf/institute_info/')  # Redirecting to desired page
			elif request.POST['subnum']=='2':  # If value of subnum is 2
				dataup = Institute_Info.objects.filter(id=1)  # Getting all objects with id 1
				# Updating all data we get from templates
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
				messages.success(request, "Data saved Successfully") # Sending Success message
				return HttpResponseRedirect('/adminf/institute_info/')  # Redirecting to desired page
		return render(request,'AdminFunc/institute_info.html',{'data':data})  # If Get request recieved
	# return render(request,'AdminFunc/institute_info.html',{'data':data})

# --------------------------------------------------------------------------------------------------------------------
# ----------------------------------Classes Related Functionalities-----------------------------

# Function to show all class data to desired page
def Show_classes(request):
	data = Classes.objects.all()  # Getting all objects from Classes class
	return render(request,'AdminFunc/show_classes.html',{'data':data}) # Rendering with the objects

# Function to add more classes
def Add_Classes(request):
	if request.method=='POST':  # If requested method is post
		class_form = ClassesForm(request.POST)  # Geting data collected from form
		if class_form.is_valid():  # Validating form
			class_data = class_form.save(commit=False)  # Saving form tempororily
			class_data.added_by=request.user  # Assigning value of Foreign to add
			class_data.save()   # Finally saving data
			# Rendering to desired page with success message
			return render(request,'AdminFunc/add_class.html',{'data':'Class created Successfully'})
	else:   # If requestedx method is Get
		return render(request,'AdminFunc/add_class.html') # rendering to desired page

# Funtion to edit class
def Edit_Classes(request,id):
	class_data = Classes.objects.get(id=id) # to get all objects associated with desired id
	if request.method=='POST':    # If request is post
		topic = request.POST['topic']  # Getting value from post request
		fees = request.POST['fees']		# Getting value from post request
		class_data.update(topic= topic, fees= fees)      # updating objects
		# rendering to desired page after updating data with success message
		return render(request,'AdminFunc/add_class.html',{'data':'Class updated Successfully'})
	else:  # If request is Get
		return render(request,'AdminFunc/add_class.html',{'update':class_data})# rendering to desired page

# Function to add subjects to desired class
def Add_Subjects(request,id):
	ca = Classes.objects.get(id=id)  # getting objects associated with id
	if request.method=="POST":  # If request method is post
		ite = request.POST['x_value']  # Getting value of no of inputs added
		for i in range(int(ite)):  # Iterating to add that no of data
		  	# Getting values of input fields one by one
			topics = request.POST['topic'+str(i+1)]
			mark = request.POST['marks'+str(i+1)]
			# Saving values one by one
			data=Subjects(topic=topics, weightage=mark, added_by=request.user, class_assigned=ca).save()
		# rendering to desired page after ading data with success message
		return render(request,'AdminFunc/edit_add_subjects.html',{'ca':ca,'data':'Subject/s added Successfully'})
	else:  # If request method is get
		return render(request,'AdminFunc/edit_add_subjects.html',{'ca':ca}) # rendering to desired page

# Function to edit desired subject
def Edit_Subjects(request,id):
	so = Subjects.objects.get(id=id)  # Getting objects of subject class associated with that id
	if request.method=="POST":  # If requested method is post
		# Getting data from request
		top = request.POST['topic']
		mark = request.POST['marks']
		# Updating data recieved
		so.update(topic=top, weightage=mark)
		# rendering to desired page after updation with a success message
		return render(request,'AdminFunc/edit_add_subjects.html',{'data':'Subject updated Successfully'})
	else:  # If requested method is GET
		# rendering to desired page
		return render(request,'AdminFunc/edit_add_subjects.html',{'update':so})

# --------------------------------------------------------------------------------------------------------------------
# ----------------------------------Students Related Functionalities----------------------------

# function to add Students
def Add_Student(request):
	classes_obj = Classes.objects.all()
	if request.method == "POST": # If requestefd method is POST
		signup = SignUpFormStu(request.POST)  # Gettingf data through forms
		student_form = Student_Detail_Form(request.POST)  # Getting data through forms
		if signup.is_valid() and student_form.is_valid():  # Validating Data
			signup_data = signup.save(commit=False)  # Saving form temporarily
			signup_data.set_password(signup_data.password)  # Encoding Password
			signup_data.save()  # Saving Data
			student_save=student_form.save(commit=False)  # Saving form temp.
			student_save.student = signup_data  # Saving foreign key
			student_save.save()  # Saving form finally
			# rendering data to desired page after updation with success data
			return render(request,'AdminFunc/new_student.html',{'msg':"Student Created Successfully",'class_obj':classes_obj})
	else:   # If requested method is GET
		# rendering user to desired page
		return render(request,'AdminFunc/new_student.html',{'class_obj':classes_obj})

# Function to show students
def Show_Students(request):
	students = Student_Details.objects.all()  # Getting all objects of Students class
	# Rendering to show student page with all objects
	return render(request,'AdminFunc/show_students_employee.html',{'student':students,'student_rendered':'yes'})

# Function to edit and view profile of desired Student
def Profile_Student(request,id):
	data = Student_Details.objects.get(id=id)  # To get objects associated with id
	user = User.objects.get(id=data.student.id) # To get objects associated with that student
	cont_data = {'stud':data,'user':user,'student_rendered':'yes'}   # Context data to render to page
	if request.method=="POST":  # If requested method is POST
		if request.POST['subnum']=='1':  # IF recieved 1 as subnum, Update image
			image = request.FILES['img']  # Getting image value
			data.img = image  # Assigning image
			data.save()  # Sving data
			# Rendering to desired page after addition with success message
			messages.success(request, "Picture updated Successfully")
			return HttpResponseRedirect('/adminf/profile_student/'+id+'/')
		elif request.POST['subnum']=='2':  # If recieved 2 as subnum
			# Getting sets of requred objects
			dataup = Student_Details.objects.filter(id=id)
			userup = User.objects.filter(id=data.student.id)
			# Getting data from request method and updating them
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
			# Renderring to desired page after updating with a success message
			messages.success(request, "Your data has been saved!")
			return HttpResponseRedirect('/adminf/profile_student/'+id+'/')
	# If GET method recieved, rendering to desired page with context data
	return render(request,'AdminFunc/student_employee_editprofile.html',cont_data)

# Function to delete student record
def Delete_Student(request,id):
	stud = Student_Details.objects.get(id=id)  # Getting all objects assciated with that id
	User.objects.get(id=stud.student.id).delete()   # Deleting data
	messages.success(request, "Your data has been deleted!") # Success message
	return HttpResponseRedirect('/adminf/show_students/') # Rendering to desired page with message

# Function to show academic Details of student
def Academic_Details(request):
	# rendering to desired page
	# Due work, to be done soon
	return render(request,'AdminFunc/student_academics.html/',{'student_rendered':'yes'})

# --------------------------------------------------------------------------------------------------------------------
# ----------------------------------Employee Related Functionalities----------------------------

# Function to add employee
def Add_Employee(request):
	if request.method == "POST": # If requested method is POST
		# Getting data from Forms
		signup = SignUpForm(request.POST)
		faculty_form = Employee_Detail_Form(request.POST)
		if signup.is_valid() and faculty_form.is_valid(): # Validating forms
			signup_data = signup.save(commit=False)   # Saving data tepm in an instance
			signup_data.set_password(signup_data.password) # Encoding password
			signup_data.save()  # saving data
			# Same process with other form just rather than encoding pass here we are saving foreign key
			faculty_save=faculty_form.save(commit=False)
			faculty_save.employee = signup_data
			faculty_save.save()
			# Rendering to desired page after updation with a success message
			return render(request,'AdminFunc/new_employee.html',{'msg':"Employee Created Successfully",'employee_rendered':'yes'})
	else: # IF requested method is GET
		# rendering to desired page
		return render(request,'AdminFunc/new_employee.html',{'employee_rendered':'yes'})

# Function toshow employees list on desired page
def Show_Employees(request):
	emp = Employee_Details.objects.all()  # Getting all objects
	# Rendering to desired page
	return render(request,'AdminFunc/show_students_employee.html',{'employee':emp,'employee_rendered':'yes'})

# Function to view details of employee
def View_Employees(request):
	# rendering to desired page
	# Work to be done soon!
	# pending now
	return render(request,'AdminFunc/view_employee.html')

# Function to Edit Employee details
# this function is same as Profile_Student Function
def Edit_Employee(request,id):
	data = Employee_Details.objects.get(id=id)
	user = User.objects.get(id=data.employee.id)
	cont_data = {'employee':data,'user':user,'employee_rendered':'yes'}
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

# Function to delet employee data
def Delete_Employee(request,id):
	emp = Employee_Details.objects.get(id=id)  # to get objects of desired employee
	User.objects.get(id=emp.employee.id).delete()  # deleting data
	# Redirecting to desired page with success message
	messages.success(request, "Deleted Successfully")
	return HttpResponseRedirect('/adminf/show_employees/')

# --------------------------------------------------------------------------------------------------------------------
# ----------------------------------Accounts Related Functionalities----------------------------

# Function is to show and add account statements
def Show_Accounts(request):
	# To show data
	data = Accounts.objects.all().order_by('-date')  # getting objects of accounts class in descending order of date
	credit = 0  # Variable to store total credit
	debit = 0  # Variable to store total Debit
	if data:    # IF there is some data
		for i in data:  # iterating in data to get credit and debit total
			credit += i.deposite   # Addign credit amount and storing in credit variable
			debit += i.withdrawal   # Addign debit amount and storing in debit variable
	paginator = Paginator(data, 10)  # For pagination on page
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	# Context data to render to page
	context = {'data':data,'credit':credit,'debit':debit,'total':credit-debit, 'page':page_obj}
	# To Add data
	if request.method=='POST':  # IF requested method is POST
		# Getting data from request
		income = request.POST['credit']
		expense = request.POST['debit']
		date = request.POST['date']
		desc = request.POST['description']
		# Assigning data to add
		data_save = Accounts(deposite = income, withdrawal = expense, description = desc, date = date)
		# Saving data
		data_save.save()
		# Rendering to desired page after saving with a success message
		messages.success(request, "Data Added Successfully")
		return HttpResponseRedirect('/adminf/accounts/')
	# Rendering to desired page with context data when Get request got
	return render(request,'AdminFunc/show_accounts.html',context)

# --------------------------------------------------------------------------------------------------------------------
# ----------------------------------Attendence Related Functionalities----------------------------

# To render attendence page
def Show_Attendance(request):
	class_obj = Classes.objects.all()
	emp_detail = Employee_Details.objects.all()
	stud_att = Student_Attendance.objects.all()
	teach_attend = Employee_Attendance.objects.all()
	PSA = 0
	ASA = 0
	LSA = 0
	PTA = 0
	ATA = 0
	LTA = 0
	for p in stud_att:
		if p.date == date.today():
			if p.status == 'P':
				PSA += 1
			elif p.status == 'A':
				ASA += 1
			elif p.status == 'L':
				LSA += 1
	for q in teach_attend:
		if q.date == date.today():
			if q.status == 'P':
				PTA += 1
			elif q.status == 'A':
				ATA += 1
			elif q.status == 'L':
				LTA += 1
	teaching = []
	non_teaching = []
	for i in emp_detail:
		if i.emp_type=='Teaching':
			teaching.append(i)
		else:
			non_teaching.append(i)
	Obj_id=[]
	if request.method=="POST":
		if request.POST['type'] == 'student':
			class_id = request.POST['class_id']
			class_data = Classes.objects.get(id = class_id)
			for i in class_data.student_details_set.all():
				Obj_id.append(i.id)
			for i in Obj_id:
				try:
					stud_obj = Student_Details.objects.get(id = request.POST['student'+str(i)])
					save_data = Student_Attendance(student = stud_obj, date = date.today(), status = request.POST['status'+str(i)])
					save_data.save()
				except:
					stud_obj = Student_Details.objects.get(id = request.POST['student'+str(i)])
					date_today = date.today()
					Student_Attendance.objects.filter(student = stud_obj).filter(date = date_today).update(status = request.POST['status'+str(i)])
		elif request.POST['type'] == 'employee':
			if request.POST['emptype']=='Teaching':
				for i in teaching:
					try:
						save_att = Employee_Attendance(employee=i,date=date.today(),status=request.POST['status'+str(i.id)])
						save_att.save()
					except:
						Employee_Attendance.objects.filter(employee=i.id).filter(date=date.today()).update(status=request.POST['status'+str(i.id)])
			if request.POST['emptype']=='Non-Teaching':
				for j in non_teaching:
					try:
						print(j.id)
						save_att = Employee_Attendance(employee=j,date=date.today(),status=request.POST['status'+str(j.id)])
						save_att.save()
					except Exception as e:
						print(e)
						Employee_Attendance.objects.filter(employee=j.id).filter(date=date.today()).update(status=request.POST['status'+str(j.id)])
		messages.success(request, "Attendance marked Successfully")
		return HttpResponseRedirect('/adminf/attendance/')
	context = {'classes':class_obj,'teaching':teaching,'non_teaching':non_teaching,'stud_attend':stud_att,'teach_attend':teach_attend}
	context.update({'PSA':PSA,'ASA':ASA,'LSA':LSA,'PTA':PTA,'ATA':ATA,'LTA':LTA,})
	return render(request,'AdminFunc/show_attendance.html',context)

# --------------------------------------------------------------------------------------------------------------------
# ----------------------------------Ajax Related Functionalities--------------------------------

# To validate username
def validate_username(request):
	uname = request.GET.get('username')
	data={ 'is_exist':User.objects.filter(username__iexact=uname).exists()}
	return JsonResponse(data)

# To validate email
def validate_email(request):
	email = request.GET.get('email')
	data={ 'is_exist':User.objects.filter(email__iexact=email).exists()}
	return JsonResponse(data)

# To validate Class name if available
def Delete_Classes(request):
	id_val = request.GET.get('id')
	data = Classes.objects.filter(id=id_val).delete()
	data_resp = {'resp': True}
	return JsonResponse(data_resp)

# To delete a subject via AJAX
def Delete_Subject(request):
	id_val = request.GET.get('id')
	data = Subjects.objects.filter(id=id_val).delete()
	data_resp = {'resp': True}
	return JsonResponse(data_resp)

# To validate class name if available
def Validate_Class_Name(request):
	name = request.GET.get('value')
	data={ 'is_exist':Classes.objects.filter(topic__iexact=name).exists()}
	return JsonResponse(data)