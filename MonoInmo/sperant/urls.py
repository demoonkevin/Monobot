from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sendsperant/', views.send_sperant, name='Send Sperant'),
]