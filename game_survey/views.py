from django.views import generic

class HomePageView(generic.TemplateView):
    template_name = 'home.html'

class ContactView(generic.TemplateView):
    template_name = 'contact.html'

class AcoreView(generic.TemplateView):
    template_name = 'acore.html'

