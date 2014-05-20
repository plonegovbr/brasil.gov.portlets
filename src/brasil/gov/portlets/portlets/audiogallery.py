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


class IAudioGalleryPortlet(IPortletDataProvider):
    '''Portal Padrão: Portlet de galeria de áudio.
    '''

    show_header = schema.Bool(
        title=_(u'Mostrar título'),
        description=_(u'Se habilitado mostra o título.'),
        required=True,
        default=False)

    header = schema.TextLine(
        title=_(u'Texto do título'),
        description=_(u'Texto do título do portlet.'),
        required=True,
        default=_(u'Portal Padrão Galeria de Áudios'))

    header_type = schema.Choice(
        title=_(u'Tipo de título'),
        description=_(u'Tipo de título que será exibido.'),
        values=(u'H1',
                u'H2',
                u'H3',
                u'H4'),
        default=u'H2',
        required=True,
    )

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
        default=5)

    collection = schema.Choice(
        title=_(u'Coleção'),
        description=_(u'Pesquisa a coleção utilizada no portlet.'),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': ('Topic', 'Collection')},
            default_query='path:'))


class Assignment(base.Assignment):

    implements(IAudioGalleryPortlet)

    show_header = False
    header = _(u'Portal Padrão Galeria de Áudios')
    header_type = u'H2'
    show_footer = False
    footer = u''
    footer_url = u''
    limit = 5
    collection = None

    def __init__(self,
                 show_header=False,
                 header=_(u'Portal Padrão Galeria de Áudios'),
                 header_type=u'H2',
                 show_footer=False,
                 footer=u'',
                 footer_url=u'',
                 limit=5,
                 collection=None):
        self.show_header = show_header
        self.header = header
        self.header_type = header_type
        self.show_footer = show_footer
        self.footer = footer
        self.footer_url = footer_url
        self.limit = limit
        self.collection = collection

    @property
    def title(self):
        return self.header


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('templates/audiogallery.pt')
    render = _template

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def css_class(self):
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return 'brasil-gov-portlets-audiogallery-%s' % normalizer.normalize(header)

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

    def title(self):
        '''Generate html part with following structure
        <HX>
            ${Title}
        </HX>
        '''
        hx = getattr(E, self.data.header_type)(self.data.header)
        return html.tostring(hx)

    def get_item_url(self, item):
        """
        Return the audio file url
        Arguments:
        - `item`: audio item
        """
        url = ''

        if (item.portal_type == 'Audio'):
            url = ';'.join([a.absolute_url() for a in item.listFolderContents()])
        else:
            url = item.absolute_url()
        return url


class AddForm(base.AddForm):

    form_fields = form.Fields(IAudioGalleryPortlet)
    form_fields['collection'].custom_widget = UberSelectionWidget

    label = _(u'Adicionar Portlet Portal Padrão Galeria de Áudios')
    description = _(u'Este portlet mostra uma Galeria de Áudios.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(IAudioGalleryPortlet)
    form_fields['collection'].custom_widget = UberSelectionWidget

    label = _(u'Editar Portlet Portal Padrão Galeria de Áudios')
    description = _(u'Este portlet mostra uma Galeria de Áudios.')
