# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements

PROJECTNAME = 'brasil.gov.portlets'


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'brasil.gov.portlets:uninstall',
            u'brasil.gov.portlets.upgrades.v1010:default'
        ]
