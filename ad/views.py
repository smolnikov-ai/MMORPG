from django.views.generic import (ListView, DetailView, )

from ad.models import Advertisement


class AdList(ListView):
    model = Advertisement
    ordering = ['-creation_date']
    context_object_name = 'ads'
    template_name = 'ads.html'
    paginate_by = 10

class AdDetail(DetailView):
    model = Advertisement
    context_object_name = 'ad'
    template_name = 'ad.html'
