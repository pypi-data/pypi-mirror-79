# distroscraper - Raspberry Pi - verified 2020-09-13
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

def scraperpi(base, deepdive):
    with getsoup(base) as soup:
        images = soup.find_all(class_='image-info')

        for index, hrefidx in deepdive.items():
            img = images[index]
            dbg('EDITION-CONTENTS', img.contents)
            jsondumps({
                "name": "Raspbian",
                "edition": img.h3.text + ' - ' + img.contents[5].strong.text,
                "href": img.contents[hrefidx].a.attrs['href'],
                "description": img.contents[3].text})

def scrape():
    scraperpi('https://www.raspberrypi.org/downloads/raspberry-pi-os/', {0:15, 1:15, 2:15})
    scraperpi('https://www.raspberrypi.org/downloads/noobs/', {0:11, 1:11})

if __name__ == '__main__':
    config()
    scrape()
