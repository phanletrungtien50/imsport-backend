from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse  # 👈 thêm

def home(request):  # 👈 thêm
    return JsonResponse({
        "status": "ok",
        "message": "Backend is running 🚀"
    })

urlpatterns = [
    path('', home),  # 👈 thêm dòng này
    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)