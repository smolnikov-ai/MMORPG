from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (ListView, DetailView, CreateView, )
from django.contrib import messages

from .forms import AdvertisementCreateForm, ReplyForm
from .models import Advertisement

class AdList(ListView):
    model = Advertisement
    ordering = ['-creation_date']
    context_object_name = 'ads'
    template_name = 'ads.html'
    paginate_by = 10

def advertisement_detail(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.advertisement = ad
            reply.user = request.user
            reply.save()
            messages.success(request, 'The reply has been created.')
            return redirect('ad-detail', pk=ad.pk)
    else:
        form = ReplyForm()

    replies = ad.reply_set.all()
    return render(request, 'ad.html', {
        'ad': ad,
        'form': form,
        'replies': replies,
    })


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

# def accept_reply(request):
#     reply = request.reply
#     reply.accept = True
#     reply.save()
#
#     previous_page = request.META.get('HTTP_REFERER')
#     #return redirect('ad-detail', pk=request.advertisement.pk)
#     if previous_page:
#         return redirect(previous_page)
#     else:
#         return redirect('ad-list')


