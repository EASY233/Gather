#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = EASY
import argparse
from api.data_from_fofa import Fofa
from api.data_from_zoomeye import ZoomEye
from api.data_from_shodan import Shodan

def cmdline():
    parser = argparse.ArgumentParser(description="Data was collected by using Fofa, Zoomeye and Shodan  --by EASY")
    target = parser.add_argument_group('Type')
    target.add_argument('-aF',dest='Fofa',default=False,action='store_true',help="Using fofa to collect data")
    target.add_argument('-aZ',dest='Zoomeye',default=False,action='store_true',help="Using Zoomeye to collect data")
    target.add_argument('-aS', dest='Shodan', default=False,action='store_true', help="Using Shodan to collect data")
    args = parser.parse_args()
    usage = '''
    Usage: python3 {} -aF or -aZ or -aS
    '''.format(parser.prog,parser.prog)
    options(args)

def options(args):
    if args.Fofa:
        Fofa()
    elif args.Zoomeye:
        ZoomEye()
    elif args.Shodan:
        Shodan()
