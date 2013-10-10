"""

"""

import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Project imports
from pages import helpers
import base
import util
import config


class ForkTests2(unittest.TestCase):
    """This test case is for testing the act of creating a fork, and consistency
    between a fork and its original node.
    """

    _project = lambda self: helpers.get_new_project()

    def _subproject(self):
        """ Create and return a (sub)project which is the child of a project.

        The ``current_url`` of the driver is the subproject's overview.
        """
        return self._project().add_component(
            title='New Subproject',
            component_type='Project',
        )

    def _test_fork_list(self, page):
        """ Given a project, register it and verify that the new registration is
         in the project's registration list
        """
        _url = page.driver.current_url

        page = page.fork()

        page.driver.get(_url)

        try:
            return page.forks
        finally:
            page.close()

    def test_project_fork_listed(self):
        """After forking a project, the fork should be listed in the original
        project's Forks pane."""
        forks = self._test_fork_list(page=self._project())
        self.assertEqual(len(forks), 1)

    def test_subproject_fork_listed(self):
        """After forking a project, the fork should be listed in the original
        project's Forks pane."""
        forks = self._test_fork_list(page=self._subproject())
        self.assertEqual(len(forks), 1)

    def test_project_fork_list_title(self):
        """After forking a project, the fork should show the correct title in
        the project's Forks pane.
        """
        page = self._project()
        title = page.title

        self.assertEqual(
            self._test_fork_list(
                page=page
            )[0].title,
            'Fork of {}'.format(title),
        )

    def test_subproject_fork_list_title(self):
        """Subproject variant of ``self.test_project_fork_list_title``"""
        page = self._subproject()
        title = page.title

        self.assertEqual(
            self._test_fork_list(
                page=page
            )[0].title,
            'Fork of {}'.format(title),
        )

    def _test_fork_matches(self, page, attribute):
        """Given a project, fork it and verify that the attribute provided
         matches between the project and its fork.

         Note that the value of the project's attribute is stored before the
         project is forked, as the act of forking may otherwise change the
         state - for example, project's fork should include its log *before*
         the project was forked.
        """
        parent_value = getattr(page, attribute)

        page = page.fork()

        self.assertEqual(
            getattr(page, attribute),
            parent_value,
        )

        page.close()

    def test_project_fork_components(self):
        """Verify that a fork's (non-empty) component list matches the original
        project"""
        page = self._project()

        # add component
        page = page.add_component(
            title='Test Component',
            component_type='Other',
        )

        page = page.parent_project()

        # add a subproject
        page = page.add_component(
            title='Test Subproject',
            component_type='Project',
        )

        page = page.parent_project()

        self._test_fork_matches(
            page=page,
            attribute='component_names'
        )

    def test_subproject_fork_components(self):
        """Subproject variant of ``self.test_project_fork_components``"""
        page = self._subproject()

        # add component
        page = page.add_component(
            title='Test Component',
            component_type='Other',
        )

        page = page.parent_project()

        self._test_fork_matches(
            page=page,
            attribute='component_names'
        )

    @unittest.skip('test not implemented')
    def test_project_fork_contributors(self):
        """Verify that a fork's contributor list matches the original project"""
        pass


    @unittest.skip('test not implemented')
    def test_subproject_fork_contributors(self):
        """Subproject variant of ``self._test_project_fork_contributors``"""
        pass


    def test_project_fork_wiki_home(self):
        """ Verify that a fork's wiki homepage content matches the original
        project """
        page = self._project()

        page.set_wiki_content('Test wiki content!')

        self._test_fork_matches(
            page=page,
            attribute='wiki_home_content'
        )

    def test_subproject_fork_wiki_home(self):
        """Subproject variant of ``self.test_project_fork_wiki_home``"""
        page = self._subproject()

        page.set_wiki_content('Test wiki content!')

        self._test_fork_matches(
            page=page,
            attribute='wiki_home_content'
        )

    def _test_fork_logged(self, page):
        """ Given a project, register it and verify that the action appears in
        the original project's logs.
        """
        user = page.contributors[0]

        original_node_url = page.driver.current_url
        title = page.title

        page = page.fork()

        self.assertEqual(
            page.logs[0].text,
            u'{user} created fork from project {title}'.format(
                user=user.full_name,
                title=title
            )
        )

        self.assertEqual(
            [x.url.rstrip('/') for x in page.logs[0].links],
            [
                user.profile_url.rstrip('/'),
                original_node_url.rstrip('/')
            ]

        )

        page.close()

    @unittest.skip('known issue')
    def test_project_fork_logged(self):
        """ Project variant of ``self._test_fork_logged``

        NOTE: This test is known to fail due to an error in the log template,
        as of 8 Sep 2013.
        """
        self._test_fork_logged(self._project())

    @unittest.skip('known issue')
    def test_subproject_fork_logged(self):
        """ Subproject variant of ``self._test_fork_logged`` """
        # TODO: This fails right now because a subproject is referred to as a
        # "node" in the log.
        self._test_fork_logged(self._subproject())

    def _test_fork_counter_decrement(self, page):
        _url = page.driver.current_url
        num_forks = page.num_forks

        page.fork()
        page.delete()

        page.driver.get(_url)

        self.assertEqual(
            page.num_forks,
            num_forks,
        )

        page.close()

    def test_project_fork_counter_decrement(self):
        self._test_fork_counter_decrement(self._project())

    def test_subproject_fork_counter_decrement(self):
        self._test_fork_counter_decrement(self._subproject())



class ForkTests(base.ProjectSmokeTest):

    def setUp(self):

        # setUp
        super(ForkTests, self).setUp()

    def test_not_fork_a_component(self):
        """
        test to make sure can't fork a component

        """
        #create a component
          # Click New Node button
        self.driver.find_element_by_link_text('Add Component').click()

        # Get form
        form = self.driver.find_element_by_xpath(
        '//form[contains(@action, "newnode")]'
        )

        # Wait for modal to stop moving
        WebDriverWait(self.driver, 3).until(
            ec.visibility_of_element_located(
                (By.CSS_SELECTOR, 'input[name="title"]')
            )
        )

        # Fill out form
        util.fill_form(
            form,
            {
                'input[name="title"]' : config.node_title,
                '#category' : 'Procedure',
            }
        )

        #check the fork option
        self.driver.find_element_by_css_selector("li span a").click()
        discrib=self.get_element('a[data-original-title="Number of times this node has been forked (copied)"]')\
            .text
        self.assertEqual(discrib, u' 0')

    def tearDown(self):
        # Close WebDriver
        self.driver.close()

# Run tests
if __name__ == '__main__':
    unittest.main()
