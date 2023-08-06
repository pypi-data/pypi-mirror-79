# distroscraper - Arch Linux - verified 2020-09-13
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

def scrape():
    with getsoup('https://www.archlinux.org/download') as soup:

        match = soup.find('a', attrs={'title': 'Magnet link'})
        dbg("MATCH title:'Magnet link'", match)

        title = match.text.strip()[-10:]
        dbg("TITLE", title)

        jsondumps({
            "name": 'ArchLinux',
            "edition": title,
            "href": match.attrs['href'],
            "description": "Arch Linux monthly release " + title,
        })

if __name__ == '__main__':
    config()
    scrape()
