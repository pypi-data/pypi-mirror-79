""""convert markdown to html and do other markdown operations"""

from typing import List
from dateutil import parser
from bs4 import BeautifulSoup

import os, bs4, time, markdown

from .etc import Config
from . import APPLICATION_DATA_DIR

def read_md(mdpath) -> str:
    if not os.path.isfile(mdpath): raise FileNotFoundError(f'markdown path = {mdpath} doesnt exist!')
    if not mdpath.endswith('.md'): raise TypeError(f'file {mdpath} must be an .md file')

    with open(mdpath, 'r') as f:
        mdfile = f.readlines()
        mdfile = ''.join(mdfile)
    
    return mdfile
    
def md2html(md) -> str:
    return markdown.markdown(md, extensions=['fenced_code'])

def md2bs4(md: str) -> BeautifulSoup:
    md = md2html(md)
    return BeautifulSoup(md, 'html.parser')

def html2bs4(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, 'html.parser')

def decorate_message(html, author, timestamp, base_url, color_scheme='nbmessage-default'):
    decorated_message = f"""
    <div class="row col-md-8 nbmessage-border">
        {html}
        <div class="col-xs-4 nbmessage-background {color_scheme}">
            <div class="col-xs-12 user-fmt">
                <p class="{color_scheme}"><i id="timestamp">{timestamp}</i></p>
            </div>
            <div class="col-xs-2 nbmessage-thumbnail">
                <img id="nbmessage-thumbnail-img" src="{os.path.join(base_url, 'nbmessage/images/ucsd-0.png')}" class="img-fluid img-thumbnail" alt="...">
            </div>
            <div class="col-xs-8" style="padding-top: .3em">
                <h5 class="user-fmt {color_scheme}"><strong>{author}</strong></h5>
            </div>
        </div>
    </div>
    """
    return decorated_message
        
