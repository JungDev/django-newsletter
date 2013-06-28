from django.contrib.auth.models import User

from django.test import LiveServerTestCase

from webdriverplus import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumAdminTests(LiveServerTestCase):
    """ Selenium-based tests for the newsletter admin. """

    @classmethod
    def setUpClass(cls):
        cls.wd = WebDriver()

        # Poll the DOM for 5 seconds if elements are not initially found
        # Ref: http://docs.seleniumhq.org/docs/04_webdriver_advanced.jsp#implicit-waits
        cls.wd.implicitly_wait(5)

        super(SeleniumAdminTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.wd.quit()
        super(SeleniumAdminTests, cls).tearDownClass()

    def setUp(self):
        """ Make sure we're logged in as a superuser. """

        self.admin = \
            User.objects.create_user('test', 'test@testers.com', 'test')
        self.admin.is_staff = True
        self.admin.is_superuser = True
        self.admin.save()

        self.wd.get('%s%s' % (self.live_server_url, '/admin/'))

        # Conditional admin login
        if 'Log in' in self.wd.title:
            print 'logging in'
            username_input = self.wd.find(name="username")
            username_input.send_keys('test')
            password_input = self.wd.find(name="password")
            password_input.send_keys('test')

            self.assertTrue(
                self.wd.find(xpath='//input[@value="Log in"]').click())

            print 'logged in'

        print self.wd.title

    def test_login(self):
        """ Test whether login succeeded. """

        self.assertEquals(
            'Site administration | Django site admin',
            self.wd.title
        )

    def test_modules(self):
        """ Test for presence of admin modules. """

        self.assertTrue(self.wd.find(link_text='Newsletter'))

        self.assertTrue(self.wd.find(link_text='Newsletter'))
        self.assertTrue(self.wd.find(link_text='Messages'))
        self.assertTrue(self.wd.find(link_text='Newsletters'))
        self.assertTrue(self.wd.find(link_text='Submissions'))
        self.assertTrue(self.wd.find(link_text='Subscriptions'))

    def test_addnewsletter(self):
        """ Test adding a newsletter. """

        # Go to newsletters view
        self.assertTrue(self.wd.find(link_text='Newsletters').click())
        self.assertEquals(
            self.wd.title,
            "Select newsletter to change | Django site admin"
        )

        self.wd.find(link_text='Add newsletter').click()
        self.assertEquals(
            self.wd.title,
            "Add newsletter | Django site admin"
        )

        # Fill in the newsletter form
        form = self.wd.find(tag_name='form')
        form.find(name='title').send_keys('Test newsletter')
        form.find(name='email').send_keys('test@test.com')
        form.find(name='sender').send_keys('Test sender')

        # Submit the form
        self.assertTrue(form.submit())

        # Confirm save result
        self.assertTrue(self.wd.find(text_contains='added successfully'))
        self.assertTrue(self.wd.find(link_text='Test newsletter'))

    def test_addsubscription(self):
        """ Test adding a subscription to a newsletter. """

        # Make sure a newsletter is created
        self.test_addnewsletter()

        # Go back to main admin page
        self.wd.get('%s%s' % (self.live_server_url, '/admin/'))

        # Open add subscription form
        self.assertTrue(self.wd.find(link_text='Subscriptions').click())
        self.assertTrue(self.wd.find(link_text='Add subscription').click())

        self.assertEquals(
            self.wd.title,
            "Add subscription | Django site admin"
        )

        # Fill in form
        form = self.wd.find(tag_name='form')
        form.find(name='name_field').send_keys('Test subscriber')
        form.find(name='email_field').send_keys('test_subscriber@test.com')

        form.find(name='newsletter').find(text='Test newsletter').click()
        form.find(name='subscribed').click()

        # Submit the form
        self.assertTrue(form.submit())

        # Confirm save results
        self.assertTrue(self.wd.find(text_contains='added successfully'))
        self.assertTrue(self.wd.find(link_text='Test subscriber'))

    def test_addmessage(self):
        """ Test adding a message to a newsletter. """

        # Make sure a newsletter is created
        self.test_addnewsletter()

        # Go back to main admin page
        self.wd.get('%s%s' % (self.live_server_url, '/admin/'))

        # Open add form
        self.assertTrue(self.wd.find(link_text='Messages').click())

        self.assertTrue(self.wd.find(link_text='Add message').click())

        self.assertEquals(
            self.wd.title,
            "Add message | Django site admin"
        )

        # Fill in form
        form = self.wd.find(tag_name='form')
        form.find(name='title').send_keys('Test message')
        form.find(name='newsletter').find(text='Test newsletter').click()

        # Setup the first article
        form.find(name='articles-0-title').click().send_keys(
            'Test article title 1')
        form.find(name='articles-0-text').click().send_keys(
            'Test text 1')

        # Open hidden link tab and fill in URL
        form.find(id='fieldsetcollapser0').click()
        form.find(name='articles-0-url').click().send_keys(
            'http://www.google.com')

        # Setup the second article
        form.find(name='articles-1-title').click().send_keys(
            'Test article title 2')
        form.find(name='articles-1-text').click().send_keys(
            'Test text 2')

        # Submit the form
        self.assertTrue(form.submit())

        # Confirm save results
        self.assertTrue(self.wd.find(text_contains='added successfully'))
        self.assertTrue(self.wd.find(link_text='Test message'))

    def test_previewaddsubmission(self):
        """ Test previewing a message and creating submission. """

        # Create a message first
        self.test_addmessage()

        # Create a subscription
        # Go back to main admin page
        self.wd.get('%s%s' % (self.live_server_url, '/admin/'))

        # Open add subscription form
        self.assertTrue(self.wd.find(link_text='Subscriptions').click())
        self.assertTrue(self.wd.find(link_text='Add subscription').click())

        # Fill in form
        form = self.wd.find(tag_name='form')
        form.find(name='name_field').send_keys('Test subscriber')
        form.find(name='email_field').send_keys('test_subscriber@test.com')

        form.find(name='newsletter').find(text='Test newsletter').click()
        form.find(name='subscribed').click()

        # Submit the form
        self.assertTrue(form.submit())

        # Go back to main admin page
        self.wd.get('%s%s' % (self.live_server_url, '/admin/'))

        # Open change form
        self.assertTrue(self.wd.find(link_text='Messages').click())
        self.assertTrue(self.wd.find(link_text='Test message').click())

        self.assertEquals(
            self.wd.title,
            "Change message | Django site admin"
        )

        self.assertTrue(self.wd.find(link_text='Preview').click())
        self.assertEquals(
            self.wd.title,
            "Preview message | Django site admin"
        )
        self.assertTrue(self.wd.find(text_contains='Test message'))
        self.assertTrue(self.wd.find(text_contains='Test newsletter'))

        # Create a submission
        self.assertTrue(self.wd.find(link_text='Create submission').click())
        self.assertEquals(
            self.wd.title,
            "Change submission | Django site admin"
        )

        # Save submission
        self.assertTrue(self.wd.find(tag_name='form').submit())

        # Confirm save results
        self.assertTrue(self.wd.find(text_contains='successfully'))

        # Go back to submission
        self.assertTrue(self.wd.find(link_text='Test message').click())

        # Confirm presence of test submission
        self.assertEquals(
            self.wd.find(name='subscriptions').find(tag_name='option').text,
            u'Test subscriber <test_subscriber@test.com> to Test newsletter')
