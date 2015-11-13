"""Tests for the models of the webmap app."""
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


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

    def test_admin_views(self):
        """
        test if we can see all admin pages
        """
        self.assertTrue(self.client.login(username='test_user', password='top_secret'))
        response = self.client.get(reverse("admin:webmap_baselayer_changelist"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("admin:webmap_legend_changelist"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("admin:webmap_license_changelist"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("admin:webmap_mappreset_changelist"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("admin:webmap_marker_changelist"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("admin:webmap_overlaylayer_changelist"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("admin:webmap_photo_changelist"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("admin:webmap_poi_changelist"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("admin:webmap_property_changelist"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("admin:webmap_sector_changelist"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("admin:webmap_status_changelist"))
        self.assertEqual(response.status_code, 200)
