"""
URL configuration for Her Beauty Hub project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('beautyhub.urls')),
]

# Serve media files (user uploaded content)
# Always serve media files - needed for production on Railway
# Note: For high-traffic sites, consider using cloud storage (AWS S3, Cloudinary, etc.)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in development only
# WhiteNoise handles static files in production
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "Her Beauty Hub Administration"
admin.site.site_title = "Her Beauty Hub Admin"
admin.site.index_title = "Welcome to Her Beauty Hub Management Portal"

