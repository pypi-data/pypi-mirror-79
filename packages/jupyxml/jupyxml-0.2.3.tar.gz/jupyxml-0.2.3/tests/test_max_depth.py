from jupyxml import JupyXML


def test_max_depth():
    inner_text = "askldjf;aksd"
    xml = f"<a><b><c><d>{inner_text}</d></c></b></a>"

    j = JupyXML(xml, force_as_string=True)
    assert inner_text in j._repr_html_()

    # Limit depth to 2, and now we shouldn't get the text
    j2 = JupyXML(xml, force_as_string=True, max_depth=2)
    assert inner_text not in j2._repr_html_()
