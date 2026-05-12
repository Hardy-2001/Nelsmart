
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('control/', admin.site.urls),
    path('', include('store.urls')),
    path('training/', include('training.urls')),
]

# THIS MUST BE OUTSIDE the list
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

