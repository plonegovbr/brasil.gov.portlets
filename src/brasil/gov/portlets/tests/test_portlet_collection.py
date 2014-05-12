# -*- coding: utf-8 -*-
from brasil.gov.portlets.portlets import collection
from brasil.gov.portlets.testing import INTEGRATION_TESTING
# from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
# from plone.portlets.interfaces import IPortletManager
# from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from Products.GenericSetup.utils import _getDottedName
# from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class CollectionPortletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

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
        addview.createAndAdd(data={})
        # title = mapping.values()[0].title

    def test_renderer(self):
        # context = self.agenda
        # request = self.agenda.REQUEST
        # view = context.restrictedTraverse('@@plone')
        # manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.agenda)
        # assignment = collection.Assignment()
        #
        # renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        # self.assertTrue(isinstance(renderer, collection.Renderer))
        # html = renderer.render()
        # # Titulo do portlet
        # self.assertIn('Busca de Agenda', html)
        # # Id do texto explicativo
        # self.assertIn('collection_agenda_texto', html)
        pass
