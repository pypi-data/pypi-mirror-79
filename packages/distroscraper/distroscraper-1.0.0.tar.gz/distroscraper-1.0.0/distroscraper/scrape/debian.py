# distroscraper - Debian - verified 2020-09-13
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

from distroscraper.lib import config,dbg,jsondumps,getsoup

def scrapeDebian(edition, base):
    with getsoup(base) as soup:

        match = soup.find_all('a')
        dbg("MATCH soup.find_all('a')", match)

        torrents = filter(lambda x: x.attrs['href'].endswith('.torrent'), match)
        dbg('TORRENTS', torrents)

        for t in torrents:
            href = t.attrs['href']
            jsondumps({
                    "name": "Debian",
                    "edition": edition,
                    "href": base + href,
                    "description": href})

def scrape():
    scrapeDebian("Free (amd64 dvd)",
            'https://cdimage.debian.org/debian-cd/current/amd64/bt-dvd/')
    scrapeDebian("Nonfree (amd64 dvd firmware)",
            'https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/current/amd64/bt-dvd/')
    scrapeDebian("Live (amd64 hybrid firmware)",
            'https://cdimage.debian.org/cdimage/unofficial/non-free/cd-including-firmware/current-live/amd64/bt-hybrid/')

if __name__ == '__main__':
    config()
    scrape()
