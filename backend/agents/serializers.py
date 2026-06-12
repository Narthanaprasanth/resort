from rest_framework import serializers
from .models import Agent, SiteConfiguration

class SiteConfigurationSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = SiteConfiguration
        fields = '__all__'

    def get_logo(self, obj):
        if obj.logo:
            return obj.logo.url
        return None

class AgentSerializer(serializers.ModelSerializer):
    # Allow signatory_date to be blank/null in case form submits empty string
    signatory_date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Agent
        fields = '__all__'
