from django.contrib import admin
from .models import Requirement
from .models import Item
from .models import MakeSubmission
from .models import Group


# Register your models here.
admin.site.register(Requirement)
admin.site.register(Item)
admin.site.register(MakeSubmission)
admin.site.register(Group)
