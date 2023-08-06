# distroscraper - Linux Mint - verified 2020-09-13
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

def mint_get(href):
    with getsoup(href) as soup:
        table = soup.find(class_='sponsor-table')
        dbg('DEREF-SPONSOR-TABLE', table.contents)
        dbg('DEREF-SPONSOR-TABLE-TORRENT-ROW', table.contents[8].contents)
        dbg('DEREF-SPONSOR-TABLE-TORRENT-COL', table.contents[8].contents[3].contents)
        return table.contents[8].contents[3].contents[0].attrs['href']

def scrape():
    with getsoup('https://linuxmint.com/download.php') as soup:

        table = soup.find(class_='sponsor-table')
        dbg("SPONSOR-TABLE", table.contents)

        for index in [3, 5, 7]:
            dbg("EDITION-PARENT", table.contents[index].contents)
            edition = table.contents[index].contents[1].text + " (x86_64)"
            description = table.contents[index].contents[3].text

            dbg('DEREF-PARENT', table.contents[index].contents[1].contents)
            deref_href = 'https://linuxmint.com' + table.contents[index].contents[1].contents[0].attrs['href']
            href = mint_get(deref_href)
            jsondumps({
                "name": "Linux Mint",
                "edition": edition,
                "href": href,
                "description": description})

if __name__ == '__main__':
    config()
    scrape()
