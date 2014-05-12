# -*- coding: utf-8 -*-
from brasil.gov.portlets.portlets import collection
from brasil.gov.portlets.testing import INTEGRATION_TESTING
from DateTime import DateTime
from datetime import datetime
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from Products.GenericSetup.utils import _getDottedName
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class CollectionPortletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        news_folder = api.content.create(
            type='Folder',
            title='News Folder',
            container=self.portal
        )
        api.content.create(
            type='News Item',
            title='New 1',
            creation_date=DateTime('2014/05/03 14:23:38.334118 GMT-3'),
            container=news_folder
        )
        api.content.create(
            type='News Item',
            title='New 2',
            creation_date=DateTime('2014/05/01 14:23:38.334118 GMT-3'),
            container=news_folder
        )
        api.content.create(
            type='News Item',
            title='New 3',
            creation_date=DateTime('2014/05/02 14:23:38.334118 GMT-3'),
            container=news_folder
        )
        self.news_collection = api.content.create(
            type='Collection',
            title='News Collection',
            query=[{
                u'i': u'portal_type',
                u'o': u'plone.app.querystring.operation.selection.is',
                u'v': u'News Item'
            }],
            sort_on='created',
            container=news_folder
        )
        events_folder = api.content.create(
            type='Folder',
            title='Events Folder',
            container=self.portal
        )
        api.content.create(
            type='Event',
            title='Event 1',
            creation_date=DateTime('2014/05/03 14:23:38.334118 GMT-3'),
            startDate=datetime(2014, 5, 3, 15, 26, 18),
            container=events_folder
        )
        api.content.create(
            type='Event',
            title='Event 2',
            creation_date=DateTime('2014/05/01 14:23:38.334118 GMT-3'),
            startDate=datetime(2014, 5, 2, 15, 26, 18),
            container=events_folder
        )
        api.content.create(
            type='Event',
            title='Event 3',
            creation_date=DateTime('2014/05/02 14:23:38.334118 GMT-3'),
            startDate=datetime(2014, 5, 1, 15, 26, 18),
            container=events_folder
        )
        self.events_collection = api.content.create(
            type='Collection',
            title='Events Collection',
            query=[{
                u'i': u'portal_type',
                u'o': u'plone.app.querystring.operation.selection.is',
                u'v': u'Event'
            }],
            sort_on='created',
            container=events_folder
        )

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.portal
        request = request or self.request
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def test_portlet_type_registered(self):
        portlet = getUtility(IPortletType, name='brasil.gov.portlets.collection')
        self.assertEqual(portlet.addview, 'brasil.gov.portlets.collection')

    def test_registered_interfaces(self):
        portlet = getUtility(IPortletType, name='brasil.gov.portlets.collection')
        registered_interfaces = [_getDottedName(i) for i in portlet.for_]
        registered_interfaces.sort()
        self.assertEqual(
            ['plone.app.portlets.interfaces.IColumn',
             'plone.app.portlets.interfaces.IDashboard'],
            registered_interfaces
        )

    def test_interfaces(self):
        portlet = collection.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_addview(self):
        portlet = getUtility(IPortletType, name='brasil.gov.portlets.collection')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={})

        self.assertEqual(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], collection.Assignment))

    def test_portlet_properties(self):
        portlet = getUtility(IPortletType, name='brasil.gov.portlets.collection')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={
            'header': u'Portal Padrão Coleção',
            'header_url': u'http://www.plone.org',
            'title_type': u'H1',
            'collection': self.news_collection
        })
        header = mapping.values()[0].header
        self.assertEqual(header, u'Portal Padrão Coleção')

    def test_renderer(self):
        assgmnt1 = collection.Assignment()

        r1 = self.renderer(context=self.portal,
                           assignment=assgmnt1)

        r1 = r1.__of__(self.portal)
        r1.update()
