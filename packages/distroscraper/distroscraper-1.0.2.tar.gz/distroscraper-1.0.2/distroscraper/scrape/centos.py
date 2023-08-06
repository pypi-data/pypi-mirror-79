# distroscraper - CentOS - verified 2020-09-13
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
    with getsoup('https://www.centos.org/download/') as soup:

        atags = soup.find_all('a')
        href = ''
        for tag in atags:
            if tag.text == 'via Torrent':
                href = tag.attrs['href']
                break
        if href == '':
            raise 'Could not find "via Torrent" link for CentOS'

        with getsoup(href) as subsoup:
            main = subsoup.find('main')
            nextlink = main.find('a').attrs['href']

            with getsoup(nextlink) as subsubsoup:
                links = subsubsoup.find_all('a')
                dbg('LINKS', links)
                for link in links:
                    href = link.attrs['href']
                    if href.startswith('CentOS-') and href.endswith('.torrent'):
                        jsondumps({
                            "name": "CentOS",
                            "edition": href,
                            "href": nextlink + href,
                            "description": href})

if __name__ == '__main__':
    config()
    scrape()
