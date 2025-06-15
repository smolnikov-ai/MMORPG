from django import forms
from django_ckeditor_5.fields import CKEditor5Field
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Advertisement, Reply


class AdvertisementForm(forms.ModelForm):
    '''
    The advertisement form based on the model Advertisement

    The form fields include:
        title (str): title of the advertisement
        content (RichTextUploadingField): advertisement content with visual editor support
        category (str): category of the advertisement

    Attributes:
        content (forms.CharField): a field for entering the content of an ad with a visual editor widget
    '''
    content = forms.CharField()

    class Meta:
        '''
        Metadata of the form

        Fields:
            title (str): title of the advertisement
            content (RichTextUploadingField): content of the advertisement
            category (str): category of the advertisement
        '''
        model = Advertisement
        fields = [
            'title',
            'content',
            'category',
        ]


class ReplyForm(forms.ModelForm):
    '''
    The reply form based on the model Reply

    The form fields include:
        content (str): content of the reply
    '''

    class Meta:
        '''
        Metadata of the form

        Fields:
            content (str): content of the reply
        '''
        model = Reply
        fields = [
            'content',
        ]


class AdvertisementCreateForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget())

    class Meta:
        model = Advertisement
        fields = [
            'title',
            'content',
            'category',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['content'].required = False

