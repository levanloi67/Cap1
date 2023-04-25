from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from authapp.models import Contact,MembershipPlan,Trainer,Enrollment,Gallery,Attendance
from authapp.models import Suggest
from authapp.forms import BotForm
from authapp.models import Bot
from .model_classification import Model_Classification
from django.http import JsonResponse
from datetime import datetime
# from .suggest import suggest

import numpy as np

# Create your views here.
def BotForm(request):
    if request.method == 'POST':

        # # Đẩy data lên admin
        # gender = request.POST.get('gender')
        # height = request.POST.get('height')
        # weight = request.POST.get('weight')
        # goal = request.POST.get('goal')
        # type = request.POST.get('type')
        # birthday_day= request.POST.get('birthday-day')
        # birthday_month= request.POST.get('birthday-month')
        # birthday_year= request.POST.get('birthday-year')
        # birthday = f"{birthday_day}-{birthday_month}-{birthday_year}"
        # myquery=Bot(goal=goal,body_type=type,gender=gender,height=height,weight=weight,birthday=birthday)
        # myquery.save()

        print(request.POST)

        goal = request.POST['goal']
        # goal_list = goal.split(',')

        physical_Condition = request.POST['body']
        # physical_Condition_list = physical_Condition.split(',')

        birthday_year= request.POST['birthday-year']

        #Tính tuổi
        today = datetime.today().date()# Lấy ngày hiện tại
        age = today.year - int(birthday_year)

        weight = float(request.POST['weight'])
        height = float(request.POST['height'])

        gender = request.POST['gender']
        # gender_list = [1.0, 0.0]
        if gender == "male":
            gender = 1.0
            gender_list = [1.0]
        else:
            gender = 0.0
            gender_list = [0.0]
        
        # data = [gender, weight, height]
        # Tạo đầu vào
        data = [gender, height,weight]
        
        # Shape (1,3) 1 hàng (đầu vào) và có 3 cột
        data = np.array(data).reshape(1, -1)
        # Model xử lý đầu vào và trả về kết quả
        result = Model_Classification.get_instance().predict(data)
        # Lấy kết quả
        result = result[0]
        # Đây là thể hình mà mình muốn tìm
        result = Model_Classification.get_instance().get_classes()[result]
        type_Body = result
        if type_Body == "Extremely Weak":
            type_Body_list = ["Extremely Weak"]
        elif type_Body == "Weak":
            type_Body_list = ["Weak"]
        elif type_Body == "Normal":
            type_Body_list = ["Normal"]
        elif type_Body == "Overweight":
            type_Body_list = ["Overweight"]
        elif type_Body == "Obesity":
            type_Body_list = ["Obesity"]
        elif type_Body == "Extremely Obesity":
            type_Body_list = ["Extremely Obesity"]
        # type_Body_list = [type_Body]
        # return JsonResponse({'result_Suggest':type_Body_list})

        #so sánh tuổi
        if(age<16):
            age_range = "0"
        elif(30>=age>=16):
            age_range = "1"
        elif(45>=age>30):
            age_range = "2"
        else:
            age_range = "3"
        age_range_list = [age_range]

        goal_list = goal.split(',')
        physical_Condition_list = physical_Condition.split(',')
        
        list_tong = []
        item = ""
        val = ""
        def suggest(type_Body_list, age_range_list, gender_list, goal_list, physical_Condition_list):
            result_Suggest = []
            # list tổng
            list_tong = ['type_Body', 'age_range', 'gender', 'goal', 'physical_Condition']
            
            for item in list_tong:
                print("item:", item)
                if item == "type_Body":
                    for val in type_Body_list:
                        print("val:", val)
                        if val == "Extremely Weak":
                            result_Suggest.append("a")
                        elif val == "Weak":
                            result_Suggest.append("b")
                        elif val == "Normal":
                            result_Suggest.append("c")
                        elif val == "Overweight":
                            result_Suggest.append("d")
                        elif val == "Obesity":
                            result_Suggest.append("e")
                        elif val == "Extreme Obesity":
                            result_Suggest.append("f")
                elif item == "age_range":
                    for val in age_range_list:
                        print("val:", val)
                        if val == "0":
                            result_Suggest.append("1") 
                        elif val == "1":
                            result_Suggest.append("2")
                        elif val == "2":
                            result_Suggest.append("3")
                        elif val == "3":
                            result_Suggest.append("4")
                elif item == "gender":
                    for val in gender_list:
                        print("val:", val)
                        if val == 1.0:
                            result_Suggest.append("A") 
                        elif val == 0.0:
                            result_Suggest.append("B")
                elif item == "goal":
                    for val in goal_list:
                        print("val:", val)
                        if val == "lose_weight":
                            result_Suggest.append("I") 
                        elif val == "gain_muscle_mass":
                            result_Suggest.append("II")
                        elif val == "get_shredded":
                            result_Suggest.append("III")
                elif item == "physical_Condition":
                    for val in physical_Condition_list:
                        print("val:", val)
                        if val == "ectomorph":
                            result_Suggest.append("q") 
                        elif val == "mesomorph":
                            result_Suggest.append("w")
                        elif val == "endomorph":
                            result_Suggest.append("e")
                else:
                    result_Suggest.append("This is an exception")
            return result_Suggest
        
        result_Suggest = suggest(type_Body_list, age_range_list, gender_list, goal_list,physical_Condition_list)

        # chuyển list sang string
        Suggestions_for_exercises = '\n'.join(map(str, result_Suggest))

        # lấy từng thành phần trong list
        sd_e = result_Suggest.pop(0)
        nd_e = result_Suggest.pop(0)
        rd_e = result_Suggest.pop(0)
        th_e = result_Suggest.pop(0)
        fth_e = result_Suggest.pop(0)


        # xuất màn hình
        # return JsonResponse({'result': type_Body,'result_Suggest':result_Suggest})
        return render(request, 'bot.html', {'result': type_Body,'Suggestions_for_exercises':Suggestions_for_exercises,'sd_e':sd_e,'nd_e':nd_e,'rd_e':rd_e,'fth_e':fth_e,'th_e':th_e})

    else:
    #     form = BotForm()
        return render(request, 'bot.html')

