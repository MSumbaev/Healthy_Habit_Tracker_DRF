from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from users.models import User


class HabitCreateTestCase(APITestCase):
    """TestCase на создание привычки"""
    def setUp(self):
        self.user = User.objects.create(
            email='test@habit.com',
            password='test',
            tg_username='test3'
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            place='Улица',
            time='19:00',
            action='Бег',
            is_pleasant=True,
            linked=None,
            period=7,
            length=120,
            is_public=False
        )
        self.habit2 = Habit.objects.create(
            owner=self.user,
            place='Улица',
            time='19:00',
            action='Бег',
            is_pleasant=False,
            linked=None,
            period=7,
            reward='Снижение веса',
            length=120,
            is_public=False
        )

    def test_reward_or_Linked_validator(self):
        """Тест валидации на одновременное заполнение полей 'linked' и 'reward'"""
        self.client.force_authenticate(user=self.user)

        data = {
            'owner': self.user.pk,
            'place': 'Дом',
            'time': '07:00',
            'action': 'Зарядка',
            'is_pleasant': False,
            'linked': self.habit.pk,
            'period': 7,
            'reward': '1000 руб.',
            'length': 120,
            'is_public': False
        }

        response = self.client.post(
            reverse('habit:habit_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': [
                    'Нельзя выбрать одновременно связанную привычку и вознаграждение!'
                ]
            }
        )

    def test_execution_duration_validator(self):
        """Тест валидации на время выполнения действия 'length'"""
        self.client.force_authenticate(user=self.user)

        data = {
            'owner': self.user.pk,
            'place': 'Дом',
            'time': '07:00',
            'action': 'Зарядка',
            'is_pleasant': False,
            'period': 7,
            'reward': '1000 руб.',
            'length': 150,
            'is_public': False
        }

        response = self.client.post(
            reverse('habit:habit_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': [
                    'Время выполнения должно быть не больше 120 секунд!'
                ]
            }
        )

    def test_linked_habits_validator(self):
        """Тест валидации на то, что в связанные привычки
        могут попадать только привычки с признаком приятной привычки"""
        self.client.force_authenticate(user=self.user)

        data = {
            'owner': self.user.pk,
            'place': 'Дом',
            'time': '07:00',
            'action': 'Зарядка',
            'is_pleasant': False,
            'linked': self.habit2.pk,
            'period': 7,
            'length': 120,
            'is_public': False
        }

        response = self.client.post(
            reverse('habit:habit_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': [
                    'В связанные привычки могут попадать только привычки с признаком приятной привычки!'
                ]
            }
        )

    def test_pleasant_habit_validator(self):
        """Тест валидации на то, что у приятной привычки не может быть вознаграждения или связанной привычки"""
        self.client.force_authenticate(user=self.user)

        data = {
            'owner': self.user.pk,
            'place': 'Дом',
            'time': '07:00',
            'action': 'Зарядка',
            'is_pleasant': True,
            'period': 7,
            'reward': '1000 руб.',
            'length': 120,
            'is_public': False
        }

        response = self.client.post(
            reverse('habit:habit_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': [
                    'У приятной привычки не может быть вознаграждения или связанной привычки!'
                ]
            }
        )

    def test_period_validator_more_than_seven(self):
        """ Тест валидации на периодичность привычки реже чем 1 раз в неделю"""
        self.client.force_authenticate(user=self.user)

        data = {
            'owner': self.user.pk,
            'place': 'Дом',
            'time': '07:00',
            'action': 'Зарядка',
            'is_pleasant': False,
            'period': 8,
            'reward': '1000 руб.',
            'length': 120,
            'is_public': False
        }

        response = self.client.post(
            reverse('habit:habit_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': [
                    'Нельзя выполнять привычку реже, чем 1 раз в 7 дней!'
                ]
            }
        )

    def test_period_validator_less_than_one(self):
        """Тест валидации на периодичность привычки чаще чем 1 раз в день"""
        self.client.force_authenticate(user=self.user)

        data = {
            'owner': self.user.pk,
            'place': 'Дом',
            'time': '07:00',
            'action': 'Зарядка',
            'is_pleasant': False,
            'period': 0,
            'reward': '1000 руб.',
            'length': 120,
            'is_public': False
        }

        response = self.client.post(
            reverse('habit:habit_create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': [
                    'Периодичность не может быть меньше 1!'
                ]
            }
        )


