from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hasker.apps.person.urls')),
    path('', include('hasker.apps.questions.urls')),
    path('api/v1/', include('hasker.api.urls', namespace='api')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
