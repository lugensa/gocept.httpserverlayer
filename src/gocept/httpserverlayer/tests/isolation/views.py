import zope.security.proxy


class Set(object):

    def __call__(self):
        c = zope.security.proxy.removeSecurityProxy(self.context)
        c.foo = 1
        return 'setting done'


class Get(object):

    def __call__(self):
        c = zope.security.proxy.removeSecurityProxy(self.context)
        return str(getattr(c, 'foo', 0))


class Error(object):

    def __call__(Self):
        raise ValueError()


class IncrementVolatile(object):

    def __call__(self):
        c = zope.security.proxy.removeSecurityProxy(self.context)
        if hasattr(c, 'aq_base'):
            c = c.aq_base

        if not hasattr(c, '_v_counter'):
            c._v_counter = 0
        c._v_counter += 1
        return str(c._v_counter)
