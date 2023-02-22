from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.v1.foodgram.urls')),
    path('api/', include('api.v1.users.urls')),
]
