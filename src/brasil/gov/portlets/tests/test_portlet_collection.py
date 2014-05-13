# -*- coding: utf-8 -*-
from brasil.gov.portlets.portlets import collection
from brasil.gov.portlets.testing import INTEGRATION_TESTING
from DateTime import DateTime
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

        test_date_order = [3, 1, 2]

        news_folder = api.content.create(
            type='Folder',
            title='News Folder',
            container=self.portal
        )
        for i in xrange(1, 4):
            n = api.content.create(
                type='News Item',
                title='New {0}'.format(i),
                creation_date=DateTime(
                    '2014/05/0{0} 14:23:38.334118 GMT-3'
                    .format(test_date_order[i - 1])),
                container=news_folder
            )
            n.setModificationDate(DateTime(
                '2014/05/0{0} 14:23:38.334118 GMT-3'.format(test_date_order[i - 1])
            ))
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
        self.news_collection_path = '/' + '/'.join(self.news_collection.getPhysicalPath()[2:])
        self.news_collection_url = self.news_collection.absolute_url()

        test_startdate_order = [3, 2, 1]
        events_folder = api.content.create(
            type='Folder',
            title='Events Folder',
            container=self.portal
        )
        for i in xrange(1, 4):
            e = api.content.create(
                type='Event',
                title='Event {0}'.format(i),
                creation_date=DateTime(
                    '2014/05/0{0} 14:23:38.334118 GMT-3'
                    .format(test_date_order[i - 1])),
                startDate=DateTime(
                    '2014/05/0{0} 14:23:38.334118 GMT-3'
                    .format(test_startdate_order[i - 1])),
                container=events_folder
            )
            e.setModificationDate(DateTime(
                '2014/05/0{0} 14:23:38.334118 GMT-3'.format(test_date_order[i - 1])
            ))
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
        self.events_collection_path = '/' + '/'.join(self.events_collection.getPhysicalPath()[2:])
        self.events_collection_url = self.events_collection.absolute_url()

    def _renderer(self, context=None, request=None, view=None, manager=None,
                  assignment=None):
        context = context or self.portal
        request = request or self.request
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def _assigned_renderers(self):
        assgmnt1 = collection.Assignment(
            header=u'Portal Padrão Coleção',
            header_url=u'http://www.plone.org',
            show_image=True,
            image_size=u'large 768:768',
            title_type=u'H4',
            show_footer=True,
            footer=u'Mais...',
            footer_url=self.news_collection_url,
            limit=3,
            show_date=True,
            date_format=u'curta: Data',
            collection=self.news_collection_path
        )

        r1 = self._renderer(context=self.portal,
                            assignment=assgmnt1)

        r1 = r1.__of__(self.portal)
        r1.update()

        assgmnt2 = collection.Assignment(
            header=u'Portal Padrão Coleção',
            header_url=u'http://www.plone.org',
            show_image=True,
            image_size=u'large 768:768',
            title_type=u'H4',
            show_footer=True,
            footer=u'Mais...',
            footer_url=self.events_collection_url,
            limit=3,
            show_date=True,
            date_format=u'longa: Data/Hora',
            collection=self.events_collection_path
        )

        r2 = self._renderer(context=self.portal,
                            assignment=assgmnt2)

        r2 = r2.__of__(self.portal)
        r2.update()

        return (r1, r2)

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
            'show_image': True,
            'image_size': u'large 768:768',
            'title_type': u'H4',
            'show_footer': True,
            'footer': u'Mais...',
            'footer_url': self.news_collection_url,
            'limit': 2,
            'show_date': True,
            'date_format': u'longa: Data/Hora',
            'collection': self.news_collection_path
        })

        title = mapping.values()[0].title
        self.assertEqual(title, u'Portal Padrão Coleção')

        header = mapping.values()[0].header
        self.assertEqual(header, u'Portal Padrão Coleção')

        header_url = mapping.values()[0].header_url
        self.assertEqual(header_url, u'http://www.plone.org')

        show_image = mapping.values()[0].show_image
        self.assertEqual(show_image, True)

        image_size = mapping.values()[0].image_size
        self.assertEqual(image_size, u'large 768:768')

        title_type = mapping.values()[0].title_type
        self.assertEqual(title_type, u'H4')

        show_footer = mapping.values()[0].show_footer
        self.assertEqual(show_footer, True)

        footer = mapping.values()[0].footer
        self.assertEqual(footer, u'Mais...')

        footer_url = mapping.values()[0].footer_url
        self.assertEqual(footer_url, self.news_collection_url)

        limit = mapping.values()[0].limit
        self.assertEqual(limit, 2)

        show_date = mapping.values()[0].show_date
        self.assertEqual(show_date, True)

        date_format = mapping.values()[0].date_format
        self.assertEqual(date_format, u'longa: Data/Hora')

        collection = mapping.values()[0].collection
        self.assertEqual(collection, self.news_collection_path)

    def test_renderer(self):
        r1, r2 = self._assigned_renderers()

        self.assertIsInstance(r1, collection.Renderer)

        self.assertIsInstance(r2, collection.Renderer)

    def test_renderer_cssclass(self):
        r1, r2 = self._assigned_renderers()

        self.assertEqual(r1.css_class(),
                         'brasil-gov-portlets-collection-portal-padrao-colecao')

    def test_renderer_typecriteria(self):
        r1, r2 = self._assigned_renderers()

        type_criteria = r1._collection_type_criteria(self.news_collection)
        self.assertEqual(type_criteria, u'News Item')

        type_criteria = r2._collection_type_criteria(self.events_collection)
        self.assertEqual(type_criteria, u'Event')

    def test_renderer_results(self):
        r1, r2 = self._assigned_renderers()

        results = [b.id for b in r1.results()]
        self.assertEqual(results, ['new-2', 'new-3', 'new-1'])

        results = [b.id for b in r2.results()]
        self.assertEqual(results, ['event-3', 'event-2', 'event-1'])

    def test_renderer_collection(self):
        r1, r2 = self._assigned_renderers()

        self.assertEqual(r1.collection(), self.news_collection)

        self.assertEqual(r2.collection(), self.events_collection)

    def test_renderer_thumbnail(self):
        r1, r2 = self._assigned_renderers()
        pass

    def test_renderer_title(self):
        r1, r2 = self._assigned_renderers()

        titles = [r1.title(b.getObject()) for b in r1.results()]
        self.assertEqual(titles, [
            '<h4><a href="http://nohost/plone/news-folder/new-2" title="">New 2</a></h4>',
            '<h4><a href="http://nohost/plone/news-folder/new-3" title="">New 3</a></h4>',
            '<h4><a href="http://nohost/plone/news-folder/new-1" title="">New 1</a></h4>'
        ])

        titles = [r2.title(b.getObject()) for b in r2.results()]
        self.assertEqual(titles, [
            '<h4><a href="http://nohost/plone/events-folder/event-3" title="">Event 3</a></h4>',
            '<h4><a href="http://nohost/plone/events-folder/event-2" title="">Event 2</a></h4>',
            '<h4><a href="http://nohost/plone/events-folder/event-1" title="">Event 1</a></h4>'
        ])

    def test_renderer_date(self):
        r1, r2 = self._assigned_renderers()

        dates = [r1.date(b.getObject()) for b in r1.results()]
        self.assertEqual(dates, ['01/05/2014', '02/05/2014', '03/05/2014'])

        dates = [r2.date(b.getObject()) for b in r2.results()]
        self.assertEqual(dates, ['01/05/2014 14:23', '02/05/2014 14:23', '03/05/2014 14:23'])
