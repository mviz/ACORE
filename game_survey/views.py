from django.views import generic


class ContactView(generic.TemplateView):
    template_name = 'contact.html'

class AcoreView(generic.TemplateView):
    template_name = 'acore.html'

