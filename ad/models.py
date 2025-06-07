from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    '''
    Represents the data of the author of the ad.

    Attributes:
        user: OneToOneField User
        first_name (str): first name of the author
        last_name (str): last name of the author
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class Category(models.Model):
    '''
    Represents the data of the advertisement category.

    Attributes:
        name (str): name of the category
    '''
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name.title()


class Reply(models.Model):
    '''
    Represents the data of the advertisement reply.
    Attributes:
        author: OneToOneField Author
        content: content of the reply
        creation_date: date the reply was created
        update_date: date the reply was updated
    '''
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class Advertisement(models.Model):
    '''
    Represents the data about the advertisement.

    Attributes:
        author: OneToOneField Author
        title (str): title of the advertisement
        content (str): content of the advertisement
        categories (List[Category]): list of categories of the advertisement
        creation_date: date the advertisement was created
        update_date: date the advertisement was updated
        replies (List[Reply]): list of replies of the advertisement
    '''
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    categories = models.ManyToManyField(Category, through='AdvertisementCategory')
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    replies = models.ManyToManyField(Reply, through='AdvertisementReply')


class AdvertisementCategory(models.Model):
    '''
    Represents the data about the advertisement categories.

    Attributes:
        advertisement: Advertisement
        category: Category of the advertisement
    '''
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class AdvertisementReply(models.Model):
    '''
    Represents the data about the advertisement replies.

    Attributes:
        advertisement: Advertisement
        reply: Reply of the advertisement
    '''
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
