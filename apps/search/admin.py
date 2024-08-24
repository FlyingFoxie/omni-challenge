from django import forms
from django.contrib import admin

from .constants import COLUMN_CHOICES
from .models import Company, Employee, Organization


class OrganizationForm(forms.ModelForm):
    display_columns = forms.MultipleChoiceField(
        choices=[(key, value) for key, value in COLUMN_CHOICES.items()],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationAdmin(admin.ModelAdmin):
    form = OrganizationForm


admin.site.register(Employee)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Company)
