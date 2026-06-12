import logging
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import viewsets, status, views
from rest_framework.response import Response
from .models import Agent, SiteConfiguration
from .serializers import AgentSerializer, SiteConfigurationSerializer
from .pdf_utils import generate_registration_pdf
import threading

logger = logging.getLogger(__name__)


class SiteConfigurationView(views.APIView):
    def get(self, request, *args, **kwargs):
        config = SiteConfiguration.objects.first()
        if config:
            serializer = SiteConfigurationSerializer(config, context={'request': request})
            return Response(serializer.data)
        return Response({})


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all().order_by('-created_at')
    serializer_class = AgentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Assign Vendor ID
        instance = serializer.instance
        instance.vendor_id = f"VND-{instance.id:06d}"
        instance.save()

        # ── Generate PDF & send email in background ─────────────────────────────────────
        def send_registration_email(instance_id):
            try:
                # We fetch the instance again in the thread just to be safe
                agent_instance = Agent.objects.get(id=instance_id)
                pdf_bytes = generate_registration_pdf(agent_instance)
                filename = f"Agent_Registration_{agent_instance.vendor_id}.pdf"

                email = EmailMessage(
                    subject=f'New Agent Registration — {agent_instance.agency_name} ({agent_instance.vendor_id})',
                    body=(
                        f"Hello,\n\n"
                        f"A new agent has completed the registration form.\n\n"
                        f"Agency : {agent_instance.agency_name}\n"
                        f"Contact: {agent_instance.contact_name} ({agent_instance.contact_email})\n"
                        f"City   : {agent_instance.city}\n"
                        f"Vendor : {agent_instance.vendor_id}\n\n"
                        f"Please find the full registration PDF attached.\n\n"
                        f"— Resort Agent Partner Portal"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.ADMIN_EMAIL],
                )
                email.attach(filename, pdf_bytes, 'application/pdf')
                email.send(fail_silently=False)
                logger.info(f"Registration email sent for {agent_instance.vendor_id}")
            except Exception as e:
                logger.error(f"Failed to send registration email for {agent_instance.vendor_id}: {e}")

        # Start thread
        thread = threading.Thread(target=send_registration_email, args=(instance.id,))
        thread.start()

        return Response(AgentSerializer(instance).data, status=status.HTTP_201_CREATED, headers=headers)

