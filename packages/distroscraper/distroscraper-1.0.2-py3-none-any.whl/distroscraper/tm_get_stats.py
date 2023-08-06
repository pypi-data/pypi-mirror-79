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

import json
from functools import reduce

from distroscraper import tmlib

parser = tmlib.get_parser('Get statistics from all Transmissions torrents, one line json per torrent')
args = parser.parse_args()
tc = tmlib.client(args)

agg = {'torrentagg.downloaders': 0
        ,'torrentagg.interested': 0
        ,'torrentagg.leechers': 0
        ,'torrentagg.seeders': 0
        ,'torrentagg.peers': 0
        ,'torrentagg.rate_download': 0
        ,'torrentagg.rate_upload': 0
        ,'torrentagg.ratio': 0
        ,'torrentagg.uploaded_ever': 0}

count = 0

for t in tc.get_torrents():
    downloaders = reduce(lambda acc, cur: acc + 1 if cur['isUploadingTo'] else acc,
            t.peers, 0)
    interested = reduce(lambda acc, cur: acc + 1 if cur['peerIsInterested'] else acc,
            t.peers, 0)
    seeders = reduce(lambda acc, cur: acc + cur['seederCount'], t.trackerStats,
            0)
    leechers = reduce(lambda acc, cur: acc + cur['leecherCount'], t.trackerStats,
            0)
    
    print(json.dumps({'torrent.name': t.name
                     ,'torrent.downloaders': downloaders
                     ,'torrent.interested': interested
                     ,'torrent.leechers': leechers
                     ,'torrent.seeders': seeders
                     ,'torrent.peers': len(t.peers)
                     ,'torrent.rate_download': t.rateDownload
                     ,'torrent.rate_upload': t.rateUpload
                     ,'torrent.ratio': t.ratio
                     ,'torrent.uploaded_ever': t.uploadedEver
                     }))

    agg['torrentagg.downloaders'] += downloaders
    agg['torrentagg.interested'] += interested
    agg['torrentagg.leechers'] += leechers
    agg['torrentagg.seeders'] += seeders
    agg['torrentagg.peers'] += len(t.peers)
    agg['torrentagg.rate_download'] += t.rateDownload
    agg['torrentagg.rate_upload'] += t.rateUpload
    agg['torrentagg.ratio'] += t.ratio
    agg['torrentagg.uploaded_ever'] += t.uploadedEver

    count += 1

agg['torrentagg.ratio'] /= count

print(json.dumps(agg))
