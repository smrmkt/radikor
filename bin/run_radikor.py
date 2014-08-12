#!/usr/bin/env python
#-*-coding:utf-8-*-

import argparse
import os.path
import sys

# path
script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../src/radikor')

from radikor import Radikor

# args
parser = argparse.ArgumentParser()
parser.add_argument('menu', type=str)
parser.add_argument('ch', nargs='?', type=str, default='FMT'),
parser.add_argument('duration', nargs='?', type=int, default=1)
parser.add_argument('out_dir', nargs='?', type=str, default='/tmp/radikor')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.menu == 'play':
        Radikor().play(args.ch)
    elif args.menu == 'record':
        Radikor().record(args.ch, args.duration, args.out_dir)
    elif args.menu == 'list':
        Radikor().list()



