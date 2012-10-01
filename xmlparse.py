try:
    from lxml import etree
    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree
                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place, using libxml2")

"""
Steps:

    __init__:
        self.schema = parse(load(schema))
        self.dtd = parse(load(dtd))
        self.xml = parse(load(xml))

    Load:
        urllib / os.path

    Validate dtd:
        elTree
        no dtd, use previous
        no previous, simply validate well-formedness

    Refresh:
        time = 10mins?
        if schema:
            refresh(schema, time)
        if dtd:
            refresh(dtd, time)

    Autofill:
        compare location in path to dtd
        show EXPECTED in dropdown

    ZencodeXML:
        autofill ZencodeXML
"""


class xmlLintUtils():

    def __init__(self, xmlFile):
        pass

    def _refresh(self, file):
        pass

    def load(self, entity):
        # load schema, dtd, etc
        pass