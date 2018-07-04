from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sendsperant/', views.send_sperant, name='Send Sperant'),
    url(r'^sendurbania/', views.urbania_sperant, name='Send Urbania'),
    url(r'^sendnexo/', views.nexo_sperant, name='Send Nexo'),
]