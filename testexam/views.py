from django.shortcuts import render, HttpResponse, redirect
from testexam.models import Questions, Subject, Exam, department, faculty, Student, contact, result
from django.views.generic import View
# Create your views here.


# To get the index/landing page
def index(request):
    if request.method == "GET":
        from django.db import connection
        cursor = connection.cursor()
        query = ("select * from testexam_department")
        cursor.execute(query)
        result_data = cursor.fetchall()
        department_code = []
        department_name = []
        for data in result_data:
            department_code.append(data[0])
            department_name.append(data[1])
        department_data = {
            "department_code": department_code,
            "department_name": department_name
        }
        cursor.close()
        connection.close()
        return render(request, "index.html", department_data)
    elif request.method == "POST":
        return render(request, "index.html")


# to logout and destroy the session
def logout_user(request):
    try:
        if request.method == "GET":
            if request.session.get("user") != None:
                del request.session["user"]
                return redirect("index")
            else:
                return redirect("index")
        elif request.method == "POST":
            return redirect("index")
    except Exception as e:
        print(e)


# for faculty login form page
def faculty_login(request):
    return render(request, "facultylogin.html")


# To authenticate faculty after click on faculty login
# if faculty present in database then open faculty home page for faculty
def faculty_home(request):
    if request.method == "POST":
        u = request.POST["username"]
        p = request.POST["password"]
        from django.db import connection
        cursor = connection.cursor()
        query = ("select email,pwd from testexam_faculty")
        cursor.execute(query)
        faculty_data = cursor.fetchall()
        cursor.close()
        connection.close()
        flag = 0
        for data in faculty_data:
            if u == data[0] and p == data[1]:
                flag = 1
                break
            else:
                flag = 0
        # print(flag)
        if flag == 1:
            request.session["user"] = u
            # print(request.session.get('user'))
            user_data = faculty.objects.filter(
                email=request.session.get("user"))
            for user in user_data:
                user_name = user.name
                profile = user.profile.url
            exam_data = {
                "exam": Exam.objects.all(),
                "user_name": user_name,
                "profile": profile,
            }
            # at faculty home page to show featured exams by default
            return render(request, "examlist.html", exam_data)
            # return render(request, "facultyhome.html")
        else:
            return redirect("/facultylogin")
    elif request.method == "GET":
        return redirect("/facultylogin")


