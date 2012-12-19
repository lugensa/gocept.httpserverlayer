import gocept.httpserverlayer.plonetestingz2
import gocept.httpserverlayer.plonetestingz2.testing
import plone.app.testing.layers
import plone.testing


PLONE_LAYER = plone.testing.Layer(
    name='PloneLayer',
    bases=(gocept.httpserverlayer.plonetestingz2.testing.Z2_LAYER,
           plone.app.testing.layers.PLONE_FIXTURE))


HTTP_LAYER = plone.testing.Layer(
    name='HTTPLayer',
    bases=(PLONE_LAYER, gocept.httpserverlayer.plonetestingz2.HTTP_SERVER))
