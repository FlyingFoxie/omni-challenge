from django import forms
from django.contrib import admin

from .constants import COLUMN_CHOICES
from .models import Company, Employee


class CompanyForm(forms.ModelForm):
    display_columns = forms.MultipleChoiceField(
        choices=[(key, value) for key, value in COLUMN_CHOICES.items()],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Company
        fields = "__all__"


class CompanyAdmin(admin.ModelAdmin):
    form = CompanyForm


admin.site.register(Employee)
admin.site.register(Company, CompanyAdmin)
