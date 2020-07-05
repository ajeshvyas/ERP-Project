from django.urls import path
from AdminFunc import views

urlpatterns = [
	path('home/',views.AdminHome),
	path('new_student/',views.Add_Student),
	path('show_students/',views.Show_Students),
	path('validate_username/',views.validate_username),
	path('validate_email/',views.validate_email),
	path('new_employee/',views.Add_Employee),
	path('show_employees/',views.Show_Employees),
	path('show_classes/',views.Show_classes),
	path('add_class/',views.Add_Classes),
	path('edit_class/<id>/',views.Edit_Classes),
	path('delete_class/',views.Delete_Classes),
	path('add_subjects/<id>/',views.Add_Subjects),
	path('edit_subjects/<id>/',views.Edit_Subjects),
	path('profile_student/<id>/',views.Profile_Student),
	path('delete_student/<id>/',views.Delete_Student),
	path('institute_info/',views.Institute_info),
	path('student_academics/',views.Academic_Details),
	path('validate_class_name/',views.Validate_Class_Name),
	path('delete_subject/',views.Delete_Subject),
	path('view_employee/',views.View_Employees),
	path('edit_employee/<id>/',views.Edit_Employee),
	path('delete_employee/<id>/',views.Delete_Employee),
	path('accounts/',views.Show_Accounts),
]