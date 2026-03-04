from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PatientViewSet, VisitViewSet, AppointmentViewSet, dashboard_stats

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='api-patient')
router.register(r'visits', VisitViewSet, basename='api-visit')
router.register(r'appointments', AppointmentViewSet, basename='api-appointment')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard-stats/', dashboard_stats, name='dashboard-stats'),
]
