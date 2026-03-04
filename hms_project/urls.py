from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('dashboard'), name='home'),
    path('admin/', admin.site.urls),
    path('', include('patients.urls')),
    path('api/', include('patients.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "MediCare HMS Admin"
admin.site.site_title = "MediCare HMS"
admin.site.index_title = "Hospital Management System"
