from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTokenTestCase(APITestCase):
    """TestCase на получение токена юзера"""
    def setUp(self):
        self.user = User.objects.create(
            email='test2@habit.com',
            password='321qwe',
            tg_username='test2'
        )

    def test_get_users_token(self):
        """Test на получение токена юзера"""
        self.user.set_password(self.user.password)
        self.user.save()

        data = {
            'email': 'test2@habit.com',
            'password': '321qwe'

        }

        response = self.client.post(
            reverse('users:token_obtain_pair'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class UserCreateTestCase(APITestCase):
    """TestCase на создания юзера"""
    def setUp(self):
        pass

    def test_create_user(self):
        """Test на создания юзера"""
        data = {
            'email': 'test1@habit.com',
            'password': 'test',
            'tg_username': 'test1'
        }

        response = self.client.post(
            reverse('users:register'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )


class UserDestroyTestCase(APITestCase):
    """TestCase на удаление юзера"""
    def setUp(self):
        self.user = User.objects.create(
            email='test@habit.com',
            password='test',
            tg_username='test3'
        )

    def test_user_delete(self):
        """Test на удаление юзера"""
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse('users:user_delete',
                    args=[self.user.pk])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(User.objects.filter(id=self.user.id).exists())


class UserListTestCase(APITestCase):
    """TestCase на вывод списка юзеров"""
    def setUp(self):
        self.user = User.objects.create(
            email='test@habit.com',
            password='test',
            tg_username='test',
            is_staff=True
        )

    def test_user_list(self):
        """Test на вывод списка юзеров"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('users:user_list'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class UserRetrieveTestCase(APITestCase):
    """TestCase на вывод профиля юзера"""
    def setUp(self):
        self.user = User.objects.create(
            email='test@habit.com',
            password='test',
            tg_username='test'
        )

    def test_user_retrieve(self):
        """Test на вывод профиля юзера"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('users:user_detail',
                    args=[self.user.pk])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class UserUpdateTestCase(APITestCase):
    """TestCase на обновление юзера"""
    def setUp(self):
        self.user = User.objects.create(
            email='test@habit.com',
            password='test',
            tg_username='test'
        )

    def test_user_update(self):
        """Test на обновление юзера"""
        self.client.force_authenticate(user=self.user)

        data = {
            'first_name': 'Test updated',
            'last_name': 'Testov'
        }

        response = self.client.patch(
            reverse('users:user_update',
                    args=[self.user.pk]),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
