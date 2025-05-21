from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class TestUserModel(TestCase):

    def setUp(self):
        # ایجاد یک کاربر نمونه برای تست
        self.user = User.objects.create_user(
            username='testuser',
            phone='1234567890',
            email='test@example.com',
            password1='StrongPassword123',
            password2='StrongPassword123',
            role='USER',
            is_active=True
        )

    def test_user_creation(self):
        """تست ایجاد کاربر با داده‌های معتبر"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.phone, '1234567890')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.role, 'USER')
        self.assertTrue(self.user.is_active)

    def test_user_string_representation(self):
        """تست نمایش متنی مدل کاربر"""
        self.assertEqual(str(self.user), 'test@example.com (USER)')

    def test_unique_email(self):
        """تست یکتایی ایمیل"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='duplicateuser',
                phone='0987654321',
                email='test@example.com',  # ایمیل تکراری
                password1='AnotherPass123',
                password2='AnotherPass123'
            )

    def test_unique_phone(self):
        """تست یکتایی شماره تلفن"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='phoneuser',
                phone='1234567890',  # شماره تلفن تکراری
                email='unique@example.com',
                password1='UniquePass123',
                password2='UniquePass123'
            )
