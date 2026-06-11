from rest_framework import serializers
from .models import Agent, SiteConfiguration

class SiteConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfiguration
        fields = '__all__'

class AgentSerializer(serializers.ModelSerializer):
    # Allow signatory_date to be blank/null in case form submits empty string
    signatory_date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Agent
        fields = '__all__'
