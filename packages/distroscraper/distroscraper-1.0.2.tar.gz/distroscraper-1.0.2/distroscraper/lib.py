# distroscraper - utilities for distro torrent scrapers
# https://jefftickle.com/projects/distroscraper
# Copyright (C) 2020 Jeffrey W. Tickle
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import json
import logging
import contextlib

import requests
from bs4 import BeautifulSoup
from htmlmin import minify

def config():
    if 'DEBUG' in os.environ:
        logging.basicConfig(level=logging.DEBUG)

def dbg(*args):
    logging.debug(str(args))

def jsondumps(data):
    print(json.dumps(data))

@contextlib.contextmanager
def getsoup(href):
    with requests.get(href) as data:
        soup = BeautifulSoup(minify(data.text), 'lxml')
        yield soup
