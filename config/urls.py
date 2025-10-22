from django.contrib import admin
from django.urls import path, include
from soundlab_store.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('soundlab_store.urls')),
    path('usuario/', include('usuario.urls')),  # 👈 importante
]


