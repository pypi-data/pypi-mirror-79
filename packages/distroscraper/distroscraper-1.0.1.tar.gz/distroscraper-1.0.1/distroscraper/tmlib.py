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

import transmissionrpc
import argparse

def get_parser(desc):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--host', '-H', default='localhost', help='Transmission RPC host (default localhost)')
    parser.add_argument('--port', '-P', type=int, default=9091, help='Transmission RPC port (default 9091)')
    parser.add_argument('--user', '-u', help='Transmission username')
    parser.add_argument('--password', '-p', help='Transmission password')
    return parser

def client(args):
    return transmissionrpc.Client(address=args.host, port=args.port, user=args.user, password=args.password)
