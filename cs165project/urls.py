"""cs165project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from online_submission import views 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base_page, name='base_page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/admin', views.signup, name='signup'),
    path('signup/success', views.signup_success, name='signup_success'),
    path('home', views.home_page, name='home_page'),
    path('requirements/', views.requirement_list, name='requirement_list'),
    path('requirements/create', views.create_requirement, name='create_requirement'),
    path('requirement/<int:req_ID>/update', views.update_requirement, name='update_requirement'),
    path('requirement/<int:req_ID>/delete', views.delete_requirement, name='delete_requirement'),
    path('requirement/<int:req_ID>/item_list', views.item_list, name='item_list'),
    path('requirement/<int:req_ID>/create/item', views.create_item, name='create_item'),
    path('requirement/<int:req_ID>/<int:item_no>/edit', views.update_item, name='update_item'),
    path('requirement/<int:req_ID>/<int:item_no>/delete', views.delete_item, name='delete_item'),
    path('requirement/<int:req_ID>/<int:item_no>/', views.item_view, name='item_view'),
    path('requirement/<int:req_ID>/<int:item_no>/submit', views.item_submit, name='item_submit'),
    path('requirement/<int:req_ID>/<int:item_no>/submission/delete', views.delete_submission, name='delete_submission'),
    path('requirement/view_grades', views.grades_view, name='grades_view'),
    path('students', views.student_list, name='student_list'),
    path('students/create', views.create_student, name='create_student')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
