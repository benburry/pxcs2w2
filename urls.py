from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import login, logout
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from pxcs2w2.default.views import register
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'index.html'}, name='site_root'),
    (r'^cards/', include('pxcs2w2.card.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^accounts/login/$', login, {'template_name': 'login.html'}),
    (r'^accounts/logout/$', logout, {'next_page': '/'}),
    (r'^accounts/register/$', register),
)

if settings.DEBUG:
    import os.path
    from django.views import static
    statics_dir = os.path.join(os.path.dirname(__file__), 'statics').replace('\\','/')
    urlpatterns += patterns('',
        (r'^styles/(?P<path>.*)$', static.serve, {'document_root': os.path.join(statics_dir, 'style')}),
        (r'^js/(?P<path>.*)$', static.serve, {'document_root': os.path.join(statics_dir, 'js')}),
		(r'^images/(?P<path>.*)$', static.serve, {'document_root': os.path.join(statics_dir, 'images')}),
    )