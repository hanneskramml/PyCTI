from django.views.generic.base import TemplateView
from django.contrib import messages

class DashboardView(TemplateView):
    template_name = "app/home.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        messages.info(self.request, "hello World!")
        return context