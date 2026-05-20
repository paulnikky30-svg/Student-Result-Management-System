"""
URL configuration for studentresultmanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path , include
from Resultapp.views import * 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index , name='home'),
    path('admin-login/',admin_login , name='admin-login'),
    path('admin_dashboard/',admin_dashboard , name='admin_dashboard'),
    path('create_semester/',create_semester , name='create_semester'),
    path('admin_logout/',admin_logout, name='admin_logout'),
    path('manage_semesters/',manage_semesters, name='manage_semesters'),
    path('create_subject/',create_subject , name='create_subject'),
    path('manage_subject/',manage_subject, name='manage_subject'),
    path('edit_subject/<int:subject_id>/',edit_subject, name='edit_subject'),
    path('add_student/',add_student, name='add_student'),
    path('manage_students/',manage_students, name='manage_students'),
    path('edit_student/<int:student_id>/',edit_student, name='edit_student'),
    path('add_notice/',add_notice, name='add_notice'),
    path('manage_notice/',manage_notice, name='manage_notice'),
    path('add_result/', views.add_result, name='add_result'),
    path('check_result/', views.check_result, name='check_result'),
    path('notice_detail/<int:notice_id>/', notice_detail, name='notice_detail'),
]
