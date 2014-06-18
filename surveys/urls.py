from django.conf.urls import patterns, url, include

from . import views


urlpatterns = patterns(
    '',
    #url(r'^questions/', views.surveyIndex, name='survey list'),
    url(r'^questions/', views.SurveyList.as_view(), name='survey results'),
    url(r'^results/', views.Results.as_view(), name='survey results'),
    url(r'^submitting/', views.submit_survey, name='redirect home'),
)