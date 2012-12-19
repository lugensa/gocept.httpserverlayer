import gocept.httpserverlayer.tests.isolation.views
import grok


class App(grok.Model):
    pass


class DelegatingView(grok.View):
    # delegates actual functionality to the common isolation fixture, but lets
    # us register the views grok-style

    grok.context(object)

    def render(self):
        view = getattr(
            gocept.httpserverlayer.tests.isolation.views,
            self.__class__.__name__)()
        view.context = self.context
        return view()


class Set(DelegatingView):

    grok.name('set.html')


class Get(DelegatingView):

    grok.name('get.html')


class IncrementVolatile(DelegatingView):

    grok.name('inc-volatile.html')
