from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgentViewSet, SiteConfigurationView

router = DefaultRouter()
router.register(r'registrations', AgentViewSet)

urlpatterns = [
    path('config/', SiteConfigurationView.as_view(), name='site-config'),
    path('', include(router.urls)),
]
