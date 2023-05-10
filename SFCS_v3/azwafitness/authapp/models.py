from distutils.command.upload import upload
from django.db import models

# Create your models here.
# this file we creates a database tables

class Contact(models.Model):
    name=models.CharField(max_length=25)
    email=models.EmailField()
    phonenumber=models.CharField(max_length=12)
    description=models.TextField()

    def __str__(self):
        return self.email

class Bot(models.Model):
    GOAL_CHOICES = [
        ('lose_weight', 'Lose weight'),
        ('gain_muscle_mass', 'Gain muscle mass'),
        ('get_shredded', 'Get shredded'),
    ]

    PHYSICAL_CONDITION_CHOICES = [
        ('ectomorph', 'Ectomorph'),
        ('mesomorph', 'Mesomorph'),
        ('endomorph', 'Endomorph'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.CharField(max_length=20)
    weight = models.CharField(max_length=20)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    physical_Condition = models.CharField(max_length=20, choices=PHYSICAL_CONDITION_CHOICES)
    # birthday_day= models.CharField(max_length=20)
    # birthday_month= models.CharField(max_length=20)
    # birthday_year= models.CharField(max_length=20)
    birthday = models.CharField(max_length=20)

class Enrollment(models.Model):        
    FullName=models.CharField(max_length=25)
    Email=models.EmailField()
    Gender=models.CharField(max_length=25)
    PhoneNumber=models.CharField(max_length=12)
    DOB=models.CharField(max_length=50)
    SelectMembershipplan=models.CharField(max_length=200)
    Address=models.TextField()
    paymentStatus=models.CharField(max_length=55,blank=True,null=True)
    Price=models.IntegerField(blank=True,null=True)
    DueDate=models.DateTimeField(blank=True,null=True)
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True,)

    def __str__(self):
        return self.FullName

class Trainer(models.Model):
    name=models.CharField(max_length=55)
    gender=models.CharField(max_length=25)
    phone=models.CharField(max_length=25)
    salary=models.IntegerField()
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True)
    def __str__(self):
        return self.name

class MembershipPlan(models.Model):
    plan=models.CharField(max_length=185)
    price=models.IntegerField()

    def __int__(self):
        return self.id
    
class Gallery(models.Model):
    title=models.CharField(max_length=100)
    img=models.ImageField(upload_to='gallery')
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True)
    def __int__(self):
        return self.id
    
class Attendance(models.Model):
    Selectdate=models.DateTimeField(auto_now_add=True)
    phonenumber=models.CharField(max_length=15)
    Login=models.CharField(max_length=200)
    Logout=models.CharField(max_length=200)
    SelectWorkout=models.CharField(max_length=200)
    TrainedBy=models.CharField(max_length=200)
    def __int__(self):
        return self.id

class Suggest(models.Model):
    def __int__(self):
        return self.id