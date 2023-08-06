from io import StringIO

from hypothesis import given, strategies
from lxml.etree import XMLSyntaxError

from jupyxml import JupyXML
from lxml import etree


@given(strategies.text(min_size=1))
def test_unicode(text):

    # Only check if JupyXML handles if, if it can be parsed by lxml
    xml = f"<a>{text}</a>"

    try:
        i = StringIO(xml)
        e = etree.parse(i)
        parsed = True
    except XMLSyntaxError as e:
        parsed = False

    if parsed:
        # I have to force as string here, as some cases were failing trying to load the file
        j = JupyXML(xml, force_as_string=True)
        assert text in j._repr_html_()
