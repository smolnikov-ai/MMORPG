from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView, )
from .forms import AdvertisementCreateForm
from .models import Advertisement

class AdList(ListView):
    model = Advertisement
    ordering = ['-creation_date']
    context_object_name = 'ads'
    template_name = 'ads.html'
    paginate_by = 10

class AdDetail(DetailView):
    model = Advertisement
    context_object_name = 'ad'
    template_name = 'account/base_entrance.html'

class AdCreate(LoginRequiredMixin, CreateView):
#class AdCreate(CreateView):
    """
    View-class for creating new advertisement.

    Inherits the LoginRequiredMixin mixins, which guarantees protection from anonymous users
    and verification of necessary permissions.
    The main task of the class is to process the form for creating an advertisement.
    """
    # related Advertisement Model
    model = Advertisement
    # the form class for creating an advertisement
    form_class = AdvertisementCreateForm
    # template for rendering the advertisement creation form
    template_name = 'ad_create.html'

    def form_valid(self, form):
        """
        The method is called when the form is valid (filled out correctly).

        Before saving the record, sets the owner of the ad equal to the current user.
        Overrides the basic implementation of the `form_valid' method to add additional logic.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)



