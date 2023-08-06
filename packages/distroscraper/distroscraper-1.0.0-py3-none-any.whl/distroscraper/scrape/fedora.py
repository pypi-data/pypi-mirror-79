# distroscraper - Fedora - verified 2020-09-13
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
    with getsoup('https://torrent.fedoraproject.org/') as soup:

        match = soup.find('table')
        dbg('MATCH table', match.contents)

        versionLabel = False

        for i, row in enumerate(match.contents):
            row = match.contents[i]
            # Skip blank lines
            if row == ' ':
                continue

            dbg('ROW ' + str(i), row.contents)

            # Skip headers
            if len(row.find_all('th')) > 0:
                continue

            # Skip first version label.  Break after second version label - get only most recent
            if 'class' in row.find('td').attrs:
                if versionLabel:
                    break
                else:
                    versionLabel = True
                    continue

            # Every row left over should be a torrent
            jsondumps({
                "name": 'Fedora',
                "edition": row.contents[3].text,
                "href": row.contents[1].a.attrs['href'],
                "description": row.contents[3].text + ' - ' + row.contents[9].text})

if __name__ == '__main__':
    config()
    scrape()
