from django.contrib import admin
from .models import Advertisement, Reply

class AdvertisementAdmin(admin.ModelAdmin):
    """
    The administrator class for the model Advertisement.
    """
    # fields shown in the list of advertisements
    list_display = ('title', 'content', 'category', 'creation_date', )
    # filters for fast advertisement search
    list_filter = ('title', 'content', 'category', 'creation_date', )

# Registration of the Advertisement model in the administrative panel using
# the special administrative class AdvertisementAdmin
admin.site.register(Advertisement, AdvertisementAdmin)
# Easy registration of the Reply model in the administrative panel
admin.site.register(Reply)
