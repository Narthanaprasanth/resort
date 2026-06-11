from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Agent
from .serializers import AgentSerializer

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all().order_by('-created_at')
    serializer_class = AgentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Generate vendor_id based on primary key
        instance = serializer.instance
        instance.vendor_id = f"VND-{instance.id:06d}"
        instance.save()
        
        # return updated data
        return Response(AgentSerializer(instance).data, status=status.HTTP_201_CREATED, headers=headers)
