from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve('/')
        assert found.func == home_page
