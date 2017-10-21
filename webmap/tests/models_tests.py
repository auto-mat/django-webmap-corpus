"""Tests for the models of the webmap app."""
try:
    from django.urls import reverse
except ImportError:  # Django<2.0
    from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings

from django_admin_smoke_tests import tests


@override_settings(MEDIA_ROOT='webmap/tests')
class WebmapTests(TestCase):
    fixtures = ['test']

    def setUp(self):
                # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_admin_filter_load(self):
        """
        test if we can download KML of places
        """
        from webmap import views
        self.assertTrue(self.client.login(username='test_user', password='test'))
        response = self.client.get(reverse(views.kml_view, args=("l",)))
        print(response.content)
        self.assertContains(response, "<name>Place 1</name>", status_code=200)

    def test_search_view(self):
        """
        test if search view
        """
        from webmap import views
        self.assertTrue(self.client.login(username='test_user', password='test'))
        response = self.client.get(reverse(views.search_view, args=("asdf",)))
        print(response.content)
        self.assertContains(response, "<name>asdf</name>", status_code=200)

    def test_photo_preview_changelist(self):
        """
        test photo preview changelist
        """
        self.assertTrue(self.client.login(username='superuser', password='test'))
        response = self.client.get(reverse("admin:webmap_photo_changelist"))
        print(response.content)
        self.assertContains(response, "Fotka 1", status_code=200)
        self.assertContains(response, "210320151233.jpg.160x160_q85_detail.jpg", status_code=200)

    def test_photo_preview(self):
        """
        test photo preview
        """
        self.assertTrue(self.client.login(username='superuser', password='test'))
        response = self.client.get(reverse("admin:webmap_photo_change", args=(1,)))
        print(response.content)
        self.assertContains(response, "Fotka 1", status_code=200)
        self.assertContains(response, "210320151233.jpg.160x160_q85_detail.jpg", status_code=200)

    def test_admin_poi_sector_filter(self):
        """
        test sector filter in poi admin
        """
        self.assertTrue(self.client.login(username='superuser', password='test'))
        response = self.client.get("%s?sector=outer" % reverse("admin:webmap_poi_changelist"))
        self.assertContains(response, "asdf", status_code=200)
        self.assertContains(response, "Test marker", status_code=200)
        self.assertContains(response, "Test property", status_code=200)

        response = self.client.get("%s?sector=sector-1" % reverse("admin:webmap_poi_changelist"))
        self.assertContains(response, "Place 1", status_code=200)
        self.assertNotContains(response, "asdf", status_code=200)
        self.assertContains(response, "Test marker", status_code=200)

    def test_poi_with_gpx(self):
        """
        test uploading poi with GPX
        """
        self.assertTrue(self.client.login(username='superuser', password='test'))
        with open('webmap/tests/test_files/modranska-rokle.gpx', 'rb') as gpxfile:
            post_data = {
                'photos-TOTAL_FORMS': 0,
                'photos-INITIAL_FORMS': 0,
                'photos-MAX_NUM_FORMS': '',
                'name': 'Testing POI',
                'slug': 'testing-poi',
                'importance': 0,
                'geom': 'GEOMETRYCOLLECTION(POINT(0 0))',
                'licence': 0,
                'marker': 1,
                'status': 2,
                'gpx_file': gpxfile,
            }
            response = self.client.post(reverse("admin:webmap_poi_add"), post_data, follow=True)
        self.assertContains(response, "was added successfully", status_code=200)


class AdminTest(tests.AdminSiteSmokeTest):
        fixtures = ['test']
        exclude_apps = ['constance', ]
