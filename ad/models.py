import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from .resources import ADVERTISEMENT_CATEGORY_CHOICES


# расширяем класс AbstractUser полем одноразового кода для аутентификации
class User(AbstractUser):
    authentication_code = models.IntegerField(null=True, blank=True)
    #is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Advertisement(models.Model):
    """
    Represents the data about the advertisement.

    Attributes:
        user: ForeignKey User
        title (str): title of the advertisement
        content (CKEditor5Field): content of the advertisement
        category (str): category of the advertisement
        creation_date: date the advertisement was created
        update_date: date the advertisement was updated
        replies (List[Reply]): list of replies of the advertisement
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = RichTextUploadingField(verbose_name='Content')
    category = models.CharField(choices=ADVERTISEMENT_CATEGORY_CHOICES, default="TK")
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creation_date']

    def get_absolute_url(self):
        """
        Returns the absolute URL of the detailed ad viewing page.
        :return: the absolute URL of the form '/ad/<pk>/'
        """
        return reverse('ad-detail', kwargs={'pk': self.pk})


class Reply(models.Model):
    """
    Represents the data of the advertisement reply.

    Attributes:
        user: ForeignKey User
        content: content of the reply
        creation_date: date the reply was created
        update_date: date the reply was updated
    """
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creation_date']