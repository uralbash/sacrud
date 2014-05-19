#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Test for sacrud.common
"""

import os
import unittest

from pyramid import testing

from sacrud.common.pyramid_helpers import get_obj_from_settings
from sacrud.pyramid_ext import get_field_template
from sacrud.pyramid_ext.breadcrumbs import breadcrumbs, get_crumb
from sacrud.pyramid_ext.views import get_relationship, get_table
from sacrud.tests.test_models import (_initTestingDB, DB_FILE,
                                      Profile, TEST_DATABASE_CONNECTION_STRING,
                                      User, user_add)


class BaseTest(unittest.TestCase):

    def setUp(self):
        from sacrud.tests.mock_main import main
        settings = {'sqlalchemy.url': TEST_DATABASE_CONNECTION_STRING}
        app = main({}, **settings)
        DBSession = _initTestingDB()
        user_add(DBSession)
        user_add(DBSession)
        # user = user_add(DBSession)
        # profile_add(DBSession, user)

        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        del self.testapp
        from sacrud.tests.test_models import DBSession
        DBSession.remove()
        os.remove(DB_FILE)


class BreadCrumbsTest(BaseTest):

    def test_get_crumb(self):
        crumb = get_crumb('Dashboard', True, 'sa_home', {'table': 'foo'})
        self.assertEqual(crumb, {'visible': True, 'name': 'Dashboard',
                                 'param': {'table': 'foo'},
                                 'view': 'sa_home'})

    def test_breadcrumbs(self):
        bc = breadcrumbs('foo', 'sa_list')
        self.assertEqual(bc,
                         [{'visible': True, 'name': 'Dashboard',
                           'param': {'table': 'foo'},
                           'view': 'sa_home'},
                          {'visible': True, 'name': 'foo',
                           'param': {'table': 'foo'}, 'view': 'sa_list'}])
        bc = breadcrumbs('foo', 'sa_create')
        self.assertEqual(bc, [{'visible': True, 'name': 'Dashboard',
                               'param': {'table': 'foo'}, 'view': 'sa_home'},
                              {'visible': True, 'name': 'foo',
                               'param': {'table': 'foo'}, 'view': 'sa_list'},
                              {'visible': False, 'name': 'create',
                               'param': {'table': 'foo'}, 'view': 'sa_list'}])
        bc = breadcrumbs('foo', 'sa_read')
        self.assertEqual(bc, [{'visible': True, 'name': 'Dashboard',
                               'param': {'table': 'foo'}, 'view': 'sa_home'},
                              {'visible': True, 'name': 'foo',
                               'param': {'table': 'foo'}, 'view': 'sa_list'},
                              {'visible': False, 'name': None,
                               'param': {'table': 'foo'}, 'view': 'sa_list'}])
        bc = breadcrumbs('foo', 'sa_union')
        self.assertEqual(bc, [{'visible': True, 'name': 'Dashboard',
                               'param': {'table': 'foo'}, 'view': 'sa_home'},
                              {'visible': True, 'name': 'foo',
                               'param': {'table': 'foo'}, 'view': 'sa_list'},
                              {'visible': False, 'name': 'union',
                               'param': {'table': 'foo'}, 'view': 'sa_list'}])


class CommonTest(BaseTest):

    def test_get_field_template(self):
        self.assertEqual('sacrud/types/String.jinja2',
                         get_field_template('foo'))
        enum = get_field_template('Enum')
        self.assertIn('sacrud/types/Enum.jinja2', enum)
        self.assertTrue(os.path.exists(enum))

    def test_get_obj_from_settings(self):
        request = testing.DummyRequest()
        config = testing.setUp(request=request)
        config.registry.settings['foo.User'] = 'sacrud.tests.test_models:User'
        obj = get_obj_from_settings(request, 'foo.User')
        self.assertEqual(obj, User)

        config.registry.settings['foo.User'] = User
        obj = get_obj_from_settings(request, 'foo.User')
        self.assertEqual(obj, User)


class ViewsTest(BaseTest):

    def _include_sacrud(self):
        request = testing.DummyRequest()
        config = testing.setUp(request=request)
        config.registry.settings['sqlalchemy.url'] = TEST_DATABASE_CONNECTION_STRING
        config.include('sacrud.pyramid_ext', route_prefix='/admin')
        settings = config.registry.settings
        settings['sacrud.models'] = {'': {'tables': [User]},
                                     'Auth models': {'tables': [User, Profile]}
                                     }
        return request

    def test_get_table(self):
        request = self._include_sacrud()
        user = get_table('UsEr', request)
        self.assertEqual(user, User)
        foo = get_table('foo', request)
        self.assertEqual(foo, None)

    def test_get_relationship(self):
        request = self._include_sacrud()
        foo = get_relationship('foo', request)
        self.assertEqual(foo, None)
        bar = get_relationship('user', request)
        self.assertEqual(len(bar), 1)
        self.assertEqual(bar, [{'col': User.id, 'cls': Profile}])

    def test_sa_home(self):
        res = self.testapp.get('/admin/', status=200)
        self.failUnless('Auth models' in res.body)
        self.failUnless('user' in res.body)
        self.failUnless('profile' in res.body)

    def test_sa_list(self):
        res = self.testapp.get('/admin/user', status=200)
        self.failUnless('user_1' in res.body)
        res = self.testapp.get('/admin/profile', status=200)
        self.failUnless('profile_1' not in res.body)

    def test_sa_read(self):
        res = self.testapp.get('/admin/user/read/1', status=200)
        self.failUnless('view user' in res.body)

    def test_sa_update(self):
        res = self.testapp.get('/admin/user/update/1', status=200)
        self.failUnless('Add a new user' in res.body)

    def test_sa_create(self):
        res = self.testapp.get('/admin/user/create', status=200)
        self.failUnless('create' in res.body)
        # XXX: not good
        self.failUnless('Add a new user' in res.body)

    def test_sa_delete(self):
        res = self.testapp.get('/admin/user/read/1', status=200)
        self.failUnless('view user' in res.body)
        self.testapp.get('/admin/user/delete/1', status=302)


# def _callFUT(self, request):
#         from sacrud_pages.views import page_visible
#         return page_visible(request)

#     def test_it(self):
#         request = testing.DummyRequest()
#         request.set_property(lambda x: MPTTPages, 'sacrud_pages_model', reify=True)
#         request.set_property(mock_dbsession, 'dbsession', reify=True)
#         request.matchdict['node'] = 12
#         response = self._callFUT(request)
#         request.dbsession.commit()
#         self.assertEqual(response, {'visible': False})
#         response = self._callFUT(request)
#         request.dbsession.commit()
#         self.assertEqual(response, {'visible': True})
#         response = self._callFUT(request)
#         request.dbsession.commit()
#         self.assertEqual(response, {'visible': False})



    # def test_sa_save_position(self):
    #     request = testing.DummyRequest()
    #     equest.set_property(mock_dbsession, 'dbsession', reify=True)
        # res = self.testapp.post_json(
        #     '/admin/save_position',
        #     {'column': 1, 'position': 3, 'widget': 'not_exists'})
        # self.assertEqual(res.json, None)

        # res = self.testapp.post_json(
        #     '/admin/save_position',
        #     {'column': 1, 'position': 3, 'widget': 'Pages'})
        # self.assertDictEqual(res.json, {"result": "ok"})
