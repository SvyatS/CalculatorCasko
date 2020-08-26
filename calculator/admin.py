from django.contrib import admin
from .models import *
# Register your models here.

class Admin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(Policyholder)
admin.site.register(Record, Admin)
