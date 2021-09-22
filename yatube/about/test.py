from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()

    def test_author(self):
        # Создаем экземпляр клиента
        guest_client = Client()
        response = guest_client.get('/about/author/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200) 
    
    def test_tech(self):
        # Создаем экземпляр клиента
        guest_client = Client()
        response = guest_client.get('/about/tech/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200) 