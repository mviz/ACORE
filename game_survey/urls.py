from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import ContactView, AcoreView


urlpatterns = patterns('',
    #url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^contact/$', ContactView.as_view(), name='Contact page'),
    url(r'^acore/$', AcoreView.as_view(), name='Acore page'),
    url(r'^surveys/', include('surveys.urls', namespace='surveys')),
    url(r'^$', include('surveys.urls', namespace='surveys')),
)