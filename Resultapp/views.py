from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Semester, Students # Apne models ka sahi naam yahan likhein
from Resultapp import views

def index(request):
    notices = Notice.objects.all().order_by('-id')
    return render(request, 'index.html',locals())

def notice_detail(request,notice_id):
    notice = get_object_or_404(Notice,id=notice_id)
    return render(request, 'notice_detail.html',locals())

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        if user is not None and user.is_superuser:
            login(request,user)
            return redirect('admin_dashboard')
        else:
          error= "Invalid crendentials or not authorized."
    return render(request, 'admin_login.html',locals())

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    return render(request,'admin_dashboard.html')

def admin_logout(request):
    logout(request)
    return redirect('admin-login')


@login_required
def create_semester(request):
    if request.method == 'POST':
        try:
            semester_name = request.POST.get('semestername')
            semester_code = request.POST.get('semestercode')
            academic_year = request.POST.get('academicyear')
            Semester.objects.create(semester_name=semester_name,semester_code=semester_code,academic_year=academic_year)
            messages.success(request," Semester Created Successfully")
            return redirect('create_semester')
        except Exception as e:

            messages.error(request,f"Something went wrong: {str(e)}")
            return redirect('create_semester')
    return render(request,'create_semester.html')

from django.shortcuts import get_object_or_404

@login_required
def manage_semesters(request):
  semesters = Semester.objects.all()

  if request.GET.get('delete'):
        try:
           semester_id = request.GET.get('delete')
           semester_obj = get_object_or_404(Semester,id=semester_id)
           semester_obj.delete()
           messages.success(request,"Semester deleted successfully!!")
           return redirect('manage_semesters')
        except Exception as e:
            messages.error(request,f"Something went wrong:{str(e)}")
            return redirect('manage_semesters')
  return render(request,'manage_semesters.html',locals())


@login_required
def create_subject(request):
    if request.method == 'POST':
        try:
            subject_name = request.POST.get('subjectname')
            subject_code = request.POST.get('subjectcode')
            Subject.objects.create(subject_name = subject_name,subject_code=subject_code)
            messages.success(request," Subject Created Successfully")
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
        return redirect('create_subject')
    return render(request,'create_subject.html')


@login_required
def manage_subject(request):
  subjects = Subject.objects.all()

  if request.GET.get('delete'):
        try:
           subject_id = request.GET.get('delete')
           subject_obj = get_object_or_404(Subject,id=subject_id)
           subject_obj.delete()
           messages.success(request,"Subject deleted successfully!!")
        except Exception as e:
            messages.error(request,f"Something went wrong:{str(e)}")
        return redirect('manage_subject')
  return render(request,'manage_subject.html',locals())


def add_student(request):
    # Semester dropdown ke liye data fetch karna
    semesters = Semester.objects.all()

    if request.method == 'POST':
        # Form se data nikalna (HTML ke 'name' attribute se)
        f_name = request.POST.get('full_name')
        f_roll = request.POST.get('roll_id')
        f_email = request.POST.get('email')
        f_gender = request.POST.get('gender')
        f_dob = request.POST.get('dob')
        f_semester_id = request.POST.get('semester')

        try:
            # Foreign Key object nikalna
            semester_obj = Semester.objects.get(id=f_semester_id)
            
            # Database mein save karna (Models.py ke fields use kiye hain)
            student = Students(
                name = f_name,               # Models.py mein 'name' hai
                roll_id = f_roll,
                email = f_email,
                gender = f_gender,
                dob = f_dob,
                student_semester = semester_obj # Models.py mein 'student_semester' hai
            )
            student.save()

            messages.success(request, "Student Info Added Successfully!")
            return redirect('add_student')

        except Exception as e:
            messages.error(request, f"Error: {e}")

    context = {
        'semester': semesters,
    }
    return render(request, 'add_student.html', context)

# --- URLS.PY KA ERROR HATANE KE LIYE YE FUNCTIONS ZAROORI HAIN ---

def edit_subject(request, subject_id):
    # Terminal mein jo 'edit_subject' error tha wo isse solve ho jayega
    return render(request, 'edit_subject.html')

def manage_subject(request):
    return render(request, 'manage_subject.html')

def create_subject(request):
    return render(request, 'create_subject.html')


@login_required
def manage_students(request):
    # 1. Database se saare students ka data fetch kiya
    students = Students.objects.all()

    # 2. Student Delete karne ka logic
    if request.GET.get('delete'):
        try:
            student_id = request.GET.get('delete')
            student_obj = get_object_or_404(Students, id=student_id) # 👈 Spelling thik kar di hai
            student_obj.delete()
            messages.success(request, "Student deleted successfully!!")
            return redirect('manage_students') 
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('manage_students')

    # 3. HTML template ko data sahi variable ke sath bhej rahe hain
    return render(request, 'manage_students.html', {'students': students})       


@login_required
def edit_student(request, student_id):
    student_obj = get_object_or_404(Students, id=student_id)
    semester=Semester.objects.all()
    if request.method == 'POST':
        try:
            student_obj.name = request.POST.get('fullname')
            student_obj.roll_id = request.POST.get('rollid')
            student_obj.email = request.POST.get('emailid')
            student_obj.gender = request.POST.get('gender')
            student_obj.dob = request.POST.get('dob')
            student_obj.status = request.POST.get('status')
            student_obj.save()
            messages.success(request, "Student updated successfully!")
            return redirect('manage_students') # Yahan try ke andar hi redirect rakhna sahi rahega taaki success pe redirect ho jaye
            
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('manage_students')

    # 4 spaces ka gap (def ke andar, par if ke bahar)
    return render(request, 'edit_student.html', locals())


@login_required
def add_notice(request):
    if request.method == 'POST':
        try:
           title = request.POST.get('title')
           details = request.POST.get('details')

           Notice.objects.create(title=title,detail=details)
           messages.success(request, "Notice  Added Successfully!")
           return redirect('add_notice')
        except Exception as e:
            messages.error(request,f"Something went wrong: {str(e)}")
    return render(request, 'add_notice.html')


@login_required
def manage_notice(request):
  notices = Notice.objects.all()

  if request.GET.get('delete'):
        try:
           notice_id = request.GET.get('delete')
           notice_obj = get_object_or_404(Notice, id=notice_id)
           notice_obj.delete()
           messages.success(request,"Notice deleted successfully!!")
        except Exception as e:
            messages.error(request,f"Something went wrong:{str(e)}")
        return redirect('manage_notice')
  return render(request,'manage_notice.html',locals())



def add_result(request):

    results = None

    if request.method == "POST":

        roll = request.POST.get('roll')
        course = request.POST.get('course')

        results = Result.objects.filter(
            roll_id=roll,
            course=course
        )

    return render(request, 'add_result.html', {
        'results': results
    })

def check_result(request):
    results = Result.objects.all()
    return render(request, 'check_result.html', {'results':results})