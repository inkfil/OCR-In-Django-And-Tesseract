
from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.filhome, name='filhome'),
    path('login', views.fillogin, name='fillogin'),
    path('readimage', views.filreadimage, name='filreadimage'),
    path('readtext', views.filreadtext, name='filreadtext'),
    path('readpdf', views.filreadpdf, name='filreadpdf'),
    path('readdoc', views.filreaddoc, name='filreaddoc'),
    path('showcode', views.filshowcode, name='showcode'),
]
if settings.DEBUG:
	urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
