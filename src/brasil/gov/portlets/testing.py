# -*- coding: utf-8 -*-

from App.Common import package_home
from PIL import Image
from plone import api
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from StringIO import StringIO

import os
import random


def loadFile(name, size=0):
    """Load file from testing directory
    """
    path = os.path.join(package_home(globals()), 'tests/input', name)
    fd = open(path, 'rb')
    data = fd.read()
    fd.close()
    return data


def generate_jpeg(width, height):
    # Mandelbrot fractal
    # FB - 201003254
    # drawing area
    xa = -2.0
    xb = 1.0
    ya = -1.5
    yb = 1.5
    maxIt = 25  # max iterations allowed
    # image size
    image = Image.new('RGB', (width, height))
    c = complex(random.random() * 2.0 - 1.0, random.random() - 0.5)

    for y in range(height):
        zy = y * (yb - ya) / (height - 1) + ya
        for x in range(width):
            zx = x * (xb - xa) / (width - 1) + xa
            z = complex(zx, zy)
            for i in range(maxIt):
                if abs(z) > 2.0:
                    break
                z = z * z + c
            r = i % 4 * 64
            g = i % 8 * 32
            b = i % 16 * 16
            image.putpixel((x, y), b * 65536 + g * 256 + r)

    output = StringIO()
    image.save(output, format='PNG')
    return output.getvalue()


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import brasil.gov.portlets
        self.loadZCML(package=brasil.gov.portlets)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'brasil.gov.portlets:default')
        with api.env.adopt_roles(['Manager']):
            obj = api.content.create(
                type='Image',
                title='My Image',
                container=portal)
            obj.setImage(generate_jpeg(50, 50))
            obj = api.content.create(
                type='Image',
                title='My Image1',
                container=portal)
            obj.setImage(generate_jpeg(50, 50))
            obj = api.content.create(
                type='Image',
                title='My Image2',
                container=portal)
            obj.setImage(generate_jpeg(50, 50))
            obj = api.content.create(
                type='File',
                title='My File',
                container=portal)
            obj.setFile(loadFile('lorem_ipsum.txt'))
            obj.reindexObject()
            obj = api.content.create(
                type='News Item',
                title='My News Item',
                container=portal)
            obj.setImage(generate_jpeg(50, 50))
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='brasil.gov.portlets:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='brasil.gov.portlets:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='brasil.gov.portlets:Robot',
)
