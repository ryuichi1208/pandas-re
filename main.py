import contextlib
import datetime
import gzip
import io
import logging
import re
import sys
import time
import uuid
import warnings
import zlib

import msgpack
import pandas as pd
import requests
import tdclient
import tdclient.version

from urllib.parse import urlparse
from urllib.parse import parse_qsl

try:
    import IPython
    import IPython.display
except ImportError:
    IPython = None


logger = logging.getLogger(__name__)


class Connection(object):
    def __init__(self, apikey=None, endpoint=None, **kwargs):
        if apikey is not None:
            kwargs["apikey"] = apikey
        if endpoint is not None:
            if not endpoint.endswith("/"):
                endpoint = endpoint + "/"
            kwargs["endpoint"] = endpoint
        if "user_agent" not in kwargs:
            versions = [
                "pandas/{0}".format(pd.__version__),
                "tdclient/{0}".format(tdclient.version.__version__),
                "Python/{0}.{1}.{2}.{3}.{4}".format(*list(sys.version_info)),
            ]
            kwargs["user_agent"] = "pandas-td/{0} ({1})".format(
                __version__, " ".join(versions)
            )
        self.kwargs = kwargs
        self.client = self.get_client()

    def get_client(self):
        return tdclient.Client(**self.kwargs)

    @property
    def apikey(self):
        return self.client.api.apikey

    @property
    def endpoint(self):
        return self.client.api.endpoint

class QueryEngine(object):
    def __init__(
        self,
        connection,
        database,
        params=None,
        header=False,
        show_progress=False,
        clear_progress=False,
    ):
        self.connection = connection
        self.database = database
        self._params = {} if params is None else params
        self._header = header
        if IPython and not sys.stdout.isatty():
            self.show_progress = show_progress
            self.clear_progress = clear_progress
        else:
            self.show_progress = False
            self.clear_progress = False

    @property
    def type(self):
        return self._params.get("type")

    def create_header(self, name):
        # name
        if self._header is False:
            header = ""
        elif isinstance(self._header, str):
            header = "-- {0}\n".format(self._header)
        else:
            header = "-- {0}\n".format(name)
        return header

    def _html_text(self, text):
        return '<div style="color: #888;"># {0}</div>'.format(text)

    def _html_presto_output(self, output):
        html = ""
        # started at
        for text in re.findall(r"started at.*", output):
            html += self._html_text(text)
        # warning
        html += '<pre style="color: #c44;">'
        for text in re.findall(r"\n\*\* .*", output):
            html += "{0}".format(text)
        html += "</pre>\n"
        # progress
        progress = None
        for progress in re.findall(
            r"\n(\d{4}-\d{2}-\d{2}.*\n\d{8}.*(?:\n *\[\d+\].*)+)", output
        ):
            pass
        if progress:
            html += "<code><small><small>{0}</small></small></code>".format(progress)
        # finished at
        for rows, finished in re.findall(r"\n(\d+ rows.*)\n(finished at.*)", output):
            html += "{0}<br>".format(rows)
            html += self._html_text(finished)
        return html
