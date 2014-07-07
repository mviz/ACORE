from django.conf.urls import patterns, url, include

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.homepage_view, name="home"),
    url(r'^questions/$', views.SurveyList.as_view(), name='questions'),
    url(r'^results/$', views.Results.as_view(), name='results'),
    url(r'^submitting/$', views.submit_survey, name='submitting'),
)