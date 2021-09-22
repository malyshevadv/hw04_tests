from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostsViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostsViewsTest.user)

        self.username = PostsViewsTest.user.username

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': PostsViewsTest.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': self.username}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': PostsViewsTest.post.pk}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': PostsViewsTest.post.pk}
            ): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        # Проверяем для name вызывается соответствующий HTML-шаблон
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


class ContextPaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.group2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='test_slug2',
            description='Тестовое описание 2',
        )
        cls.posts = []
        for i in range(13):
            cls.posts.append(
                Post.objects.create(
                    author=cls.user,
                    text='Тестовый текст',
                    group=cls.group,
                )
            )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(ContextPaginatorViewsTest.user)
        self.username = ContextPaginatorViewsTest.user.username

        self.paginator_link_list = [
            reverse('posts:index'),
            reverse(
                'posts:group_list',
                kwargs={'slug': ContextPaginatorViewsTest.group.slug}
            ),
            reverse(
                'posts:profile',
                kwargs={'username': self.username}
            ),
        ]

    def test_first_page_contains_ten_records(self):
        """Проверка что первая страница содержит 10 записей"""
        for reverse_name in self.paginator_link_list:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                # Проверка: количество постов на первой странице равно 10.
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        """Проверка что вторая страница содержит 3 записи"""
        for reverse_name in self.paginator_link_list:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 3)

    def test_post_list_page_show_correct_context(self):
        """Проверка контекста страниц со списками."""
        for reverse_name in self.paginator_link_list:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)

                first_object = response.context['page_obj'][0]
                post_author_0 = first_object.author.username
                post_text_0 = first_object.text
                post_group_0 = first_object.group.title
                post_date_0 = first_object.pub_date
                self.assertEqual(post_author_0, self.username)
                self.assertEqual(post_text_0, 'Тестовый текст')
                self.assertEqual(post_group_0, 'Тестовая группа')
                self.assertIsInstance(post_date_0, datetime)

    def test_post_detail_page_show_correct_context(self):
        post_id = ContextPaginatorViewsTest.posts[0].pk
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': post_id})
        )
        post = response.context.get('post')
        self.assertEqual(post.author.username, self.username)
        self.assertEqual(post.text, 'Тестовый текст')
        self.assertEqual(post.group.title, 'Тестовая группа')
        self.assertIsInstance(post.pub_date, datetime)

    def test_post_form_correct_context(self):
        post_id = ContextPaginatorViewsTest.posts[0].pk
        pages_to_test = [
            reverse(
                'posts:post_edit',
                kwargs={'post_id': post_id}
            ),
            reverse('posts:post_create'),
        ]
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for reverse_name in pages_to_test:
            for value, expected in form_fields.items():
                with self.subTest(reverse_name=reverse_name, value=value):
                    response = self.authorized_client.get(reverse_name)
                    form_field = response.context.get('form').fields.get(value)
                    self.assertIsInstance(form_field, expected)

    def test_new_post_with_group_added(self):
        links_to_test_list = [
            reverse('posts:index'),
            reverse(
                'posts:group_list',
                kwargs={'slug': ContextPaginatorViewsTest.group2.slug}
            ),
            reverse(
                'posts:profile',
                kwargs={'username': self.username}
            ),
        ]

        new_post = Post.objects.create(
            author=ContextPaginatorViewsTest.user,
            text='Тестовый текст',
            group=ContextPaginatorViewsTest.group2,
        )
        for reverse_name in links_to_test_list:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertIn(new_post, response.context['page_obj'])

        response = self.authorized_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': ContextPaginatorViewsTest.group.slug}
            )
        )
        self.assertNotIn(new_post, response.context['page_obj'])
