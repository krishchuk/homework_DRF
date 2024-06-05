from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED

from materials.models import Course, Lesson, Subscription
from materials.paginators import LessonPagination, LearningPagination
from materials.serializers import CourseSerializer, LessonSerializer, CourseCountSerializer, SubscriptionSerializer
from materials.tasks import send_mail_update
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CourseCountSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [~IsModerator]
        elif self.action in ['update', 'retrieve', 'list']:
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        course = serializer.save()
        print('updating...')
        send_mail_update.delay(course_id=course.pk)
        print('updated')


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = LessonPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subscription_item = Subscription.objects.filter(user=user, course=course_item).first()

        if subscription_item:
            subscription_item.delete()
            message = 'подписка удалена'
            status = HTTP_204_NO_CONTENT
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'
            status = HTTP_201_CREATED

        return Response({'message': message}, status=status)


class SubscriptionListAPIView(ListAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    pagination_class = LearningPagination
    permission_classes = [IsAuthenticated, IsOwner]
