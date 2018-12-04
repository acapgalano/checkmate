from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	is_student = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False) 

class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	student_no = models.CharField(max_length=10)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	email = models.EmailField()

class Admin(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	email = models.EmailField()

class Requirement(models.Model):
	#reg_ID --> auto increment
	req_name = models.CharField(max_length=20)
	total_score = models.IntegerField()
	deadline = models.DateTimeField(auto_now=False, auto_now_add=False)

# delete: SomeModel.objects.filter(id=id).delete()

def item_input_test(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<requirement's name>/<item number>/input
    return '{req}/{item}/input/{file}'.format(req=instance.requirement.req_name, item=instance.item_no, file=filename)

def item_output_test(instance, filename):
	# file will be uploaded to MEDIA_ROOT/<requirement's name>/<item number>/output
	return '{req}/{item}/output/{file}'.format(req=instance.requirement.req_name, item=instance.item_no, file=filename)

class Item(models.Model):
	# (new) item_ID --> auto  increment
	class Meta: 
		unique_together = (('requirement', 'item_no'),)

	requirement = models.ForeignKey('Requirement', on_delete=models.CASCADE)
	item_no = models.IntegerField() #admin bahala default = current_item_no
	test_input_file = models.FileField(upload_to=item_input_test, null=True, blank=True)
	test_output_file = models.FileField(upload_to=item_output_test, null=True, blank=True)
	score = models.IntegerField()

	def get_score(self): 
		return self.score 

def submission_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/
    return '{req}/{item}/{user}/{filename}'.format(req=instance.requirement.req_name, item=instance.item_no, user=instance.user_ID.id, filename=filename)

class MakeSubmission(models.Model):
	#submission_ID --> auto increment
	user_ID = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	requirement = models.ForeignKey('Requirement', on_delete=models.CASCADE)
	item_no =  models.IntegerField()
	timestamp = models.DateTimeField(auto_now=True) #for future implementation: edititng submissions
	file = models.FileField(upload_to=submission_path, null = True)
	grade = models.IntegerField(default = 0)

class Group(models.Model):
	#group_ID --> auto increment
	group_name = models.CharField(max_length = 20)
	students = models.ManyToManyField(get_user_model(), blank=True)

#class CanBePartOf(models.Model):
#	user_ID = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#	group_ID =  models.ForeignKey('Groups', on_delete=models.CASCADE)

