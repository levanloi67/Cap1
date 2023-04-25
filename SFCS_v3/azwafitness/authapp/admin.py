from django.contrib import admin
from authapp.models import Contact,MembershipPlan,Enrollment,Trainer,Gallery,Attendance,Bot
from .models import Bot
from .forms import BotForm

@admin.register(Bot)
class UserProfileAdmin(admin.ModelAdmin):
    form = BotForm

# Register your models here.
admin.site.register(Contact)
admin.site.register(MembershipPlan)
admin.site.register(Enrollment)
admin.site.register(Trainer)
admin.site.register(Gallery)
admin.site.register(Attendance)
# admin.site.register(Bot)