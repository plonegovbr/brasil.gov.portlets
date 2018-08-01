# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFQuickInstallerTool import interfaces as BBB
from zope.interface import implementer


@implementer(BBB.INonInstallable)  # BBB: Plone 4.3
@implementer(INonInstallable)
class NonInstallable(object):  # pragma: no cover

    @staticmethod
    def getNonInstallableProducts():
        """Hide in the add-ons configlet."""
        return [
        ]

    @staticmethod
    def getNonInstallableProfiles():
        """Hide at site creation."""
        return [
            u'brasil.gov.portlets:uninstall',
        ]
