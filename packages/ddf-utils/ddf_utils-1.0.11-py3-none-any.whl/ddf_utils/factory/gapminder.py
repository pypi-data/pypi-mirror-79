# -*- coding: utf-8 -*-

"""Gapminder spreadsheets readers

Note to myself:

so we should have a fixed format
but it seems that not every file have this format.
what should I do?
"""

#TODO: complete this

import parse
from io import BytesIO
from . common import requests_retry_session, DataFactory, download


def open_google_spreadsheet(docid):
    """load a google spreadsheet and return it as BytesIO file."""
    tmpl_xls = "https://docs.google.com/spreadsheets/d/{docid}/export?format=xlsx&id={docid}"
    url = tmpl_xls.format(docid=docid)
    session = requests_retry_session()
    res = session.get(url)
    if res.ok:
        return BytesIO(res.content)
    return None


def get_docid_sheet(link):
    p = parse.parse(
        "https://docs.google.com/spreadsheets/d/{docid}/gviz/tq?tqx=out:csv&sheet={sheet_name}",
        link)
    docid = p.named['docid']
    sheet_name = p.named['sheet_name']

    return docid, sheet_name
