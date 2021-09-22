from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.form = PostForm()
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTests.user)

    def test_title_label(self):
        expected_labels = {
            'text': 'Текст',
            'group': 'Группа',
        }
        for label_name, label in expected_labels.items():
            with self.subTest(lebel_name=label_name):
                title_label = PostFormTests.form.fields[label_name].label
                self.assertTrue(title_label, label)

    def test_title_help_text(self):
        expected_help_texts = {
            'text': ('Это текст вашего поста'),
            'group': ('Укажите группу, к которой будет относится ваш пост'),
        }
        for label_name, text in expected_help_texts.items():
            with self.subTest(lebel_name=label_name):
                title_help_text = PostFormTests.form.fields[label_name]
                self.assertTrue(title_help_text, text)

    def test_create_post(self):
        post_count = Post.objects.count()

        form_data = {
            'text': 'Тестовый текст',
            'group': PostFormTests.group.id
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': 'auth'}
        ))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), post_count + 1)
        # Проверяем, что создалась запись с заданным слагом
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                group=PostFormTests.group
            ).exists()
        )

    def test_edit_post(self):
        post_id = Post.objects.first().id
        form_data = {
            'text': 'Тестовый текст 1',
            'group': PostFormTests.group.id
        }

        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post_id}),
            data=form_data,
            follow=True
        )

        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse(
            'posts:post_detail',
            kwargs={'post_id': post_id}
        ))
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст 1',
                group=PostFormTests.group
            ).exists()
        )
