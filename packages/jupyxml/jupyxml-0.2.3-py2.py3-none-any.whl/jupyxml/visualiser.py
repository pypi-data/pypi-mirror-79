import os
from datetime import datetime
from io import StringIO

from lxml import etree

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from typing import Union, TextIO, AnyStr

from jupyxml.accordian_creator import create_recursive_accordion_html
from . import styles


class JupyXML:

    def __init__(self, xml_file_or_path: Union[AnyStr, TextIO], force_as_string: bool = False,
                 **render_kwargs):
        self.xml_file_or_path = xml_file_or_path
        if not force_as_string and os.path.exists(xml_file_or_path):
            self._file = self.xml_file_or_path
        else:
            self._file = StringIO(xml_file_or_path)
        self.root = etree.parse(self._file)
        self.render_kwargs = render_kwargs

    def _repr_html_(self) -> AnyStr:
        root_identifier = str(datetime.now().timestamp()).replace(".", "")
        cards = create_recursive_accordion_html(self.root.getroot(), root_identifier=root_identifier,
                                                **self.render_kwargs)
        css = pkg_resources.read_text(styles, 'jupyxml.css')
        # Concatenate css and cards. TODO: It would be nice if the css was "once-only"
        # TODO: Ability to turn off CSS adding
        html_representation = f"""
            <div class="jupyxml">
                <style scoped>
                    {css}
                </style>
                {cards}
            </div>
        """
        return html_representation
