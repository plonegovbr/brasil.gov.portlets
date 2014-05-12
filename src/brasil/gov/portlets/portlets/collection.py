# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from DateTime import DateTime
from lxml import html
from lxml.html import builder as E
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from secom.brasil.portal import _
from zope import schema
from zope.component import getMultiAdapter, getUtility
from zope.formlib import form
from zope.interface import implements
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def default_image_scale(context):
    image_scale = None
    properties_tool = getToolByName(context, 'portal_properties')
    imagescales_properties = getattr(properties_tool, 'imaging_properties', None)
    raw_scales = getattr(imagescales_properties, 'allowed_sizes', None)
    if (raw_scales):
        image_scale = raw_scales[0]
    return image_scale


class ICollectionPortlet(IPortletDataProvider):
    '''Portal Padrão: Portlet de coleção.
    '''

    header = schema.TextLine(
        title=_(u'Título'),
        description=_(u'Título do portlet.'),
        required=True)

    header_url = schema.TextLine(
        title=_(u'Link do título'),
        description=_(u'Link do título do portlet.'),
        required=False)

    show_image = schema.Bool(
        title=_(u'Imagem'),
        description=_(u'Se habilitado pede as informações da imagem.'),
        required=True,
        default=False)

    image_size = schema.Choice(
        title=_(u'Tamanho da imagem'),
        description=_(u'Tamanho da imagem que será exibida.'),
        vocabulary='brasil.image.scales',
        required=True,
        defaultFactory=default_image_scale
    )

    title_type = schema.Choice(
        title=_(u'Tipo de título'),
        description=_(u'Tipo de título que será exibido.'),
        values=(u'H1',
                u'H2',
                u'H3',
                u'H4'),
        default=u'H1',
        required=True,
    )

    show_footer = schema.Bool(
        title=_(u'Rodapé'),
        description=_(u'Se habilitado pede as informações do rodapé.'),
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

    show_date = schema.Bool(
        title=_(u'Exibir Datas'),
        description=_(u'Se habilitado, será mostrado a data dos itens da '
                      u'coleção.'),
        required=True,
        default=False)

    date_format = schema.Choice(
        title=_(u'Formato de Data'),
        description=_(u'Formato que a data será exibida.'),
        values=(_(u'curta: Data'),
                _(u'longa: Data/Hora')),
        default=_(u'curta: Data'),
        required=True,
    )

    collection = schema.Choice(
        title=_(u'Coleção'),
        description=_(u'Pesquisa a coleção utilizada no portlet.'),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': ('Topic', 'Collection')},
            default_query='path:'))


class Assignment(base.Assignment):

    implements(ICollectionPortlet)

    header = u''
    header_url = u''
    show_image = False
    image_size = None
    title_type = u'H1'
    show_footer = False
    footer = u''
    footer_url = u''
    limit = 5
    show_date = False
    date_format = _(u'curta: Data')
    collection = None

    def __init__(self,
                 header=u'',
                 header_url=u'',
                 show_image=False,
                 image_size=None,
                 title_type=u'H1',
                 show_footer=False,
                 footer=u'',
                 footer_url=u'',
                 limit=5,
                 show_date=False,
                 date_format=_(u'curta: Data'),
                 collection=None):
        self.header = header
        self.header_url = header_url
        self.show_image = show_image
        self.image_size = image_size
        self.title_type = title_type
        self.show_footer = show_footer
        self.footer = footer
        self.footer_url = footer_url
        self.limit = limit
        self.show_date = show_date
        self.date_format = date_format
        self.collection = collection

    @property
    def title(self):
        return self.header


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('templates/collection.pt')
    render = _template

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def css_class(self):
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return 'brasil-gov-portlets-collection-%s' % normalizer.normalize(header)

    def _collection_type_criteria(self, collection):
        type_criteria = u''
        for c in collection.getQuery():
            if ((c[u'i'] == u'portal_type') and
               (c[u'o'] == u'plone.app.querystring.operation.selection.is')):
                type_criteria = c[u'v']
                break
        return type_criteria

    @memoize
    def results(self):
        results = []
        collection = self.collection()
        query = {}
        if collection is not None:
            if (self._collection_type_criteria(collection) in [u'Compromisso',
                                                               u'Event']):
                query['sort_on'] = u'start'
            limit = self.data.limit
            if limit and limit > 0:
                # pass on batching hints to the catalog
                query['batch'] = True,
                query['b_size'] = limit
                results = collection.queryCatalog(query)
                results = results._sequence
            else:
                results = collection.queryCatalog(query)
            if limit and limit > 0:
                results = results[:limit]
        return results

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

    def thumbnail(self, item):
        """Return a thumbnail of an image if the item has an image field and
        the field is visible in the portlet.

        :param item: [required]
        :type item: content object
        """
        if self.data.show_image:
            scaleconf = self.data.image_size
            # scale string is something like: 'mini 200:200'
            scale = scaleconf.split(' ')[0]  # we need the name only: 'mini'
            scales = item.restrictedTraverse('@@images')
            return scales.scale('image', scale)

    def title(self, item):
        '''Generate html part with following structure
        <HX>
            <a href="${item/absolute_url}"
               title="${item/Description}">
                ${item/Title}
            </a>
        </HX>
        '''
        hx = getattr(E, self.data.title_type)()
        hx.append(
            E.A(item.Title().decode('utf-8'),
                href=item.absolute_url(),
                title=item.Description().decode('utf-8'))
        )
        return html.tostring(hx)

    def date(self, item):
        dt = DateTime(item.Date())
        if (item.portal_type in [u'Compromisso',
                                 u'Event']):
            dt = DateTime(item.start_date)
        if (self.data.date_format == _(u'curta: Data')):
            return dt.strftime('%d/%m/%Y')
        else:
            return dt.strftime('%d/%m/%Y %H:%M')


class AddForm(base.AddForm):

    form_fields = form.Fields(ICollectionPortlet)
    form_fields['collection'].custom_widget = UberSelectionWidget

    label = _(u'Adicionar Portlet Portal Padrão Coleção')
    description = _(u'Este portlet mostra uma listagem de itens de uma '
                    u'Coleção.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(ICollectionPortlet)
    form_fields['collection'].custom_widget = UberSelectionWidget

    label = _(u'Editar Portlet Portal Padrão Coleção')
    description = _(u'Este portlet mostra uma listagem de itens de uma '
                    u'Coleção.')
