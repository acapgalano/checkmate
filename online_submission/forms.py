from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
import datetime

from .models import Requirement, Item, MakeSubmission, User

class AdminSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = True
        if commit:
            user.save()
        return user

class CreateStudentForm(forms.Form):
	student_no = forms.CharField(max_length=10)
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)
	email = forms.EmailField()

class CreateRequirementForm(forms.ModelForm):
	deadline_date = forms.DateField()
	deadline_time = forms.TimeField()

	class Meta: 
		model = Requirement
		fields = ('req_name', 'total_score', 'deadline_date', 'deadline_time',)

	def __init__(self, *args, **kwargs):
		super(CreateRequirementForm, self).__init__(*args, **kwargs)
		if 'instance' in kwargs:
			self.fields['deadline_date'].initial = kwargs['instance'].deadline.date()
			self.fields['deadline_time'].initial = kwargs['instance'].deadline.time()

	def save(self, commit=True):
		model = super(CreateRequirementForm, self).save(commit=False)
		model.deadline = datetime.datetime.combine(self.cleaned_data['deadline_date'], self.cleaned_data['deadline_time'])
		if commit:
			model.save()
		return model


class UpdateRequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ('req_name','total_score','deadline',)

class CreateItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('test_input_file', 'test_output_file', 'score',)

class UpdateItemForm(forms.ModelForm):
	class Meta: 
		model = Item
		fields = ('test_input_file','test_output_file','score',)

class SubmissionForm(forms.ModelForm):
	class Meta:
		model = MakeSubmission
		fields = ('file',)

	
