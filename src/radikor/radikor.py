#!/usr/bin/env python
#-*-coding:utf-8-*-

from radiko import Radiko

class Radikor:
    def __init__(self):
        self.radiko = Radiko()

    def play(self, ch='FMT'):
        self.radiko.play(ch)

    def record(self, ch, duration, out_dir):
        self.radiko.record(ch, duration, out_dir)

    def list(self):
        self.radiko.list()