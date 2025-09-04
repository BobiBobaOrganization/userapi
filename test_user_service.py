import unittest
from uuid import uuid4
from datetime import date
from src.services.users_storage import User
from src.services.users_service import UserService

class TestUserService(unittest.TestCase):
    __id__ = uuid4();
    
    def setUp(self):
        # Ініціалізація, перед тим як кожен тест буде запущений
        self.user_service = UserService()
        # Додавання тестового користувача
        self.user_service.create_user(User(id=self.__id__, email="test3@example.com"))

    def test_add_user(self):
        # Перевірка чи доданий користувач є в сховищі
        user = self.user_service.get_user(self.__id__)
        self.assertEqual(user.email, "test3@example.com")

    def test_get_user(self):
        # Перевірка чи метод повертає правильного користувача
        user = self.user_service.get_user(self.__id__)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.__id__)

    def test_user_not_found(self):
        # Перевірка на те, що повернеться None для неіснуючого користувача
        user = self.user_service.get_user(999)
        self.assertIsNone(user)

if __name__ == "__main__":
    unittest.main()
