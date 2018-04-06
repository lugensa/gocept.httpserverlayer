try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

ENSURE_ORDER = False


class IsolationTests(object):
    """NOTE: Subclasses need to implement getRootFolder() and getDatabase().
    """

    # test_0_set and test_1_get verify that different test methods are isolated
    # from each other, i.e. that the underlying DemoStorage stacking is wired
    # up correctly

    def test_0_set(self):
        global ENSURE_ORDER
        r = urlopen('http://%s/set.html' % self.layer['http_address'])
        r = urlopen('http://%s/get.html' % self.layer['http_address'])
        self.assertEqual(b'1', r.read())
        ENSURE_ORDER = True

    def test_1_get(self):
        global ENSURE_ORDER
        self.assertEqual(
            ENSURE_ORDER, True, 'Set test was not run before get test')
        r = urlopen('http://%s/get.html' % self.layer['http_address'])
        self.assertNotEqual('1', r.read())
        ENSURE_ORDER = False

    def test_each_request_gets_a_separate_zodb_connection(self):
        r = urlopen(
            'http://%s/inc-volatile.html' % self.layer['http_address'])
        self.assertEqual(b'1', r.read())
        # We demonstrate isolation using volatile attributes (which are
        # guaranteed not to be present on separate connections). But since
        # there is no guarantee that volatile attributes disappear on
        # transaction boundaries, we need to prevent re-use of the first
        # connection -- to avoid trouble like "it's the same connection, so the
        # volatile attribute is still there".
        #
        # The proper way to do this would be two requests that are processing
        # concurrently, but a) we are not prepared for multi-threaded requests
        # and b) simulating that would be a major pain, so we cheat and force
        # the opening of another connection by claiming one here.
        db = self.getDatabase()
        conn = db.open()
        r = urlopen(
            'http://%s/inc-volatile.html' % self.layer['http_address'])
        conn.close()
        self.assertEqual(b'1', r.read())

    def test_requests_get_different_zodb_connection_than_tests(self):
        root = self.getRootFolder()
        root._v_counter = 1
        r = urlopen(
            'http://%s/inc-volatile.html' % self.layer['http_address'])
        self.assertEqual(b'1', r.read())
