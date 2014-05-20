# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from brasil.gov.portlets import _
from lxml import html
from lxml.html import builder as E
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.formlib import form
from zope.interface import implements


class IMediaCarouselPortlet(IPortletDataProvider):
    '''Portal Padrão: Portlet de carrossel de imagens.
    '''

    show_header = schema.Bool(
        title=_(u'Mostrar cabeçalho'),
        description=_(u'Se habilitado mostra o cabeçalho.'),
        required=True,
        default=False)

    header = schema.TextLine(
        title=_(u'Texto do cabeçalho'),
        description=_(u'Texto do cabeçalho do portlet.'),
        required=True,
        default=_(u'Portal Padrão Carrossel de Imagens'))

    header_type = schema.Choice(
        title=_(u'Tipo de cabeçalho'),
        description=_(u'Tipo de cabeçalho que será exibido.'),
        values=(u'H1',
                u'H2',
                u'H3',
                u'H4'),
        default=u'H2',
        required=True)

    show_title = schema.Bool(
        title=_(u'Mostrar título'),
        description=_(u'Se habilitado mostra o título.'),
        required=True,
        default=False)

    show_description = schema.Bool(
        title=_(u'Mostrar descrição'),
        description=_(u'Se habilitado mostra a descrição.'),
        required=True,
        default=False)

    show_footer = schema.Bool(
        title=_(u'Mostrar rodapé'),
        description=_(u'Se habilitado mostra o rodapé.'),
        required=True,
        default=False)

    footer = schema.TextLine(
        title=_(u'Texto do rodapé'),
        description=_(u'Texto do rodapé do portlet.'),
        required=False)

    footer_url = schema.TextLine(
        title=_(u'Link do rodapé'),
        description=_(u'Link do rodapé do portlet.'),
        required=False)

    show_rights = schema.Bool(
        title=_(u'Mostrar crédito'),
        description=_(u'Se habilitado mostra o crédito.'),
        required=True,
        default=False)

    limit = schema.Int(
        title=_(u'Quantidade de itens a exibir'),
        description=_(u'Informe o total de itens que devem ser exibidos no '
                      u'portlet.'),
        required=True,
        default=5)

    collection = schema.Choice(
        title=_(u'Coleção'),
        description=_(u'Pesquisa a coleção utilizada no portlet.'),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': ('Topic', 'Collection')},
            default_query='path:'))


class Assignment(base.Assignment):

    implements(IMediaCarouselPortlet)

    show_header = False
    header = _(u'Portal Padrão Carrossel de Imagens')
    header_type = u'H2'
    show_title = False
    show_description = False
    show_footer = False
    footer = u''
    footer_url = u''
    show_rights = False
    limit = 5
    collection = None

    def __init__(self,
                 show_header=False,
                 header=_(u'Portal Padrão Carrossel de Imagens'),
                 header_type=u'H2',
                 show_title=False,
                 show_description=False,
                 show_footer=False,
                 footer=u'',
                 footer_url=u'',
                 show_rights=False,
                 limit=5,
                 collection=None):
        self.show_header = show_header
        self.header = header
        self.header_type = header_type
        self.show_title = show_title
        self.show_description = show_description
        self.show_footer = show_footer
        self.footer = footer
        self.footer_url = footer_url
        self.show_rights = show_rights
        self.limit = limit
        self.collection = collection

    @property
    def title(self):
        return self.header


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('templates/mediacarousel.pt')
    render = _template

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def css_class(self):
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return 'brasil-gov-portlets-mediacarousel-%s' % normalizer.normalize(header)

    @memoize
    def results(self):
        results = []
        collection = self.collection()
        query = {}
        if collection is not None:
            limit = self.data.limit
            if limit and limit > 0:
                # pass on batching hints to the catalog
                query['batch'] = True
                query['b_size'] = limit
                results = collection.queryCatalog(**query)
                results = results._sequence
            else:
                results = collection.queryCatalog(**query)
            if limit and limit > 0:
                results = results[:limit]
        return [b.getObject() for b in results]

    @memoize
    def collection(self):
        collection_path = self.data.collection
        if not collection_path:
            return None

        if collection_path.startswith('/'):
            collection_path = collection_path[1:]

        if not collection_path:
            return None

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        if isinstance(collection_path, unicode):
            # restrictedTraverse accepts only strings
            collection_path = str(collection_path)

        result = portal.unrestrictedTraverse(collection_path, default=None)
        if result is not None:
            sm = getSecurityManager()
            if not sm.checkPermission('View', result):
                result = None
        return result

    def header(self):
        '''Generate html part with following structure
        <HX>
            ${Header}
        </HX>
        '''
        hx = getattr(E, self.data.header_type)(self.data.header)
        return html.tostring(hx)

    def thumbnail(self, item):
        if self._has_image_field(item):
            scales = item.restrictedTraverse('@@images')
            thumb = scales.scale('image', width=80, height=60)
            return {
                'src': thumb.url,
                'alt': item.Description(),
            }

    def scale(self, item):
        if self._has_image_field(item):
            scales = item.restrictedTraverse('@@images')
            thumb = scales.scale('image', width=692, height=433)
            return {
                'src': thumb.url,
                'alt': item.Description(),
            }


class AddForm(base.AddForm):

    form_fields = form.Fields(IMediaCarouselPortlet)
    form_fields['collection'].custom_widget = UberSelectionWidget

    label = _(u'Adicionar Portlet Portal Padrão Carrossel de Imagens')
    description = _(u'Este portlet mostra uma Carrossel de Imagens.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(IMediaCarouselPortlet)
    form_fields['collection'].custom_widget = UberSelectionWidget

    label = _(u'Editar Portlet Portal Padrão Carrossel de Imagens')
    description = _(u'Este portlet mostra uma Carrossel de Imagens.')