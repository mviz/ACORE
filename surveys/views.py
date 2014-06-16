from django.shortcuts import get_object_or_404
from django.views import generic
from surveys.models import SurveyQuestion, SurveyAnswer
from django.core.urlresolvers import reverse
from django.http import HttpsResponseRedirect, HttpsResponse

class Results(generic.TemplateView):
    template_name = 'surveys/survey_results.html'

class SurveyList(generic.ListView):
    model = SurveyQuestion
    template_name = "surveys/survey_list.html"

    def get_context_data(self, **kwargs):
        context = super(SurveyList, self).get_context_data(**kwargs)
        return context
    #def get_queryset(self):
    #    return self.object_list