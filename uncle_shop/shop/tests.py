from django.test import TestCase, override_settings
from django.urls import reverse


class CanonicalSeoTests(TestCase):
    def test_page_includes_preferred_canonical_url(self):
        response = self.client.get(reverse("about"), HTTP_HOST="causeofjoybuilders.com")

        self.assertContains(
            response,
            '<link rel="canonical" href="https://causeofjoybuilders.com/about/">',
            html=True,
        )

    def test_canonical_url_ignores_tracking_query_parameters(self):
        response = self.client.get(
            f"{reverse('services')}?utm_source=google",
            HTTP_HOST="causeofjoybuilders.com",
        )

        self.assertContains(
            response,
            '<link rel="canonical" href="https://causeofjoybuilders.com/services/">',
            html=True,
        )

    @override_settings(
        CANONICAL_HOST="causeofjoybuilders.com",
        CANONICAL_SCHEME="https",
        CANONICAL_HOST_REDIRECTS=[
            "www.causeofjoybuilders.com",
            "nd-production-42eb.up.railway.app",
        ],
    )
    def test_duplicate_production_hosts_redirect_to_canonical_host(self):
        response = self.client.get(
            f"{reverse('contact')}?ref=google",
            HTTP_HOST="www.causeofjoybuilders.com",
        )

        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response["Location"],
            "https://causeofjoybuilders.com/contact/?ref=google",
        )
