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
from plone.uuid.interfaces import IUUID


class IVideoGalleryPortlet(IPortletDataProvider):
    '''Portal Padrão: Portlet de galeria de vídeos.
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
        default=_(u'Portal Padrão Galeria de Vídeos'))

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

    show_subtitle = schema.Bool(
        title=_(u'Mostrar subtítulo'),
        description=_(u'Se habilitado mostra o subtítulo.'),
        required=True,
        default=False)

    subtitle = schema.TextLine(
        title=_(u'Texto do subtítulo'),
        description=_(u'Texto do subtítulo do portlet.'),
        required=False)

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

    limit = schema.Int(
        title=_(u'Quantidade de itens a exibir'),
        description=_(u'Informe o total de itens que devem ser exibidos no '
                      u'portlet.'),
        required=True,
        default=6)

    collection = schema.Choice(
        title=_(u'Coleção'),
        description=_(u'Pesquisa a coleção utilizada no portlet.'),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': ('Topic', 'Collection')},
            default_query='path:'))


class Assignment(base.Assignment):

    implements(IVideoGalleryPortlet)

    show_header = False
    header = _(u'Portal Padrão Galeria de Vídeos')
    header_type = u'H2'
    show_title = False
    show_subtitle = False
    subtitle = u''
    show_description = False
    show_footer = False
    footer = u''
    footer_url = u''
    limit = 6
    collection = None

    def __init__(self,
                 show_header=False,
                 header=_(u'Portal Padrão Galeria de Vídeos'),
                 header_type=u'H2',
                 show_title=False,
                 show_subtitle=False,
                 subtitle=u'',
                 show_description=False,
                 show_footer=False,
                 footer=u'',
                 footer_url=u'',
                 limit=6,
                 collection=None):
        self.show_header = show_header
        self.header = header
        self.header_type = header_type
        self.show_title = show_title
        self.show_subtitle = show_subtitle
        self.subtitle = subtitle
        self.show_description = show_description
        self.show_footer = show_footer
        self.footer = footer
        self.footer_url = footer_url
        self.limit = limit
        self.collection = collection

    @property
    def title(self):
        return self.header


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('templates/videogallery.pt')
    render = _template

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def _has_image_field(self, obj):
        """Return True if the object has an image field.

        :param obj: [required]
        :type obj: content object
        """
        if hasattr(obj, 'image'):  # Dexterity
            return True
        elif hasattr(obj, 'Schema'):  # Archetypes
            return 'image' in obj.Schema().keys()
        else:
            return False

    def css_class(self):
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return 'brasil-gov-portlets-videogallery-%s' % normalizer.normalize(header)

    def get_uid(self, obj):
        return IUUID(obj)

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
            return scales.scale('image', width=80, height=60)


class AddForm(base.AddForm):

    form_fields = form.Fields(IVideoGalleryPortlet)
    form_fields['collection'].custom_widget = UberSelectionWidget

    label = _(u'Adicionar Portlet Portal Padrão Galeria de Vídeo')
    description = _(u'Este portlet mostra uma Galeria de Vídeos.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(IVideoGalleryPortlet)
    form_fields['collection'].custom_widget = UberSelectionWidget

    label = _(u'Editar Portlet Portal Padrão Galeria de Vídeo')
    description = _(u'Este portlet mostra uma Galeria de Vídeos.')
