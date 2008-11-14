from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^card/', include('pxcs2w2.card.urls')),
    # Example:
    # (r'^pxcs2w2/', include('pxcs2w2.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
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