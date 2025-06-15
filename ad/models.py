import random
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse
from .resources import ADVERTISEMENT_CATEGORY_CHOICES


def generate_random_code():
    code = random.randrange(1000, 10000)
    return code

# расширяем класс AbstractUser полем одноразового кода для аутентификации
class CustomUser(AbstractUser):
    authentication_code = models.IntegerField(default=generate_random_code)
    groups = models.ManyToManyField(
        to='auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='Groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_permissions',  # Меняем related_name!
    )

    def __str__(self):
        return self.username

class Reply(models.Model):
    """
    Represents the data of the advertisement reply.

    Attributes:
        user: ForeignKey User
        content: content of the reply
        creation_date: date the reply was created
        update_date: date the reply was updated
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = CKEditor5Field(verbose_name='Content', config_name='extends')
    category = models.CharField(choices=ADVERTISEMENT_CATEGORY_CHOICES, default="TK")
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    replies = models.ManyToManyField(Reply, through='AdvertisementReply')

    def get_absolute_url(self):
        """
        Returns the absolute URL of the detailed ad viewing page.
        :return: the absolute URL of the form '/ad/<pk>/'
        """
        return reverse('ad-detail', kwargs={'pk': self.pk})


class AdvertisementReply(models.Model):
    """
    Represents the data about the advertisement replies.

    Attributes:
        advertisement: Advertisement
        reply: Reply of the advertisement
    """
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