def contact(request):
    if request.method=="POST":
        name=request.POST.get('fullname')
        email=request.POST.get('email')
        number=request.POST.get('num')
        desc=request.POST.get('desc')
        myquery=Contact(name=name,email=email,phonenumber=number,description=desc)
        myquery.save()       
        messages.info(request,"Thanks for Contacting us we will get back you soon")
        return redirect('/contact')
        
    return render(request,"contact.html")

def Suggest(request):
    return render (request,"Suggest.html")

def Bot(request):
    return render (request,"Bot.html")

def Home(request):
    return render(request,"index.html")

def gallery(request):
    posts=Gallery.objects.all()
    context={"posts":posts}
    return render(request,"gallery.html",context)

def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    SelectTrainer=Trainer.objects.all()
    context={"SelectTrainer":SelectTrainer}
    if request.method=="POST":
        phonenumber=request.POST.get('PhoneNumber')
        Login=request.POST.get('logintime')
        Logout=request.POST.get('loginout')
        SelectWorkout=request.POST.get('workout')
        TrainedBy=request.POST.get('trainer')
        query=Attendance(phonenumber=phonenumber,Login=Login,Logout=Logout,SelectWorkout=SelectWorkout,TrainedBy=TrainedBy)
        query.save()
        messages.warning(request,"Attendace Applied Success")
        return redirect('/attendance')
    return render(request,"attendance.html",context)

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    user_phone=request.user
    posts=Enrollment.objects.filter(PhoneNumber=user_phone)
    print(posts)
    context={"posts":posts}

    return render(request,"profile.html",context)

def signup(request):
    if request.method=="POST":
        username=request.POST.get('usernumber')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
      
        if len(username)>10 or len(username)<10:
            messages.info(request,"Phone Number Must be 10 Digits")
            return redirect('/signup')

        if pass1!=pass2:
            messages.info(request,"Password is not Matching")
            return redirect('/signup')
       
        try:
            if User.objects.get(username=username):
                messages.warning(request,"Phone Number is Taken")
                return redirect('/signup')
           
        except Exception as identifier:
            pass
        
        
        try:
            if User.objects.get(email=email):
                messages.warning(request,"Email is Taken")
                return redirect('/signup')
           
        except Exception as identifier:
            pass
        
        
        
        myuser=User.objects.create_user(username,email,pass1)
        myuser.save()
        messages.success(request,"User is Created Please Login")
        return redirect('/login')
        
        
    return render(request,"signup.html")

def handlelogin(request):
    if request.method=="POST":        
        username=request.POST.get('usernumber')
        pass1=request.POST.get('pass1')
        myuser=authenticate(username=username,password=pass1)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Successful")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/login')
            
        
    return render(request,"handlelogin.html")

def handleLogout(request):
    logout(request)
    messages.success(request,"Logout Success")    
    return redirect('/login')

def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')

    Membership=MembershipPlan.objects.all()
    SelectTrainer=Trainer.objects.all()
    context={"Membership":Membership,"SelectTrainer":SelectTrainer}
    if request.method=="POST":
        FullName=request.POST.get('FullName')
        email=request.POST.get('email')
        gender=request.POST.get('gender')
        PhoneNumber=request.POST.get('PhoneNumber')
        DOB=request.POST.get('DOB')
        member=request.POST.get('member')
        address=request.POST.get('address')
        query=Enrollment(FullName=FullName,Email=email,Gender=gender,PhoneNumber=PhoneNumber,DOB=DOB,SelectMembershipplan=member,Address=address)
        query.save()
        messages.success(request,"Thanks For Enrollment")
        return redirect('/join')



    return render(request,"enroll.html",context)