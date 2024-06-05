from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import TitleValidator, LinkValidator, SubscriptionValidator


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            TitleValidator(field='title'),
            serializers.UniqueTogetherValidator(fields=['title'], queryset=Lesson.objects.all()),
        ]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            TitleValidator(field='title'),
            LinkValidator('video_url'),
            serializers.UniqueTogetherValidator(fields=['title'], queryset=Lesson.objects.all()),
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [
            SubscriptionValidator(),
        ]


class CourseCountSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True)
    # subscriptions = SubscriptionSerializer(source='subscription_set', many=True)
    subscription = SerializerMethodField()

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_subscription(self, obj):
        if Subscription.objects.filter(course=obj, user=self.context.get('request', None).user.id):
            return True
        return False

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'lessons_count', 'lessons', 'subscription', )
