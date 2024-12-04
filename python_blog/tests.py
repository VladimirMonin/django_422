"""
Документация для тестов Django приложения

Файл tests.py содержит тестовые случаи для проверки работоспособности основного представления (view).

Структура тестов:
1. MainViewTests - основной тестовый класс, наследующий TestCase
   - setUp(): метод, выполняющийся перед каждым тестом
     * инициализирует тестовый клиент для выполнения HTTP-запросов

   - test_main_view_with_name(): тестовый метод
     * проверяет ответ сервера на GET-запрос к URL '/test/'
     * проверяет код ответа (должен быть 200)
     * проверяет содержимое ответа (должно быть 'Привет test!')

   - test_main_view_with_different_name(): тестовый метод
     * проверяет ответ сервера на GET-запрос к URL '/python/'
     * проверяет код ответа (должен быть 200)
     * проверяет содержимое ответа (должно быть 'Привет python!')

Примечания:
- Используется встроенный тестовый клиент Django
- Проверяется корректность ответов для разных URL-путей
- Тесты проверяют как статус ответа, так и его содержимое
- Кодировка ответа поддерживает кириллицу
"""

from django.test import TestCase, Client
from django.urls import reverse

class MainViewTests(TestCase):
    """
    Тестовый класс для проверки основного представления.
    
    Методы:
        setUp(): Инициализирует тестовое окружение перед каждым тестом.
        test_main_view_with_name(): Проверяет ответ view для URL '/test/'.
        test_main_view_with_different_name(): Проверяет ответ view для URL '/python/'.
    """
    
    def setUp(self):
        """Создает тестовый клиент перед каждым тестовым методом."""
        self.client = Client()
    
    def test_main_view_with_name(self):
        """
        Тестирует view с параметром 'test'.
        
        Проверяет:
        - HTTP статус код (200)
        - Содержимое ответа ('Привет test!')
        """
        response = self.client.get('/test/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'Привет test!')
    
    def test_main_view_with_different_name(self):
        """
        Тестирует view с параметром 'python'.
        
        Проверяет:
        - HTTP статус код (200)
        - Содержимое ответа ('Привет python!')
        """
        response = self.client.get('/python/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'Привет python!')