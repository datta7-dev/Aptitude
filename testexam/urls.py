from django.urls import path
from testexam import views

urlpatterns = [
    #path("practicepaper", views.practice_paper, name="practicepaper"),
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("logout", views.logout_user, name="logout"),
    path("facultylogin", views.faculty_login, name="facultylogin"),
    path("facultyhome", views.faculty_home, name="facultyhome"),
    path("studentregistration", views.student_register,
         name="studentregistration"),
    path("studentlogin", views.student_login, name="studentlogin"),
    path("studenthome", views.student_home, name="studenthome"),
    path("adddepartment", views.add_department, name="adddepartment"),
    path("addquestion", views.add_question, name="addquestion"),
    path("addsubject", views.add_subject, name="addsubject"),
    path("addquestion", views.add_question, name="addquestion"),
    path("exampaper", views.exam_paper, name="exampaper"),
    path("subjectlist", views.subject_list, name="subjectlist"),
    path("addexam", views.add_exam, name="examlist"),
    path("examlist", views.exam_list, name="examlist"),
    path("examliststudent", views.examlist_student, name="examliststudent"),
    path("exampaper", views.exam_paper, name="exampaper"),
    path("papercheck", views.paper_check, name="papercheck"),
    path("editexam", views.delete_exam, name="editexam"),
    path("practicetest", views.practice_test, name="practicetest"),
    path("practicepaper", views.practice_paper, name="practicepaper"),
    path("about", views.about_us, name="about"),
    path("contact", views.contact_us, name="contact"),
    path("result", views.result_list, name="result")
]
