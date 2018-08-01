from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sendsperant/', views.fb_sperant, name='Send Facebook'),
    url(r'^sendurbania/', views.urbania_sperant, name='Send Urbania'),
    url(r'^sendnexo/', views.nexo_sperant, name='Send Nexo'),
    url(r'^sendwebform/', views.web_sperant, name='Send Webform'),
]