# distroscraper - transmissionrpc utilities
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

import argparse

from distroscraper import tmlib

parser = tmlib.get_parser('Add a torrent HTTP or Magnet URL to Transmission')
parser.add_argument('--download-dir', help='Download dir for all specified torrents')
parser.add_argument('torrents', metavar='TORRENT', nargs='+', help='Torrrent HTTP or Magnet URL')
args = parser.parse_args()

tc = tmlib.client(args)

for torrent in args.torrents:
    if args.download_dir:
        t = tc.add_torrent(torrent, download_dir=args.download_dir)
    else:
        t = tc.add_torrent(torrent)
    print('Added {}'.format(t.name))

