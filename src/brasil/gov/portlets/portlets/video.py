# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from brasil.gov.portlets import _
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


class IVideoPortlet(IPortletDataProvider):
    '''Portal Padrão: Portlet de vídeo.
    '''

    show_header = schema.Bool(
        title=_(u'Mostrra título'),
        description=_(u'Se habilitado mostra o título.'),
        required=True,
        default=False)

    header = schema.TextLine(
        title=_(u'Texto do título'),
        description=_(u'Texto do título do portlet.'),
        required=True,
        default=_(u'Portal Padrão Vídeo'))

    video = schema.Choice(
        title=_(u'Vídeo'),
        description=_(u'Pesquisa o vídeo utilizado no portlet.'),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': ('sc.embedder')},
            default_query='path:'))


class Assignment(base.Assignment):

    implements(IVideoPortlet)

    show_header = False
    header = _(u'Portal Padrão Vídeo')
    video = None

    def __init__(self,
                 show_header=False,
                 header=_(u'Portal Padrão Vídeo'),
                 video=None):
        self.show_header = show_header
        self.header = header
        self.video = video

    @property
    def title(self):
        return self.header


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('templates/video.pt')
    render = _template

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def css_class(self):
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return 'brasil-gov-portlets-video-%s' % normalizer.normalize(header)

    @memoize
    def video(self):
        video_path = self.data.video
        if not video_path:
            return None

        if video_path.startswith('/'):
            video_path = video_path[1:]

        if not video_path:
            return None

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        if isinstance(video_path, unicode):
            # restrictedTraverse accepts only strings
            video_path = str(video_path)

        result = portal.unrestrictedTraverse(video_path, default=None)
        if result is not None:
            sm = getSecurityManager()
            if not sm.checkPermission('View', result):
                result = None
        return result


class AddForm(base.AddForm):

    form_fields = form.Fields(IVideoPortlet)
    form_fields['video'].custom_widget = UberSelectionWidget

    label = _(u'Adicionar Portlet Portal Padrão Vídeo')
    description = _(u'Este portlet mostra um Player de Vídeo.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(IVideoPortlet)
    form_fields['video'].custom_widget = UberSelectionWidget

    label = _(u'Editar Portlet Portal Padrão Vídeo')
    description = _(u'Este portlet mostra um Player de Vídeo.')
