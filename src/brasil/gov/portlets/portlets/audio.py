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


class IAudioPortlet(IPortletDataProvider):
    '''Portal Padrão: Portlet de áudio.
    '''

    header = schema.TextLine(
        title=_(u'Texto do título'),
        description=_(u'Texto do título do portlet.'),
        required=True,
        default=_(u'Portal Padrão Áudio'))

    audio = schema.Choice(
        title=_(u'Áudio'),
        description=_(u'Pesquisa o audio utilizado no portlet.'),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': ('Audio', 'MPEG Audio File')},
            default_query='path:'))


class Assignment(base.Assignment):

    implements(IAudioPortlet)

    header = u''
    audio = None

    def __init__(self,
                 header=u'',
                 audio=None):
        self.header = header
        self.audio = audio

    @property
    def title(self):
        return self.header


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('templates/audio.pt')
    render = _template

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def css_class(self):
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return 'brasil-gov-portlets-audio-%s' % normalizer.normalize(header)

    @memoize
    def audio(self):
        audio_path = self.data.audio
        if not audio_path:
            return None

        if audio_path.startswith('/'):
            audio_path = audio_path[1:]

        if not audio_path:
            return None

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        if isinstance(audio_path, unicode):
            # restrictedTraverse accepts only strings
            audio_path = str(audio_path)

        result = portal.unrestrictedTraverse(audio_path, default=None)
        if result is not None:
            sm = getSecurityManager()
            if not sm.checkPermission('View', result):
                result = None
        return result

    def title(self):
        audio = self.audio()
        return audio.Title()

    def description(self):
        audio = self.audio()
        return audio.Description()

    def rights(self):
        audio = self.audio()
        return audio.Rights()

    def url(self):
        audio = self.audio()
        mp3 = audio.return_mp3()
        url = ''
        if mp3:
            url = mp3.absolute_url()
        else:
            url = audio.absolute_url()
        return url

    def content_type(self):
        audio = self.audio()
        mp3 = audio.return_mp3()
        content_type = ''
        if mp3:
            content_type = 'audio/mp3'
        return content_type


class AddForm(base.AddForm):

    form_fields = form.Fields(IAudioPortlet)
    form_fields['audio'].custom_widget = UberSelectionWidget

    label = _(u'Adicionar Portlet Portal Padrão Audio')
    description = _(u'Este portlet mostra um Player de Áudio.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(IAudioPortlet)
    form_fields['audio'].custom_widget = UberSelectionWidget

    label = _(u'Editar Portlet Portal Padrão Audio')
    description = _(u'Este portlet mostra um Player de Áudio.')
