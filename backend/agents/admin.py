from django.contrib import admin
from django import forms
from .models import Agent, SiteConfiguration


class SiteConfigurationForm(forms.ModelForm):
    header_bg_color = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color', 'style': 'width:80px; height:40px; padding:2px; cursor:pointer;'}),
        required=False,
        help_text='Pick the header background colour',
    )

    class Meta:
        model = SiteConfiguration
        fields = '__all__'


class SiteConfigurationAdmin(admin.ModelAdmin):
    form = SiteConfigurationForm

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


admin.site.register(Agent)
admin.site.register(SiteConfiguration, SiteConfigurationAdmin)