# To register new student
def student_register(request):
    if request.method == "POST":
        profile = request.FILES["profile"]
        student_name = request.POST["stud_name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        branch = request.POST["branch"]
        year = request.POST["year"]
        pwd1 = request.POST["pwd1"]
        pwd2 = request.POST["pwd2"]
        if pwd1 != pwd2:
            return redirect("/index")
        s = Student(profile=profile, name=student_name,
                    email=email, phone=phone, branch=branch, year=year, pwd=pwd1)
        s.save()
        from django.db import connection
        cursor = connection.cursor()
        query = ("select * from testexam_department")
        cursor.execute(query)
        result_data = cursor.fetchall()
        cursor.close()
        connection.close()
        department_code = []
        department_name = []
        for data in result_data:
            department_code.append(data[0])
            department_name.append(data[1])
        department_data = {
            "department_code": department_code,
            "department_name": department_name,
            "success": "Registered Successfully",
        }
        return render(request, "index.html", department_data)
    elif request.method == "GET":
        return redirect("/index")


# for student login form page
def student_login(request):
    return render(request, "studentlogin.html")


# To authenticate student after click on student login
# if student present in database then open student home page for the student
def student_home(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        student_data = Student.objects.all()
        flag = 0
        for data in student_data:
            if username == data.email and password == data.pwd:
                flag = 1
                break
            else:
                flag = 0
        if flag == 1:
            request.session['user'] = username
            # print(request.session.get('user'))
            user_data = Student.objects.filter(
                email=request.session.get('user'))
            for user in user_data:
                user_name = user.name
                profile = user.profile.url
            exam_data = {
                "exam": Exam.objects.all(),
                'user_name': user_name,
                'profile': profile,
                "user_name": user_name,
            }
            # at student home page to show featured exams by default
            return render(request, "examliststudent.html", exam_data)
            # return render(request, "studenthome.html", users)
        else:
            return render(request, "studentlogin.html")
    elif request.method == "GET":
        return redirect("/studentlogin")


# To add new department by faculty
def add_department(request):
    try:
        if request.method == "GET":
            if request.session.get("user") != None:
                user_data = faculty.objects.filter(
                    email=request.session.get("user"))
                for user in user_data:
                    user_name = user.name
                    profile = user.profile.url
                user_data = {
                    "user_name": user_name,
                    "profile": profile,
                }
                return render(request, "adddepartment.html", user_data)
            else:
                return redirect("facultylogin")
        elif request.method == "POST":
            if request.session.get("user") != None:
                department_name = request.POST["dept_name"]
                department_code = request.POST["dept_code"]
                k = department.objects.all()
                flag = 0
                for key in k:
                    if department_code == key.department_code or department_name == key.department_name:
                        flag = 1
                        break
                    else:
                        flag = 0
                if flag == 1:
                    user_data = faculty.objects.filter(
                        email=request.session.get("user"))
                    for user in user_data:
                        user_name = user.name
                        profile = user.profile.url
                    msg1 = {
                        "failed": "failed to add department",
                        "user_name": user_name,
                        "profile": profile,
                    }
                    return render(request, "adddepartment.html", msg1)
                else:
                    t = department(department_name=department_name,
                                   department_code=department_code)
                    t.save()
                    user_data = faculty.objects.filter(
                        email=request.session.get("user"))
                    for user in user_data:
                        user_name = user.name
                        profile = user.profile.url
                    msg = {
                        "success": "department added",
                        "user_name": user_name,
                        "profile": profile,
                    }
                    return render(request, "adddepartment.html", msg)
    except Exception as e:
        print(e)


# To add the new subject into the database by faculty
def add_subject(request):
    try:
        if request.method == "GET":
            if request.session.get("user") != None:
                user_data = faculty.objects.filter(
                    email=request.session.get("user"))
                for user in user_data:
                    user_name = user.name
                    profile = user.profile.url
                    user_data = {
                        "user_name": user_name,
                        "profile": profile,
                    }
                return render(request, "addsubject.html", user_data)
            else:
                return redirect("facultylogin")
        elif request.method == "POST":
            from django.db import connection
            with connection.cursor() as cursor:
                subject_code = request.POST.get("sub_code")
                subject_name = request.POST.get("sub_name")
                query = ("insert into testexam_subject values(%s,%s)")
                values = (subject_code, subject_name)
                cursor.execute(query, values)
                cursor.close()
                connection.close()
                user_data = faculty.objects.filter(
                    email=request.session.get("user"))
                for user in user_data:
                    user_name = user.name
                    profile = user.profile.url
                msg = {
                    "success": "subject added...",
                    "user_name": user_name,
                    "profile": profile,
                }
                return render(request, "addsubject.html", msg)
    except Exception as e:
        print(e)


# To get the subjects list from the database
def subject_list(request):
    from django.db import connection
    # with connection.cursor() as cursor:
    cursor = connection.cursor()
    query = ("select * from testexam_subject")
    cursor.execute(query)
    result_data = cursor.fetchall()
    """ for data in result_data:
        print(result_data) """
    cursor.close()
    connection.close()
    return HttpResponse("<h1>query executed successfully</h1>")
    # return render(request, "display.html")


# To add new questions into the database by faculty
def add_question(request):
    try:
        if request.method == "GET":
            if request.session.get("user") != None:
                user_data = faculty.objects.filter(
                    email=request.session.get("user"))
                for user in user_data:
                    user_name = user.name
                    profile = user.profile.url
                subjects = {
                    "sub": Subject.objects.all(),
                    "user_name": user_name,
                    "profile": profile,
                }
                return render(request, "addquestion.html", subjects)
            else:
                return redirect("facultylogin")
        elif request.method == "POST":
            from django.db import connection
            cursor = connection.cursor()
            question = request.POST.get("question")
            option_a = request.POST.get("option_a")
            option_b = request.POST.get("option_b")
            option_c = request.POST.get("option_c")
            option_d = request.POST.get("option_d")
            correct_option = request.POST.get("correct_option")
            subject_code = request.POST.get("sub_code")
            insert_data = (question, option_a, option_b, option_c,
                           option_d, correct_option, subject_code)
            query = "insert into testexam_questions(question, option_a, option_b, option_c, option_d, correct_answer, subject_code)values( % s, % s, % s, % s, % s, % s, % s)"
            cursor.execute(query, insert_data)
            cursor.close()
            connection.close()
            user_data = faculty.objects.filter(
                email=request.session.get("user"))
            for user in user_data:
                user_name = user.name
                profile = user.profile.url
            context_data = {
                "sub": Subject.objects.all(),
                "success": " question added",
                "user_name": user_name,
                "profile": profile,
            }
            return render(request, "addquestion.html", context_data)
    except Exception as e:
        print(e)


# To add new exam into the database by faculty
def add_exam(request):
    try:
        if request.method == "GET":
            if request.session.get("user") != None:
                from django.db import connection
                cursor = connection.cursor()
                query = ("select * from testexam_subject")
                cursor.execute(query)
                result_data = cursor.fetchall()
                cursor.close()
                connection.close()
                sub_code_list = []
                sub_name_list = []
                for d in result_data:
                    sub_code_list.append(d[0])
                    sub_name_list.append(d[1])
                user_data = faculty.objects.filter(
                    email=request.session.get("user"))
                for user in user_data:
                    user_name = user.name
                    profile = user.profile.url
                subjects = {
                    "subject_code": sub_code_list,
                    "subject_name": sub_name_list,
                    "user_name": user_name,
                    "profile": profile,
                }
                return render(request, "addexam.html", subjects)
            else:
                return redirect("facultylogin")
        elif request.method == "POST":
            exam_code = request.POST["exam_code"]
            exam_date = request.POST["exam_date"]
            exam_duration = request.POST["exam_duration"]
            no_of_questions = request.POST["n_questions"]
            subject_code = request.POST["subject_code"]
            values = (exam_code, exam_date, exam_duration,
                      no_of_questions, subject_code)
            # print(values)
            from django.db import connection
            cursor = connection.cursor()
            query = (
                "insert into testexam_exam(exam_code,exam_date,exam_duration,question_count,subject_code)values(%s,%s,%s,%s,%s)")
            # cursor.execute(query, values)
            return_data = cursor.execute(query, values)
            if return_data is not None:
                # return redirect("/addexam")
                query = ("select * from testexam_subject")
                cursor.execute(query)
                result_data = cursor.fetchall()
                cursor.close()
                connection.close()
                sub_code_list = []
                sub_name_list = []
                for d in result_data:
                    sub_code_list.append(d[0])
                    sub_name_list.append(d[1])
                user_data = faculty.objects.filter(
                    email=request.session.get("user"))
                for user in user_data:
                    user_name = user.name
                    profile = user.profile.url
                subjects = {
                    "subject_code": sub_code_list,
                    "subject_name": sub_name_list,
                    "success": "exam added successfully",
                    "user_name": user_name,
                    "profile": profile,
                }
                return render(request, "addexam.html", subjects)
            else:
                query = ("select * from testexam_subject")
                cursor.execute(query)
                result_data = cursor.fetchall()
                cursor.close()
                connection.close()
                sub_code_list = []
                sub_name_list = []
                for d in result_data:
                    sub_code_list.append(d[0])
                    sub_name_list.append(d[1])
                user_data = faculty.objects.filter(
                    email=request.session.get("user"))
                for user in user_data:
                    user_name = user.name
                    profile = user.profile.url
                subjects = {
                    "subject_code": sub_code_list,
                    "subject_name": sub_name_list,
                    "failed": "failed to add exam",
                    "user_name": user_name,
                }
                return render(request, "addexam.html", subjects)
    except Exception as e:
        print(e)


# To get the examlist for faculty
def exam_list(request):
    try:
        if request.method == "GET":
            if request.session.get("user") != None:
                user_data = faculty.objects.filter(
                    email=request.session.get("user"))
                for user in user_data:
                    user_name = user.name
                    profile = user.profile.url
                exam_data = {
                    "exam": Exam.objects.all(),
                    "user_name": user_name,
                    "profile": profile,
                }
                return render(request, "examlist.html", exam_data)
            else:
                return redirect("facultylogin")
        elif request.method == "POST":
            return redirect("facultylogin")
    except Exception as e:
        print(e)


# to delete exam by faculty
def delete_exam(request):
    if request.method == "POST":
        exam_code = request.POST["exam_code"]
        # print(exam_code)
        e = Exam.objects.filter(exam_code=exam_code)
        e.delete()
        return redirect("examlist")
    elif request.method == "GET":
        return redirect("examlist")


# To get the examlists for students
def examlist_student(request):
    try:
        if request.method == "GET":
            if request.session.get("user") != None:
                user_data = Student.objects.filter(
                    email=request.session.get("user"))
                for user in user_data:
                    user_name = user.name
                    profile = user.profile.url
                exam_data = {
                    "exam": Exam.objects.all(),
                    "user_name": user_name,
                    "profile": profile,
                }
                return render(request, "examliststudent.html", exam_data)
            else:
                return redirect("index")
        elif request.method == "POST":
            return redirect("index")
    except Exception as e:
        print(e)


# to load the all the subjects available on practice test page for subject selection
def practice_test(request):
    try:
        if request.method == "POST":
            return redirect("index")
        elif request.method == "GET":
            if request.session.get("user") != None:
                user_data = Student.objects.filter(
                    email=request.session.get("user"))
                for user in user_data:
                    user_name = user.name
                    profile = user.profile.url
                subject_data = {
                    "user_name": user_name,
                    "profile": profile,
                    "subjects": Subject.objects.all(),
                }
                return render(request, "practicetest.html", subject_data)
            else:
                return redirect("index")
    except Exception as e:
        print(e)


# to perform the practice test after selecting the subject
def practice_paper(request):
    try:
        if request.method == "POST":
            sub_code = request.POST["practicesubject"]
            # print(sub_code)
            subject = Subject.objects.filter(subject_code=sub_code)
            for s in subject:
                subject_name = s.subject_name
            user_data = Student.objects.filter(
                email=request.session.get("user"))
            for user in user_data:
                user_name = user.name
                profile = user.profile.url
            paper_data = {
                "paper": Questions.objects.filter(subject_code=sub_code).order_by('question_id')[:10],
                "sub_code": sub_code,
                "sub_name": subject_name,
                "exam_code": "Test",
                "time": 10,
                "user_name": user_name,
                "profile": profile,
                "check": True,
            }
            return render(request, "exampaper.html", paper_data)
        elif request.method == "GET":
            return redirect("practicetest")
    except Exception as e:
        print(e)


# To get questions from database and send it to exampaper
def exam_paper(request):
    if request.method == "GET":
        return redirect("examliststudent")
    elif request.method == "POST":
        e = request.POST["exam"]
        exam = Exam.objects.filter(exam_code=e)
        for p in exam:
            time = p.exam_duration
            no_of_questions = p.question_count
            sub_code = p.subject_code
        # print(sub_code)
        # print(time)
        subject = Subject.objects.filter(subject_code=sub_code)
        for s in subject:
            subject_name = s.subject_name
        # print(subject_name)
        user_data = Student.objects.filter(
            email=request.session.get("user"))
        for user in user_data:
            user_name = user.name
            profile = user.profile.url
        paper_data = {
            "paper": Questions.objects.filter(subject_code=sub_code).order_by('-question_id')[:no_of_questions],
            "sub_code": sub_code,
            "sub_name": subject_name,
            "exam_code": e,
            "time": time,
            "user_name": user_name,
            "profile": profile,
            "check": False,
        }
        return render(request, "exampaper.html", paper_data)


# To get the result after submitting the exampaper
def paper_check(request):
    if request.method == "POST":
        q = request.POST["questid"].split(',')
        a = request.POST["ans"].split(',')
        #m = request.POST["totalmarks"]
        exam_code = request.POST["examcode"]
        exam_type = request.POST["examtype"]
        # print(exam_type)
        # print(exam_code)
        #marks1 = (m)
        #print(q, len(q))
        #print(a, len(a))
        marks = 0
        for i in range(len(q)):
            if Questions.objects.filter(question_id=q[i], correct_answer=a[i]).exists():
                marks += 1
        #print("you have total marks of", marks)
        user_data = Student.objects.filter(
            email=request.session.get("user"))
        for user in user_data:
            user_name = user.name
            profile = user.profile.url
        exam_data = Exam.objects.filter(exam_code=exam_code)
        for e in exam_data:
            quest_count = e.question_count
        total_marks = {
            "marks": marks,
            "user_name": user_name,
            "profile": profile,
            "question_count": quest_count,
        }
        if exam_type == "practice":
            return render(request, "test_result.html", total_marks)
        else:
            from django.db import connection
            cursor = connection.cursor()
            query = (
                "insert into testexam_result(marks,email,exam_code)values(%s,%s,%s)")
            values = (marks, request.session.get("user"), exam_code)
            cursor.execute(query, values)
            cursor.close()
            connection.close()
            # r = result(email=user, marks=marks)
            # r.save()
            return render(request, "test_result.html", total_marks)
            # return HttpResponse("<h1>Result in Review...</h1>")
    else:
        return redirect("index")


# to get the results list for student
def result_list(request):
    try:
        if request.method == "GET":
            if request.session.get("user") != None:
                user_data = Student.objects.filter(
                    email=request.session.get("user"))
                for user in user_data:
                    user_name = user.name
                    profile = user.profile.url
                # to get the results of exams which user has given
                results = result.objects.filter(
                    email=request.session.get("user"))
                result_context = {
                    "result_data": results,
                    "user_name": user_name,
                    "profile": profile,
                }
                return render(request, "resultlist.html", result_context)
            else:
                return redirect("index")
        elif request.method == "POST":
            return redirect("index")
    except Exception as e:
        print(e)


# to visit about-us page
def about_us(request):
    # print("hello")
    if request.method == "POST":
        return render(request, "aboutus.html")
    elif request.method == "GET":
        return render(request, "aboutus.html")


# for contact-us from about-us page
def contact_us(request):
    try:
        if request.method == "GET":
            return render(request, "aboutus.html")
        elif request.method == "POST":
            email = request.POST["email"]
            phone = request.POST["phone"]
            query = request.POST["query"]
            c = contact(email=email, phone=phone, query=query)
            c.save()
            return render(request, "aboutus.html")
    except Exception as e:
        print(e)
