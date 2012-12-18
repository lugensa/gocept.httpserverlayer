import gocept.httpserverlayer.plonetesting
import gocept.httpserverlayer.plonetesting.testing
import plone.app.testing.layers
import plone.testing


PLONE_LAYER = plone.testing.Layer(
    name='PloneLayer',
    bases=(gocept.httpserverlayer.plonetesting.testing.Z2_LAYER,
           plone.app.testing.layers.PLONE_FIXTURE))


HTTP_LAYER = plone.testing.Layer(
    name='HTTPLayer',
    bases=(PLONE_LAYER, gocept.httpserverlayer.plonetesting.HTTP_SERVER))
