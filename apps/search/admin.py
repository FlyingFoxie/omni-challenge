from django.contrib import admin

from .models import Company, Employee

admin.site.register(Employee)
admin.site.register(Company)
