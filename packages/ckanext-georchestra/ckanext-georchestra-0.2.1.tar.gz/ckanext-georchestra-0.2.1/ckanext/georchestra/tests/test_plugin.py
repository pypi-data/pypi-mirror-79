# encoding: utf-8

from nose import tools as nosetools

import ckan.model as model
import ckan.tests.helpers as helpers
import ckan.plugins as plugins
from ckan.plugins.toolkit import NotAuthorized, ObjectNotFound
import ckan.tests.factories as factories


class TestGeorchestraPlugin(object):
    '''Tests for the ckanext.georchestra.plugin module.

    '''
    @classmethod
    def setup_class(cls):
        '''Nose runs this method once to setup our test class.'''
        # Test code should use CKAN's plugins.load() function to load plugins
        # to be tested.
        plugins.load('georchestra')

    def teardown(self):
        '''Nose runs this method after each test method in our test class.'''
        # Rebuild CKAN's database after each test method, so that each test
        # method runs with a clean slate.
        model.repo.rebuild_db()

    @classmethod
    def teardown_class(cls):
        '''Nose runs this method once after all the test methods in our class
                have been run.

                '''
        # We have to unload the plugin we loaded, so it doesn't affect any
        # tests that run after ours.
        plugins.unload('georchestra')

    def test_dummytest(self):
        nosetools.assert_true('a'+'a' == 'aa')

    def test_dummyfailedtest(self):
        nosetools.assert_equal('a'+'a','aa')
