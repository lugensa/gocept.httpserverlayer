from shoobx.junitxml import feature
import zope.testrunner
import zope.testrunner.runner


# Code taken from https://github.com/shoobx/shoobx.junitxml
feature.JUnitXMLSupport.install_options()


class Runner(zope.testrunner.runner.Runner):
    """Customized test runner."""

    def configure(self):
        super(Runner, self).configure()
        self.features.append(feature.JUnitXMLSupport(self))


zope.testrunner.runner.Runner = Runner


def test_runner():
    """Entry point for to run the tests with `JUnitXMLSupport`."""
    return zope.testrunner.run()
