from django.contrib import admin

from .models import Advertisement, Reply

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'category', 'creation_date', )
    list_filter = ('title', 'content', 'category', 'creation_date', )

admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Reply)
