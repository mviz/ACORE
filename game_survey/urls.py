from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import HomePageView, AboutView

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^survey/', include('surveys.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', AboutView.as_view(), name='About page'),
)
