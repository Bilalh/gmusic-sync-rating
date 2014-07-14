# coding: utf-8
"""
:copyright: 2014 Bilal Syed Hussain
:license: Apache 2.0
"""

import logging
import argparse
import getpass
import sys
from pprint import pformat
from os.path import expanduser, exists

logger = logging.getLogger(__name__)

def handle_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("username", help='Google music Username')
    parser.add_argument("--password", help='Google music Password')
    parser.add_argument("--itunes-xml", default='~/Music/iTunes/iTunes Music Library.xml',
        help='iTunes xml file', metavar='FILE')
    parser.add_argument('--only-rated',  action='store_true', 
        help='Only sync non empty ratings')

    args = parser.parse_args()
    
    if not args.password:
        print("Enter your google music password")
        args.password = getpass.getpass()
        if not args.password:
            print("Password can't be empty")
            sys.exit(2)
    
    args.itunes_xml = expanduser(args.itunes_xml)
    if not exists(args.itunes_xml):
        print("%s does not exist" % args.itunes_xml )
        sys.exit(3)
    
    logger.info("args:",pformat(args))
    return args