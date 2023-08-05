# encoding: utf-8

'''Tests for the ckanext.example_iauthfunctions extension.

'''

from nose.tools import assert_raises
from nose.tools import assert_equal

import ckan.model as model
import ckan.plugins
from ckan.plugins.toolkit import NotAuthorized, ObjectNotFound
import ckan.tests.factories as factories
import ckan.logic as logic

import ckan.tests.helpers as helpers


class TestGeorchestraAuthFunctions(object):
    '''Tests for the ckanext.georchestra.plugin module.

    Specifically tests that overriding parent auth functions will cause
    child auth functions to use the overridden version.
    '''
    @classmethod
    def setup_class(cls):
        '''Nose runs this method once to setup our test class.'''
        # Test code should use CKAN's plugins.load() function to load plugins
        # to be tested.
        ckan.plugins.load('georchestra')

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
        ckan.plugins.unload('georchestra')

    def test_existing_user_connects(self):
        '''Normally organization admins can delete resources
        Our plugin prevents this by blocking delete organization.

        Ensure the delete button is not displayed (as only resource delete
        is checked for showing this)

        '''
        sec_headers = {
            'Sec-Orgname': 'R�gion Hauts-de-France',
            'Sec-Roles': 'ROLE_GT_INGENIERIE_FONCIERE_REDACTEUR;ROLE_GT_INGENIERIE_FONCIERE_ANIMATEUR;ROLE_GT_EFF_ENER_BAT;ROLE_GT_OCCSOL;ROLE_GT_RESEAU_DE_DONNEES_SUR_L_ENVIRONNEMENT;ROLE_GT_CHEMINS;ROLE_GN_ADMIN;ROLE_GT_CHEMINS_REDACTEUR;ROLE_GT_CENTRES_VILLES;ROLE_USER;ROLE_GT_DOCUMENTS_D_URBANISME_ET_GPU;ROLE_GT_TU_CAPTES;ROLE_EXTRACTORAPP;ROLE_GN_EDITOR;ROLE_GT_INGENIERIE_FONCIERE;ROLE_GT_CENTRES_VILLES_REDACTEUR;ROLE_GN_REVIEWER',
            'Sec-Firstname': 'C�dric',
            'Sec-Email': 'jean@pomfont.fr',
            'Sec-Tel': '03 74 27 15 13',
            'Sec-Proxy': 'true',
            'Sec-Username': 'cansard',
            'Sec-Lastname': 'Ansard',
            'Sec-Org': 'region_hdf',
        }
        user = factories.User(
            name=u'cansard',
            fullname=u'Cédric Ansard'
        )
        assert_equal(user['fullname'],u'Cdric Ansard')
