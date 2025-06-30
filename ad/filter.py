from django_filters import FilterSet

from ad.models import Reply, Advertisement

class ReplyFilterSet(FilterSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.pop('request')
        self.filters['advertisement'].queryset = Advertisement.objects.filter(user=self.user)

    class Meta:
        model = Reply
        fields = ['advertisement']