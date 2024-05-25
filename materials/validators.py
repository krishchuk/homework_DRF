import re
from rest_framework.serializers import ValidationError

from materials.models import Subscription


class TitleValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r'^[a-zA-Z0-9\.\-\ ]+$')
        tmp_val = dict(value).get(self.field)
        if not bool(reg.match(tmp_val)):
            raise ValidationError('Исправьте название')


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = value.get(self.field, [])
        if "youtube.com" not in link:
            raise ValidationError("Оставьте ссылку на YouTube")


class SubscriptionValidator:
    def __call__(self, attrs):
        user = attrs.get('user')
        course = attrs.get('course')
        owner = attrs.get('owner')
        if user and course and owner and Subscription.objects.filter(user=user, course=course, owner=owner).exists():
            raise ValidationError('Вы уже подписаны на этот курс')
