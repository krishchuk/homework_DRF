from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(id=1, email='user@test.ru')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='test', description='test test')
        self.lesson = Lesson.objects.create(title='test', description='test test', course=self.course,
                                            video_url='https://youtube.com/test/', owner=self.user)

    def test_create_lesson(self):
        data = {'title': 'creating test', 'description': 'creating test test',
                'course': self.course.id, 'video_url': 'https://youtube.com/test2/',
                'owner': self.user.id}
        response = self.client.post('/course/lesson/create/', data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(title=data['title']).exists())

    def test_retrieve_lesson(self):
        path = reverse('materials:lesson_get', args=[self.lesson.id])
        response = self.client.get(path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_retrieve_not_existent_lesson(self):
        not_existent_lesson_id = 9999
        path = reverse('materials:lesson_get', args=[not_existent_lesson_id])
        response = self.client.get(path)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_lesson(self):
        path = reverse('materials:lesson_update', args=[self.lesson.id])
        data = {'title': 'updating test', 'description': 'updating test test', 'video_url': 'https://youtube.com/test/'}
        response = self.client.patch(path, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, data['title'])

    def test_delete_lesson(self):
        not_owner = User.objects.create(id=2, email='moderator@test.ru',
                                        password='12345')
        self.client.force_authenticate(user=not_owner)
        path = reverse('materials:lesson_delete', [self.lesson.id])
        response = self.client.delete(path)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(
            email='test1@test.ru',
            password='12345',
        )
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            title='test',
            description='test',
        )

    def test_create_subscription(self):
        data = {
            'user': self.user.id,
            'course': self.course.id,
        }

        response = self.client.post('/course/subscription/create/', data=data)
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {'message': 'подписка добавлена'}
        )

    def test_list_subscription(self):
        response = self.client.get(reverse('materials:subscription_list'))
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)
        self.assertEqual(response.json(), {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_delete_subscription(self):
        data = {
            'user': self.user.id,
            'course': self.course.id,
        }
        response = self.client.post('/course/subscription/create/', data=data)

        self.assertEqual(
            response.json(),
            {'message': 'подписка добавлена'}
        )
        print(response.json())

        response = self.client.post('/course/subscription/create/', data=data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {'message': 'подписка удалена'})
        print(response.content)
