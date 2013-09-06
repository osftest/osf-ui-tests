import unittest

from pages import helpers, ProjectPage, LoginPage


class RegistrationTests(unittest.TestCase):
    _project = lambda x: helpers.get_new_project('New Project')

    def _subproject(self):
        return self._project().add_component(
            title='New Subproject',
            component_type='Project',
        )

    def _test_registration_meta(self, page):
        meta = ('sample narrative', )

        page = page.add_registration(
            registration_type='Open-Ended Registration',
            meta=meta
        )

        self.assertEqual(
            page.registration_meta,
            meta
        )

        page.close()

    def test_project_registration_meta(self):
        self._test_registration_meta(self._project())

    def test_subproject_registration_meta(self):
        self._test_registration_meta(self._subproject())

    def _test_registration_matches(self, page, attribute):
        parent_value = getattr(page, attribute)

        page = page.add_registration(
            registration_type='Open-Ended Registration',
            meta=('sample narrative', )
        )

        self.assertEqual(
            getattr(page, attribute),
            parent_value,
        )

        page.close()

    def test_project_registration_title(self):
        self._test_registration_matches(
            page=self._project(),
            attribute='title'
        )

    def test_subproject_registration_title(self):
        self._test_registration_matches(
            page=self._subproject(),
            attribute='title'
        )

    def test_subproject_registration_parent_title(self):
        self._test_registration_matches(
            page=self._subproject(),
            attribute='parent_title'
        )

    def test_project_registration_components_empty(self):
        self._test_registration_matches(
            page=self._project(),
            attribute='component_names'
        )

    def test_project_registration_components(self):
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

        self._test_registration_matches(
            page=page,
            attribute='component_names'
        )

    def test_subproject_registration_components(self):
        page = self._project()


        page = page.add_component(
            title='Subproject',
            component_type='Project',
        )

        # add component
        page = page.add_component(
            title='Test Component',
            component_type='Other',
        )

        page = page.parent_project()

        self._test_registration_matches(
            page=page,
            attribute='component_names'
        )