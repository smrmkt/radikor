#!/usr/bin/env python
#-*-coding:utf-8-*-

import argparse
from radikor.radikor import RadikoPlayer

# args
parser = argparse.ArgumentParser()
parser.add_argument('menu', type=str)
parser.add_argument('ch', nargs='?', type=str, default='FMT'),
parser.add_argument('duration', nargs='?', type=int, default=1)
parser.add_argument('out_dir', nargs='?', type=str, default='/tmp/radikor')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.menu == 'play':
        RadikoPlayer(args.ch).play()
    elif args.menu == 'record':
        RadikoPlayer(args.ch).record(args.duration, args.out_dir)
    elif args.menu == 'list':
        RadikoPlayer().list()



