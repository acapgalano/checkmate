from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.urls import reverse

from .models import Requirement, Item, User, Student, MakeSubmission
from .forms import SubmissionForm, AdminSignUpForm, CreateRequirementForm, CreateItemForm, CreateStudentForm, UpdateRequirementForm, UpdateItemForm

def base_page(request):
	return render(request, 'online_submission/base_page.html', {})


def signup(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():

            form.save()
            #messages.success(request, 'Account created successfully') #from django.contrib import messages
            return redirect(reverse('signup_success'))

    else:
        form = AdminSignUpForm()
    return render(request, 'online_submission/admin_signup.html', {'form': form})

def signup_success(request):
	return render(request, 'online_submission/signup_success.html', {})


def home_page(request):
	print(request.user.is_authenticated)
	if request.user.is_authenticated:
		if request.user.is_admin: 
			return render(request, 'online_submission/home_page_admin.html', {})
		else: 
			current_user = get_object_or_404(Student, user=request.user)
			return render(request, 'online_submission/home_page.html', {'current_user': current_user})
	else:
		return redirect(reverse('base_page'))
	#if request.user.is_authenticated():
	#	return render(request, 'online_submission/home_page.html', {'current_user': current_user})
	#else:
	#	return render(request, 'online_submission/page_block.html', {'current_user': current_user})

def student_list(request):
	if request.user.is_authenticated:
		if request.user.is_admin:
			students = Student.objects.order_by('last_name')
			return render(request, 'online_submission/student_list.html', {'students':students})
		else: 
			return render(request, 'online_submission/page_block.html', {})
	else:
		return render(request, 'online_submission/page_block.html', {})

def create_student(request):
	if request.user.is_authenticated:
		if request.user.is_admin:
			if request.method == 'POST':
				form = CreateStudentForm(request.POST)
				if form.is_valid():
					username = "".join([name[0] for name in form.cleaned_data["first_name"].split()] + [form.cleaned_data["last_name"]])
					password = form.cleaned_data["last_name"].lower() + form.cleaned_data["student_no"].split('-')[1]
					user = User(username=username.lower())
					user.set_password(password)
					user.is_student = True
					user.save()
					student = Student(user=user, student_no=form.cleaned_data["student_no"], 
						first_name=form.cleaned_data["first_name"], 
						last_name=form.cleaned_data["last_name"], 
						email=form.cleaned_data["email"])
					student.save()
					return redirect(reverse('student_list'))
			else:
				form = CreateStudentForm()
			return render(request, 'online_submission/student_create.html', {'form': form})
		else:
			return render(request, 'online_submission/page_block.html', {})
	else:
		return render(request, 'online_submission/page_block.html', {})

def requirement_list(request):
	if request.user.is_authenticated:
		requirements = Requirement.objects.order_by('deadline')
		if request.user.is_admin:
			return render(request,'online_submission/requirement_list_admin.html', {'requirements': requirements})
		else:
			return render(request, 'online_submission/requirement_list.html', {'requirements': requirements})
	else:
		return render(request, 'online_submission/page_block.html', {})

def create_requirement(request):
	if request.user.is_authenticated and request.user.is_admin:
		form = CreateRequirementForm()

		if request.method == 'POST':
			form = CreateRequirementForm(request.POST)
			if form.is_valid():
				#submission = form.save(commit=False)
				form.save()
			else:
				print(form.errors)
			return redirect(reverse('requirement_list'))
		else:
			form = CreateRequirementForm()
			return render(request, 'online_submission/requirement_create_form.html', {'form': form}) 
	else: 
		return render(request, 'online_submission/page_block.html', {})

def update_requirement(request, req_ID):
	if request.user.is_authenticated and request.user.is_admin:
		requirement = get_object_or_404(Requirement, id=req_ID)
		form = UpdateRequirementForm(request.POST or None, instance=requirement)
		if form.is_valid():
			form.save()
			return redirect(reverse('item_list', args=[req_ID]))
		return render(request, 'online_submission/requirement_update.html', {'form':form, 'requirement':requirement})
	else:
		return render(request, 'online_submission/page_block.html', {})

def delete_requirement(request, req_ID):
	if request.user.is_authenticated and request.user.is_admin:
		Requirement.objects.filter(id=req_ID).delete()
		return redirect(reverse('requirement_list'))
	else:
		return render(request, 'online_submission/page_block.html', {})

def item_list(request, req_ID):
	if request.user.is_authenticated:
		requirement = get_object_or_404(Requirement, id=req_ID)
		items = Item.objects.filter(requirement=requirement)
		if request.user.is_admin: 
			return render(request, 'online_submission/item_list_admin.html', {'items': items, 'requirement': requirement})
		else:
			return render(request, 'online_submission/item_list.html', {'items': items, 'requirement': requirement})
	else:
		return render(request, 'online_submission/page_block.html', {})

def create_item(request, req_ID):
	if request.user.is_authenticated and request.user.is_admin: 
		form = CreateItemForm()
		requirement = get_object_or_404(Requirement, id=req_ID)
		items = Item.objects.filter(requirement=requirement)
		item_no = len(items)+1 

		if request.method == 'POST':
			form = CreateItemForm(request.POST, request.FILES)
			if form.is_valid():
				item = form.save(commit=False)
				item.requirement = requirement
				item.item_no = item_no
				item.save()
			else: 
				print(form.errors) 
			return redirect(reverse('item_list', args=[requirement.id]))
		else: 
			form = CreateItemForm()
			return render(request, 'online_submission/item_create.html', {'form': form, 'requirement': requirement})
	else:
		return render(request, 'online_submission/page_block.html', {})

def update_item(request, req_ID, item_no):
	requirement = get_object_or_404(Requirement, id=req_ID)
	item = get_object_or_404(Item, requirement=requirement, item_no=item_no)
	form = UpdateItemForm(request.POST or None, request.FILES or None, instance=item)
	if form.is_valid():
		form.save()
		return redirect(reverse('item_view', args=[req_ID, item_no]))
	return render(request, 'online_submission/item_update.html', {'form':form, 'requirement':requirement, 'item':item})

def delete_item(request, req_ID, item_no):
	requirement = get_object_or_404(Requirement, id=req_ID)
	Item.objects.filter(requirement=requirement, item_no=item_no).delete()
	return redirect(reverse('item_list', args=[requirement.id])) 


def item_view(request, req_ID, item_no):
	requirement = get_object_or_404(Requirement, id=req_ID)
	item = get_object_or_404(Item, requirement=requirement, item_no=item_no)
	if request.user.is_admin:
		return render(request, 'online_submission/item_view.html', {'requirement':requirement, 'item': item})
	else: 
		submissions = MakeSubmission.objects.filter(requirement=requirement, item_no=item_no) 
		return render(request, 'online_submission/item_view_student.html', {'requirement':requirement, 'item': item, 'submissions':submissions})


def item_submit(request, req_ID, item_no):
	form = SubmissionForm()
	requirement = get_object_or_404(Requirement, id=req_ID)

	if request.method == 'POST':
		form = SubmissionForm(request.POST, request.FILES or None)
		print(request.FILES)
		if form.is_valid():
			submission = form.save(commit=False)
			submission.requirement = requirement
			submission.item_no = item_no
			submission.timestamp = timezone.now()
			submission.user_ID = request.user;
			submission.save()
		else:
			print(form.errors)
		return redirect(reverse('item_list', args=[requirement.id]))
	else:
		form = SubmissionForm()
		return render(request, 'online_submission/item_submit.html', {'form': form, 'requirement':requirement, 'item_no': item_no})

def delete_submission(request, req_ID, item_no):
	requirement = get_object_or_404(Requirement, id=req_ID)
	Item.objects.filter(requirement=requirement, item_no=item_no)
	MakeSubmission.objects.filter(user_ID=request.user, requirement=requirement, item_no=item_no).delete()
	return redirect(reverse('item_list', args=[requirement.id]))

def grades_view(request):
	if request.user.is_authenticated:
		if request.user.is_admin:
			print("Not yet implemented.")
			return redirect(reverse('home_page'))
		else: 
			user = request.user
			submissions = MakeSubmission.objects.filter(user_ID=request.user)
			requirements = Requirement.objects.all() 
			grades = []

			for requirement in requirements:
				sum = 0
				for submission in MakeSubmission.objects.filter(requirement=requirement):
					sum += submission.grade
				grades.append({'requirement': requirement.req_name, 'score': sum})
			return render(request, 'online_submission/grades_view.html', {'grades': grades})

