# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
""" 

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
 """


class Exam(models.Model):
    exam_code = models.CharField(primary_key=True, max_length=32)
    exam_date = models.DateField(blank=True, null=True)
    exam_duration = models.IntegerField(blank=True, null=True)
    question_count = models.IntegerField(blank=True, null=True)
    subject_code = models.ForeignKey(
        'Subject', models.DO_NOTHING, db_column='subject_code', blank=True, null=True)

    def __str__(self):
        return self.exam_code


class Questions(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=512, blank=True, null=True)
    option_a = models.CharField(max_length=128, blank=True, null=True)
    option_b = models.CharField(max_length=128, blank=True, null=True)
    option_c = models.CharField(max_length=128, blank=True, null=True)
    option_d = models.CharField(max_length=128, blank=True, null=True)
    correct_answer = models.CharField(max_length=20, blank=True, null=True)
    subject_code = models.ForeignKey(
        'Subject', models.DO_NOTHING, db_column='subject_code', blank=True, null=True)

    def __int__(self):
        return self.question_id


class Student(models.Model):
    profile = models.ImageField(upload_to="images")
    name = models.CharField(max_length=32)
    email = models.EmailField(max_length=40, primary_key=True)
    phone = models.BigIntegerField()
    branch = models.CharField(max_length=50)
    year = models.CharField(max_length=20)
    pwd = models.CharField(max_length=20)

    def __str__(self):
        return self.email


class Subject(models.Model):
    subject_code = models.CharField(primary_key=True, max_length=32)
    subject_name = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.subject_code


class department(models.Model):
    department_code = models.CharField(primary_key=True, max_length=20)
    department_name = models.CharField(max_length=50)

    def __str__(self):
        return self.department_code


class faculty(models.Model):
    profile = models.ImageField(upload_to="images")
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40, primary_key=True)
    phone = models.BigIntegerField()
    pwd = models.CharField(max_length=20)

    def __str__(self):
        return self.email


class contact(models.Model):
    email = models.EmailField(max_length=40)
    phone = models.BigIntegerField()
    query = models.CharField(max_length=128)

    def __str__(self):
        return self.email


class result(models.Model):
    email = models.ForeignKey(
        'Student', models.DO_NOTHING, db_column='email', blank=True, null=False)
    exam_code = models.ForeignKey(
        "Exam", models.DO_NOTHING, db_column="exam_code", blank=True, null=False)
    marks = models.IntegerField()

    def __int__(self):
        return self.email
