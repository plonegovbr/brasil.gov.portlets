# -*- coding: utf-8 -*-

from Products.CMFPlone import interfaces as plone_interfaces
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from zope.interface import implements

PROJECTNAME = 'brasil.gov.portlets'


class HiddenProducts(object):
    implements(qi_interfaces.INonInstallable)

    def getNonInstallableProducts(self):
        return [
            'brasil.gov.portlets.upgrades.v1000',
            'brasil.gov.portlets.upgrades.v1001'
        ]


class HiddenProfiles(object):
    implements(plone_interfaces.INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            'brasil.gov.portlets:uninstall',
            'brasil.gov.portlets.upgrades.v1000:default',
            'brasil.gov.portlets.upgrades.v1001:default'
        ]
