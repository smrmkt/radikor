#!/usr/bin/env python
#-*-coding:utf-8-*-

import argparse
from lib.radiko_player import RadikoPlayer

# args
parser = argparse.ArgumentParser()
parser.add_argument('menu', type=str)
parser.add_argument('ch', nargs='?', type=str),
parser.add_argument('duration', nargs='?', type=int)
parser.add_argument('out_dir', nargs='?', type=str)

if __name__ == '__main__':
    args = parser.parse_args()
    if args.menu == 'play':
        RadikoPlayer(args.ch).play()
    elif args.menu == 'record':
        RadikoPlayer(args.ch).record(args.duration, args.out_dir)
    elif args.menu == 'list':
        RadikoPlayer().list()