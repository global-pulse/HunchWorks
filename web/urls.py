from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('web.views',
	(r'^homepageStrict', 'homepage'),
	(r'^profileStrict', 'profile'),
    (r'^', 'index'),
    
    


    # Examples:
    # url(r'^$', 'hunchWorks.views.home', name='home'),
    # url(r'^hunchWorks/', include('hunchWorks.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
