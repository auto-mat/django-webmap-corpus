"""Tests for the models of the webmap app."""
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django_admin_smoke_tests import tests


class WebmapTests(TestCase):
    fixtures = ['test']

    def setUp(self):
                # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username='test_user', email='test_user@test_user.com', password='top_secret')
        self.user.save()

    def test_admin_filter_load(self):
        """
        test if we can download KML of places
        """
        from webmap import views
        self.assertTrue(self.client.login(username='test_user', password='top_secret'))
        response = self.client.get(reverse(views.kml_view, args=("l",)))
        self.assertEqual(response.status_code, 200)

    def test_search_view(self):
        """
        test if search view
        """
        from webmap import views
        self.assertTrue(self.client.login(username='test_user', password='top_secret'))
        response = self.client.get(reverse(views.search_view, args=("asdf",)))
        self.assertEqual(response.status_code, 200)


class AdminTest(tests.AdminSiteSmokeTest):
        fixtures = ['test']
        exclude_apps = ['constance', ]
