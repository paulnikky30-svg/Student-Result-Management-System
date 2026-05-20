from django.db import models

class Semester(models.Model):
    semester_name = models.CharField(max_length=50)
    semester_code = models.CharField(max_length=50)
    academic_year = models.IntegerField(default=20)
    creation_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.semester_name} - {self.academic_year}"

class Subject(models.Model):
    subject_name = models.CharField(max_length=50)
    subject_code = models.CharField(max_length=50)
    academic_year = models.IntegerField(default=20)
    creation_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.subject_name} - {self.subject_code}"

class Students(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    name = models.CharField(max_length=50)
    roll_id = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    dob = models.CharField(max_length=100)
    reg_date = models.DateTimeField(auto_now_add=True)
    student_semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    reg_date_models = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def _str_(self):
        return self.name

class SubjectCombination(models.Model):
    student_semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    reg_date = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.student_semester} - {self.subject}"

class Result(models.Model):

    roll_id = models.CharField(max_length=100)

    course = models.CharField(max_length=200)

    subject = models.CharField(max_length=200)

    marks = models.IntegerField()

    def __str__(self):
        return self.roll_id

class Notice(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField()
    marks = models.IntegerField(null=True,blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    posting_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title