from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .forms import CreationForm

User = get_user_model()


class CreationFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = CreationForm()

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованный клиент
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        # Создаем клиент-автор
        self.author_client = Client()
        self.author_client.force_login(self.user)

    def test_create_user(self):
        user_count = User.objects.count()

        form_data = {
            'first_name': 'First',
            'last_name': 'Last',
            'username': 'usrnm',
            'email': 'eml@eml.inl',
            'password1': 'p@$sworD',
            'password2': 'p@$sworD',
        }

        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )

        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse('posts:index'))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(User.objects.count(), user_count + 1)
        # Проверяем, что создалась запись с заданным слагом
        self.assertTrue(
            User.objects.filter(
                first_name='First',
                last_name='Last',
                username='usrnm',
                email='eml@eml.inl',
            ).exists()
        )