class HabitDestroyTestCase(APITestCase):
    """TestCase на удаление привычки"""
    def setUp(self):
        self.user = User.objects.create(
            email='test@habit.com',
            password='test',
            tg_username='test'
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            place='Улица',
            time='19:00',
            action='Бег',
            is_pleasant=False,
            linked=None,
            period=7,
            reward='Снижение веса',
            length=120,
            is_public=False
        )

    def test_habit_delete(self):
        """Test на удаление привычки"""
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse('habit:habit_delete',
                    args=[self.habit.pk])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())


class HabitListTestCase(APITestCase):
    """TestCase на вывод списка привычек"""
    def setUp(self):
        self.user = User.objects.create(
            email='test@habit.com',
            password='test',
            tg_username='test'
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            place='Улица',
            time='19:00:00',
            action='Бег',
            is_pleasant=False,
            linked=None,
            period=7,
            reward='Снижение веса',
            length=120,
            is_public=False
        )

    def test_habit_list(self):
        """Test на вывод списка привычек"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('habit:habit_list'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.habit.id,
                        "place": self.habit.place,
                        "time": self.habit.time,
                        "action": self.habit.action,
                        "is_pleasant": self.habit.is_pleasant,
                        "period": self.habit.period,
                        "reward": self.habit.reward,
                        "length": self.habit.length,
                        "is_public": self.habit.is_public,
                        "last_dispatch_time": None,
                        "owner": self.habit.owner.pk,
                        "linked": self.habit.linked
                    }
                ]
            }
        )


class HabitListPublicTestCase(APITestCase):
    """TestCase на вывод списка публичных привычек"""
    def setUp(self):
        self.user = User.objects.create(
            email='test@habit.com',
            password='test',
            tg_username='test'
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            place='Улица',
            time='19:00:00',
            action='Бег',
            is_pleasant=False,
            linked=None,
            period=7,
            reward='Снижение веса',
            length=120,
            is_public=False
        )

    def test_habit_public_list(self):
        """Test на вывод списка публичных привычек"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('habit:habit_public_list'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            []
        )


class HabitRetrieveTestCase(APITestCase):
    """TestCase на вывод привычки"""
    def setUp(self):
        self.user = User.objects.create(
            email='test@habit.com',
            password='test',
            tg_username='test'
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            place='Улица',
            time='19:00:00',
            action='Бег',
            is_pleasant=False,
            linked=None,
            period=7,
            reward='Снижение веса',
            length=120,
            is_public=False
        )

    def test_habit_retrieve(self):
        """Test на вывод привычки"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('habit:habit_detail',
                    args=[self.habit.pk])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.habit.id,
                "place": self.habit.place,
                "time": self.habit.time,
                "action": self.habit.action,
                "is_pleasant": self.habit.is_pleasant,
                "period": self.habit.period,
                "reward": self.habit.reward,
                "length": self.habit.length,
                "is_public": self.habit.is_public,
                "last_dispatch_time": None,
                "owner": self.habit.owner.pk,
                "linked": self.habit.linked
            }
        )


class HabitUpdateTestCase(APITestCase):
    """TestCase на обновление привычки"""
    def setUp(self):
        self.user = User.objects.create(
            email='test@habit.com',
            password='test',
            tg_username='test'
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            place='Улица',
            time='19:00:00',
            action='Бег',
            is_pleasant=False,
            linked=None,
            period=7,
            reward='Снижение веса',
            length=110,
            is_public=False
        )

    def test_habit_update(self):
        """Test на обновление привычки"""
        self.client.force_authenticate(user=self.user)

        data = {
            'action': 'Подтягивания',
            'length': 30,
            'period': 3,
            'reward': '1000000$'
        }

        response = self.client.patch(
            reverse('habit:habit_update',
                    args=[self.habit.pk]),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": self.habit.pk,
                "place": self.habit.place,
                "time": self.habit.time,
                "action": "Подтягивания",
                "is_pleasant": self.habit.is_pleasant,
                "period": 3,
                "reward": "1000000$",
                "length": 30,
                "is_public": self.habit.is_public,
                "last_dispatch_time": None,
                "owner": self.habit.owner.pk,
                "linked": self.habit.linked
            }
        )
