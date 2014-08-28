from django.conf.urls import patterns, url, include

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.homepage_view, name="home"),
    url(r'^questions/$', views.SurveyList.as_view(), name='questions'),
    url(r'^submitting/$', views.submit_survey, name='submitting'),
    url(r'^ajax/$', views.acore_next_step, name="ajax"),
    url(r'^reinitialize/$', views.reinitialize_data, name='reinitialize'),
    url(r'^initialize/$', views.initialize_data, name='initialize'),
    url(r'^infoPopup/$', views.acoreInfoPopup, name='infoPopup'),
)