from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from pxcs2w2.card import views

urlpatterns = patterns('',
    url(r'^(\d{3})$', views.index, name='card_view'),
)