import datetime

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from wagtail.wagtailcore.models import Page, Site

from portal_pages.models import (
    MarketplaceIndexPage, MarketplaceEntryPage,
    CaseStudyIndexPage, CaseStudyPage,
    BlogIndexPage, BlogPage
    )

from portal_pages.forms import CaseStudyForm


class UserFormTests(TestCase):

    def setUp(self):
        # Wagtail's default site comes with a Root (1) and Home Page (2)
        self.default_site = Site.objects.get(is_default_site=True)        
        self.root = Page.objects.get(pk=1)
        self.home_page = Page.objects.get(pk=2)

        # Add a marketplace index page under the home page
        self.marketplace_index_page = self.home_page.add_child(
            instance=MarketplaceIndexPage(
                title="Marketplace",
                slug="marketplace",
                live=True,
            ))
        self.marketplace_submission_url = self.marketplace_index_page.url + self.marketplace_index_page.reverse_subpage('submit')

        self.marketplace_entry_form_data = { 
            'date_start': '2015-01-01',
            'title': 'new marketplace',
            'biography': '<p>bio</p>',
            # spambuster/honeypot fields
            'email_field_email': '',
            'company_company_email': 'nine'
        }

        # Add a case study index page under the home page
        self.case_study_index_page = self.home_page.add_child(
            instance=CaseStudyIndexPage(
                title="Stories",
                slug="stories",
                live=True,
            ))
        self.case_study_submission_url = self.case_study_index_page.url + self.case_study_index_page.reverse_subpage('submit')

        self.case_study_form_data = { 
            'date': '2015-01-01',
            'month_start': 12,
            'year_start': 2014,
            'title': 'new case study',
            'summary': '<p>summary</p>',
            # spambuster/honeypot fields
            'email_field_email': '',
            'company_company_email': 'nine'
        }

        # Add a blog index page under the home page
        self.blog_index_page = self.home_page.add_child(
            instance=BlogIndexPage(
                title="Blog",
                slug="blog",
                live=True,
            ))
        self.blog_submission_url = self.blog_index_page.url + self.blog_index_page.reverse_subpage('submit')

        self.blog_form_data = { 
            'date': '2015-01-01',
            'title': 'new blog',
            'body': '<p>body</p>',
            'submitter_email': 'fakeone@caktusgroup.com',
            # spambuster/honeypot fields
            'email_field_email': '',
            'company_company_email': 'nine'
        }

    def test_marketplace_entry_form_valid(self):
        # This should successfully add a single new marketplace entry
        resp = self.client.post(self.marketplace_submission_url, self.marketplace_entry_form_data)
        self.assertEqual(resp.status_code, 302)
        expected_redirect = self.marketplace_index_page.url + self.marketplace_index_page.reverse_subpage('thanks')
        self.assertRedirects(resp, expected_redirect)
        self.assertEqual(MarketplaceEntryPage.objects.all().count(), 1)

    def test_marketplace_entry_form_invalid_honeypot(self):
        # This should throw an ValidationError and not add the entry
        self.marketplace_entry_form_data['company_company_email'] = 'Iamabot@bots.com'
        resp = self.client.post(self.marketplace_submission_url, self.marketplace_entry_form_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)
        form = resp.context['form']
        self.assertEqual(len(form.errors), 1)
        self.assertTrue('__all__' in form.errors)
        self.assertEqual(form.errors['__all__'], ['Invalid submission'])
        self.assertEqual(MarketplaceEntryPage.objects.all().count(), 0)

    def test_marketplace_entry_good_image(self):
        test_file = open('portal_pages/tests/files/goodimage.jpg', 'rb')
        good_image = SimpleUploadedFile(test_file.name, test_file.read())
        self.marketplace_entry_form_data['file'] = good_image
        resp = self.client.post(self.marketplace_submission_url, self.marketplace_entry_form_data)
        self.assertEqual(resp.status_code, 302)
        expected_redirect = self.marketplace_index_page.url + self.marketplace_index_page.reverse_subpage('thanks')
        self.assertRedirects(resp, expected_redirect)

    def test_marketplace_entry_bad_image_type(self):
        test_file = open('portal_pages/tests/files/badimage.bmp', 'rb') # File types accepted are GIF/JPG/PNG, this should error
        good_image = SimpleUploadedFile(test_file.name, test_file.read())
        self.marketplace_entry_form_data['file'] = good_image
        resp = self.client.post(self.marketplace_submission_url, self.marketplace_entry_form_data)
        self.assertEqual(resp.status_code, 200)
        logo_form = resp.context["logo_form"]
        self.assertFalse(logo_form.is_valid())
        self.assertEqual(logo_form.errors["file"], ["Not a supported image format. Supported formats: GIF, JPEG, PNG."])
        self.assertTrue(logo_form.errors["file"][0] in str(resp.content)) # Check that the user sees this error message

    def test_marketplace_entry_animated_gif(self):
        test_file = open('portal_pages/tests/files/animated.gif', 'rb') # Animated gifs are not supported, this should error
        good_image = SimpleUploadedFile(test_file.name, test_file.read())
        self.marketplace_entry_form_data['file'] = good_image
        resp = self.client.post(self.marketplace_submission_url, self.marketplace_entry_form_data)
        self.assertEqual(resp.status_code, 200)
        logo_form = resp.context["logo_form"]
        self.assertFalse(logo_form.is_valid())
        self.assertEqual(logo_form.errors["file"], ["Animated GIFs are not supported."])
        self.assertTrue(logo_form.errors["file"][0] in str(resp.content)) # Check that the user sees this error message

    def test_case_study_form_valid(self):
        # This should successfully add a single new case study
        resp = self.client.post(self.case_study_submission_url, self.case_study_form_data)
        self.assertEqual(resp.status_code, 302)
        expected_redirect = self.case_study_index_page.url + self.case_study_index_page.reverse_subpage('thanks')
        self.assertRedirects(resp, expected_redirect)
        self.assertEqual(CaseStudyPage.objects.all().count(), 1)
        case_study_page = CaseStudyPage.objects.all()[0]
        # The original date should have been overriden by month_start/year_start
        self.assertEqual(case_study_page.date, datetime.date(self.case_study_form_data['year_start'], self.case_study_form_data['month_start'], 1))

    def test_case_study_form_invalid_honeypot(self):        
        self.case_study_form_data['email_field_email'] = 'notnine'
        resp = self.client.post(self.case_study_submission_url, self.case_study_form_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)
        form = resp.context['form']
        self.assertEqual(len(form.errors), 1)
        self.assertTrue('__all__' in form.errors)
        self.assertEqual(form.errors['__all__'], ['Invalid submission'])
        self.assertEqual(MarketplaceEntryPage.objects.all().count(), 0)
        self.assertEqual(CaseStudyPage.objects.all().count(), 0)

    def test_case_study_invalid_bad_email(self):
        self.case_study_form_data['submitter_email'] = 'invalid@nope'
        resp = self.client.post(self.case_study_submission_url, self.case_study_form_data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context[0]['form'].errors['submitter_email'], ['Enter a valid email address.'])
        self.assertEqual(CaseStudyPage.objects.all().count(), 0)

    def test_case_study_form(self):
        # Add 2 Marketplace Entry Pages, one published, one unpublished.
        # Only the published one should show up in the queryset
        mpe_published = self.marketplace_index_page.add_child(
                            instance=MarketplaceEntryPage(
                                title="published",
                                slug="published",
                                date_start="2015-05-01",
                                live=True,
                                biography='<p>bio test</p>',
                            ))
        mpe_unpublished = self.marketplace_index_page.add_child(
                            instance=MarketplaceEntryPage(
                                title="unpublished",
                                slug="unpublished",
                                date_start="2015-05-01",
                                live=False,
                                biography='<p>bio test</p>',
                            ))

        form = CaseStudyForm()
        self.assertEqual(form.fields['marketplace_entry'].queryset[0].name, "published")
        self.assertEqual(len(form.fields['marketplace_entry'].queryset), 1)

    def test_blog_form_valid(self):
        # This should successfully add a single new blog post
        resp = self.client.post(self.blog_submission_url, self.blog_form_data)
        self.assertEqual(resp.status_code, 302)
        expected_redirect = self.blog_index_page.url + self.blog_index_page.reverse_subpage('thanks')
        self.assertRedirects(resp, expected_redirect)
        self.assertEqual(BlogPage.objects.all().count(), 1)

    def test_blog_form_invalid_honeypot(self):        
        self.blog_form_data['email_field_email'] = 'notnine'
        resp = self.client.post(self.blog_submission_url, self.blog_form_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)
        form = resp.context['form']
        self.assertEqual(len(form.errors), 1)
        self.assertTrue('__all__' in form.errors)
        self.assertEqual(form.errors['__all__'], ['Invalid submission'])
        self.assertEqual(MarketplaceEntryPage.objects.all().count(), 0)
        self.assertEqual(BlogPage.objects.all().count(), 0)

    def test_blog_form_invalid_bad_email(self):
        self.blog_form_data['submitter_email'] = 'invalid@nope'
        resp = self.client.post(self.blog_submission_url, self.blog_form_data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context[0]['form'].errors['submitter_email'], ['Enter a valid email address.'])
        self.assertEqual(BlogPage.objects.all().count(), 0)
