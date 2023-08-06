"Test for compatibility with django.contrib.auth.base_user.AbstractBaseUser"
from django.test import TestCase

from djangolovessandstorm.models import SandstormUser

ID1 = "01234567890123456789012345678901"
HANDLE1 = "alice"
NAME1 = "Alice Dev Admin"


class DLSAbstractBaseUserTest(TestCase):
    def setUp(self):
        SandstormUser.objects.create(id=ID1, handle=HANDLE1, name=NAME1)

    def test_password(self):
        # Sandstorm users do not have passwords.
        user = SandstormUser.objects.get(pk=ID1)
        self.assertRaises(AttributeError, getattr, user, "password")

    def test_last_login(self):
        # Django does not know when users log in.
        user = SandstormUser.objects.get(pk=ID1)
        self.assertRaises(AttributeError, getattr, user, "last_login")

    def test_is_active(self):
        # Sandstorm users are always able to log in.
        user = SandstormUser.objects.get(pk=ID1)
        self.assertTrue(user.is_active)

    def test_str(self):
        # If str() is used for display, this should show the name.
        user = SandstormUser.objects.get(pk=ID1)
        self.assertEqual(str(user), NAME1)

    def test_save(self):
        uid = ("12345123451234512345123451234512",)
        sessionkey = (
            "1234512345123451234512345123451234512345123451234512345123451234"
        )
        sandstormname = "Old Name"
        sandstormhandle = "Old Handle"
        SandstormUser.objects.create(
            pk=uid,
            handle=sandstormhandle,
            name=sandstormname,
            session_key=sessionkey,
        )
        user1 = SandstormUser.objects.get(pk=uid)
        newname = "New Name"
        user1.name = newname
        newhandle = "New Handle"
        user1.handle = newhandle
        newsession_key = "0987654321"
        user1.session_key = newsession_key
        user1.save()
        user2 = SandstormUser.objects.get(pk=uid)
        self.assertEqual(user2.name, newname)
        self.assertEqual(user2.handle, newhandle)
        self.assertEqual(user2.session_key, newsession_key)
