from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^', include('apps.dash.urls')),
    url('admin/', admin.site.urls),
]