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
from django.http import HttpResponse
# from .suggest import suggest

import numpy as np

# Create your views here.
def BotForm(request):
    if request.method == 'POST':
        print('save data')

        # Đẩy data lên admin
        gender = request.POST.get('gender')
        print(type(gender))
        
        # return JsonResponse({'result': type(gender)})
        height = request.POST.get('height')
        print(height)
        weight = request.POST.get('weight')
        print(weight)
        goal = request.POST.get('goal')
        print(goal)
        physical_Condition = request.POST.get('physical_Condition')
        print(physical_Condition)
        birthday_day= request.POST.get('birthday_day')
        print(birthday_day)
        birthday_month= request.POST.get('birthday_month')
        print(birthday_month)
        birthday_year= request.POST.get('birthday_year')
        print(birthday_year)
        birthday = f"{birthday_day}-{birthday_month}-{birthday_year}"
        birthday= request.POST.get('birthday')
        print(birthday)

        # Kiem tra kieu du lieu khi get tu POST
        type_gender = type(gender).__name__
        type_height = type(height).__name__
        type_weight = type(weight).__name__
        type_goal = type(goal).__name__
        type_physical_Condition = type(physical_Condition).__name__
        # type_birthday_day = type(birthday_day).__name__
        # type_birthday = type(birthday).__name__
        # return JsonResponse({'gender': type_gender,'height':type_height,'weight':type_weight,'goal':type_goal,'physical_Condition':type_physical_Condition,'birthday_day':type_birthday_day,'birthday':type_birthday})

        # myquery=Bot(gender=gender,height=height,weight=weight,goal=goal,physical_Condition=physical_Condition,birthday=birthday)
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
                if item == "goal":
                    for val in goal_list:
                        # print("val:", val)
                        if val == "lose_weight":
                            if "gender" in list_tong:
                                for val in gender_list:
                                    # print("val:", val)
                                    if val == 1.0:
                                        if "type_Body" in list_tong:
                                            for val in type_Body_list:
                                                if val == "Extremely Weak":
                                                    result_Suggest.append("Bắt đầu với các bài tập cardio nhẹ nhàng như đi bộ, chạy bộ, hoặc bơi lội. Sau đó, nên tập thêm các bài tập đẩy tay, cơ bụng, squat để tăng cường đốt cháy calo và giảm mỡ thừa.")
                                                elif val == "Weak":
                                                    result_Suggest.append("Tập luyện cardio nhẹ nhàng như chạy bộ, đi bộ, hoặc bơi lội. Nên tập thêm các bài tập đẩy tay, cơ bụng, squat để tăng cường đốt cháy calo và giảm mỡ thừa.")
                                                elif val == "Normal":
                                                    result_Suggest.append("Tập luyện cardio như chạy bộ, đi bộ, hoặc bơi lội. Nên tập thêm các bài tập đẩy tay, cơ bụng, squat để tăng cường đốt cháy calo và giảm mỡ thừa.")
                                                elif val == "Overweight":
                                                    result_Suggest.append("Tập luyện cardio như chạy bộ, đi bộ, hoặc bơi lội. Nên tập thêm các bài tập đẩy tay, cơ bụng, squat để tăng cường đốt cháy calo và giảm mỡ thừa.")
                                                else :
                                                    result_Suggest.append("Tập luyện cardio như chạy bộ, đi bộ, hoặc bơi lội. Nên tập thêm các bài tập đẩy tay, cơ bụng, squat để tăng cường đốt cháy calo và giảm mỡ thừa. Cần hạn chế tập các bài tập tạ hoặc các bài tập khác có tác động mạnh đến cơ bắp và khớp.")

                                    else:
                                        if "type_Body" in list_tong:
                                            for val in type_Body_list:
                                                if val == "Extremely Weak":
                                                    result_Suggest.append("Bắt đầu với các bài tập yoga, pilates hoặc aerobic để giảm cân một cách nhẹ nhàng. Nên tập thêm các bài tập giúp đốt cháy mỡ như plank, cơ bụng và các bài tập cardio như chạy bộ, nhảy dây.")
                                                elif val == "Weak":
                                                    result_Suggest.append("Tập yoga, pilates hoặc aerobic để giảm cân một cách nhẹ nhàng. Nên tập thêm các bài tập giúp đốt cháy mỡ như plank, cơ bụng và các bài tập cardio như chạy bộ, nhảy dây.")
                                                elif val == "Normal":
                                                    result_Suggest.append("Tập yoga, pilates hoặc aerobic để giảm cân một cách nhẹ nhàng. Nên tập thêm các bài tập cardio như chạy bộ, nhảy dây hoặc bơi lội để tăng cường đốt cháy calo và giảm mỡ thừa.")
                                                elif val == "Overweight":
                                                    result_Suggest.append("Tập yoga, pilates hoặc aerobic để giảm cân một cách nhẹ nhàng. Nên tập thêm các bài tập giúp đốt cháy mỡ như plank, cơ bụng và các bài tập cardio như chạy bộ, nhảy dây hoặc bơi lội để tăng cường đốt cháy calo và giảm mỡ thừa.")
                                                else :
                                                    result_Suggest.append("Tập yoga, pilates hoặc aerobic để giảm cân một cách nhẹ nhàng. Nên tập thêm các bài tập giúp đốt cháy mỡ như plank, cơ bụng và các bài tập cardio như chạy bộ, nhảy dây hoặc bơi lội để tăng cường đốt cháy calo và giảm mỡ thừa. Cần hạn chế tập các bài tập tạ hoặc các bài tập khác có tác động mạnh đến cơ bắp và khớp.")

                        elif val == "gain_muscle_mass":
                            if "gender" in list_tong:
                                for val in gender_list:
                                    # print("val:", val)
                                    if val == 1.0:
                                        if "type_Body" in list_tong:
                                            for val in type_Body_list:
                                                if val == "Extremely Weak":
                                                    result_Suggest.append("Tập các bài tập cơ bắp cơ bản như tạ đơn, đẩy tay, nâng tạ, squat với trọng lượng nhẹ để tăng cường cơ bắp và giúp cơ thể phát triển.")
                                                elif val == "Weak":
                                                    result_Suggest.append("Tập các bài tập cơ bắp cơ bản như tạ đơn, đẩy tay, nâng tạ, squat với trọng lượng vừa phải để tăng cường cơ bắp và giúp cơ thể phát triển.")
                                                elif val == "Normal":
                                                    result_Suggest.append("Tập các bài tập cơ bắp như tạ đơn, đẩy tay, nâng tạ, squat với trọng lượng vừa phải để tăng cường cơ bắp và giúp cơ thể phát triển. Nên tập thêm các bài tập cardio để giảm mỡ thừa và giúp cơ bắp được khoe hơn.")
                                                elif val == "Overweight":
                                                    result_Suggest.append("Tập các bài tập cơ bắp như tạ đơn, đẩy tay, nâng tạ, squat với trọng lượng vừa phải để tăng cường cơ bắp và giúp cơ thể phát triển. Nên tập thêm các bài tập cardio để giảm mỡ thừa và giúp cơ bắp được khoe hơn.")
                                                else :
                                                    result_Suggest.append("Bắt đầu với các bài tập cardio nhẹ nhàng như đi bộ, chạy bộ, hoặc bơi lội")

                                    else:
                                        if "type_Body" in list_tong:
                                            for val in type_Body_list:
                                                if val == "Extremely Weak":
                                                    result_Suggest.append("Tập các bài tập cơ bắp cơ bản như tạ đơn, đẩy tay, nâng tạ, squat với trọng lượng nhẹ để tăng cường cơ bắp và giúp cơ thể phát triển.")
                                                elif val == "Weak":
                                                    result_Suggest.append("Tập các bài tập cơ bắp cơ bản như tạ đơn, đẩy tay, nâng tạ, squat với trọng lượng vừa phải để tăng cường cơ bắp và giúp cơ thể phát triển.")
                                                elif val == "Normal":
                                                    result_Suggest.append("Tập các bài tập cơ bắp như tạ đơn, đẩy tay, nâng tạ, squat với trọng lượng vừa phải để tăng cường cơ bắp và giúp cơ thể phát triển. Nên tập thêm các bài tập cardio để giảm mỡ thừa và giúp cơ bắp được khoe hơn.")
                                                elif val == "Overweight":
                                                    result_Suggest.append("Tập các bài tập cơ bắp như tạ đơn, đẩy tay, nâng tạ, squat với trọng lượng vừa phải để tăng cường cơ bắp và giúp cơ thể phát triển. Nên tập thêm các bài tập cardio nhẹ nhàng như yoga, pilates hoặc aerobic để giảm cân một cách nhẹ nhàng và giúp cơ bắp được khoe hơn.")
                                                else :
                                                    result_Suggest.append("Bắt đầu với các bài tập cardio nhẹ nhàng như đi bộ, chạy bộ, hoặc bơi lội để tăng cường sức khỏe và giảm cân. Sau khi giảm cân đến mức an toàn, có thể bắt đầu tập các bài tập cơ bắp như tạ đơn, đẩy tay, nâng tạ, squat với trọng lượng nhẹ để tăng cường cơ bắp và giúp cơ thể phát triển.")

                        else:
                            if "gender" in list_tong:
                                for val in gender_list:
                                    # print("val:", val)
                                    if val == 1.0:
                                        if "type_Body" in list_tong:
                                            for val in type_Body_list:
                                                if val == "Extremely Weak":
                                                    result_Suggest.append("Tập các bài tập cơ bắp cơ bản như tạ đơn, đẩy tay, nâng tạ, squat với trọng lượng nhẹ để tăng cường cơ bắp và giúp cơ thể phát triển. Nên tập thêm các bài tập cardio như chạy bộ, nhảy dây hoặc bơi lội để tăng cường đốt cháy calo và giảm mỡ thừa.")
                                                elif val == "Weak":
                                                    result_Suggest.append("Tập các bài tập cơ bắp cơ bản như tạ đơn, đẩy tay, nâng tạ, squat với trọng lượng vừa phải để tăng cường cơ bắp và giúp cơ thể phát triển. Nên tập thêm các bài tập cardio như chạy bộ, nhảy dây hoặc bơi lội để tăng cường đốt cháy calo và giảm mỡ thừa.")
                                                else :
                                                    result_Suggest.append("Tập các bài tập cơ bắp như tạ đơn, đẩy tay, nâng tạ, squat với trọng lượng vừa phải để tăng cường cơ bắp và giúp cơ thể phát triển. Nên tập thêm các bài tập cardio như chạy bộ, nhảy dây hoặc bơi lội để tăng cường đốt cháy calo và giảm mỡ thừa.")

                                    else:
                                        if "type_Body" in list_tong:
                                            for val in type_Body_list:
                                                if val == "Extremely Weak":
                                                    result_Suggest.append("Tập yoga, pilates hoặc aerobic để giảm cân một cách nhẹ nhàng. Nên tập thêm các bài tập giúp đốt cháy mỡ như plank, cơ bụng và các bài tập cardio như chạy bộ, nhảy dây hoặc bơi lội để tăng cường đốt cháy calo và giảm mỡ thừa.")
                                                else :
                                                    result_Suggest.append("Tập yoga, pilates hoặc aerobic để giảm cân một cách nhẹ nhàng. Nên tập thêm các bài tập giúp đốt cháy mỡ như plank, cơ bụng và các bài tập cardio như chạy bộ, nhảy dây hoặc bơi lội để tăng cường đốt cháy calo và giảm mỡ thừa.")


                elif item == "age_range":
                    for val in age_range_list:
                        print("val:", val)
                        if val == "0":
                            if "physical_Condition" in list_tong:
                                for val in physical_Condition_list:
                                    print("val:", val)
                                    if val == "ectomorph":
                                        result_Suggest.append("Cường độ tập luyện nên tập trung vào việc tăng cường sức mạnh và cơ bắp. Tập luyện từ 3-4 lần/tuần, với cường độ trung bình đến cao.")
                                    elif val == "mesomorph":
                                        result_Suggest.append("Cường độ tập luyện nên tập trung vào việc phát triển sức mạnh, cơ bắp và sự nhanh nhẹn. Tập luyện từ 3-4 lần/tuần, với cường độ trung bình đến cao.")
                                    else:
                                        result_Suggest.append("Cường độ tập luyện nên tập trung vào việc giảm mỡ và tăng cường sức khỏe. Tập luyện từ 3-4 lần/tuần, với cường độ trung bình đến thấp.")
                        elif val == "1":
                            if "physical_Condition" in list_tong:
                                for val in physical_Condition_list:
                                    print("val:", val)
                                    if val == "ectomorph":
                                        result_Suggest.append("Cường độ tập luyện nên tập trung vào việc tăng cường sức mạnh và cơ bắp. Tập luyện từ 3-5 lần/tuần, với cường độ trung bình đến cao.")
                                    elif val == "mesomorph":
                                        result_Suggest.append("Cường độ tập luyện nên tập trung vào việc phát triển sức mạnh, cơ bắp và sự nhanh nhẹn. Tập luyện từ 3-5 lần/tuần, với cường độ trung bình đến cao.")
                                    else:
                                        result_Suggest.append("Cường độ tập luyện nên tập trung vào việc giảm mỡ và tăng cường sức khỏe. Tập luyện từ 3-4 lần/tuần, với cường độ trung bình đến thấp.")
                        elif val == "2":
                            if "physical_Condition" in list_tong:
                                for val in physical_Condition_list:
                                    print("val:", val)
                                    if val == "ectomorph":
                                        result_Suggest.append("Cường độ tập luyện nên tập trung vào việc tăng cường sức mạnh, cơ bắp và duy trì thể lực. Tập luyện từ 2-4 lần/tuần, với cường độ trung bình đến cao.")
                                    elif val == "mesomorph":
                                        result_Suggest.append("Cường độ tập luyện nên tập trung vào việc phát triển sức mạnh, cơ bắp và sự nhanh nhẹn. Tập luyện từ 2-4 lần/tuần, với cường độ trung bình đến cao.")
                                    else:
                                        result_Suggest.append("Cường độ tập luyện nên tập trung vào việc giảm mỡ và tăng cường sức khỏe. Tập luyện từ 2-3 lần/tuần, với cường độ trung bình đến thấp.")
                        else:
                            if "physical_Condition" in list_tong:
                                for val in physical_Condition_list:
                                    print("val:", val)
                                    if val == "ectomorph":
                                        result_Suggest.append("Cường độ tập luyện nên tập trung vào việc duy trì và nâng cao sức khỏe, bảo vệ cơ bắp và xương khớp. Tập luyện từ 2-3 lần/tuần, với cường độ thấp đến trung bình.")
                                    elif val == "mesomorph":
                                        result_Suggest.append("Cường độ tập luyện nên tập trung vào việc duy trì sức mạnh, cơ bắp và sự nhanh nhẹn, đồng thời bảo vệ sức khỏe của cơ thể. Tập luyện từ 2-3 lần/tuần, với cường độ trung bình đến cao.")
                                    else:
                                        result_Suggest.append("Cường độ tập luyện nên tập trung vào việc giảm mỡ, duy trì sức khỏe và tăng cường khả năng thực hiện các hoạt động hàng ngày. Tập luyện từ 2-3 lần/tuần, với cường độ thấp đến trung bình.")

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
        return render(request, 'bot.html', {'result': type_Body,'nd_e':nd_e,'th_e':th_e})#'Suggestions_for_exercises':Suggestions_for_exercises,
        # return HttpResponse(request, {type(gender)})

    else:
        print('Save Data Failed')
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