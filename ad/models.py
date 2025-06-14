from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from .resources import ADVERTISEMENT_CATEGORY_CHOICES


class Reply(models.Model):
    '''
    Represents the data of the advertisement reply.

    Attributes:
        user: OneToOneField User
        content: content of the reply
        creation_date: date the reply was created
        update_date: date the reply was updated
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class Advertisement(models.Model):
    '''
    Represents the data about the advertisement.

    Attributes:
        user: OneToOneField User
        title (str): title of the advertisement
        content (RichTextUploadingField): content of the advertisement
        category (str): category of the advertisement
        creation_date: date the advertisement was created
        update_date: date the advertisement was updated
        replies (List[Reply]): list of replies of the advertisement
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = RichTextUploadingField(blank=True, null=True)
    category = models.CharField(choices=ADVERTISEMENT_CATEGORY_CHOICES, default="TK")
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    replies = models.ManyToManyField(Reply, through='AdvertisementReply')


class AdvertisementReply(models.Model):
    '''
    Represents the data about the advertisement replies.

    Attributes:
        advertisement: Advertisement
        reply: Reply of the advertisement
    '''
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
