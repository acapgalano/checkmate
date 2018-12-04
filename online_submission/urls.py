from django.urls import path
from . import views

urlpatterns = [
	path('admin/', admin.site.urls)
    path(r'^requirements', views.requirement_list, name='requirement_list'),
]