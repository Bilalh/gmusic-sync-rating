#!/usr/bin/env python2.7

from gmusicapi import Mobileclient
from pprint import pprint

import argparse
import logging
import xml.etree.cElementTree as ET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def iter_many(it, length, num):
    """ iter_many([1,2,3,4],4, 2) -> [1,2] [3,4] """
    for i in xrange(0, length, num):
        yield (it[i:i + num])


class RatingsSync(object):

    def run(self):
        logger.info("Logging in")
        mc = self.get_gmusic_client()
        logger.info("Getting gmusic tracks")
        gtracks = self.get_all_gmusic_tracks(mc)
        logger.info("Parsing itunes xml")
        itracks = self.get_all_itunes_tracks("/Users/bilalh/Music/iTunes/iTunes Music Library.xml")
        raise

    def get_gmusic_client(self):
        mc = Mobileclient()
        mc.login('user', 'password')
        return mc

    def get_all_gmusic_tracks(self, mc):
        """ all of the user's gmusic tracks """
        tracks = []
        for track in mc.get_all_songs(incremental=True):
            tracks += track
            logger.info("Gathered %d tracks info", len(tracks))

        # tracks = [song for song in tracks]
        return sorted(tracks, key=lambda t: t['title'])


    def get_all_itunes_tracks(self, xml_file):
        """ all of the user's itunes tracks """

        logger.info("Loading XML file...")
        tree = ET.parse(xml_file)
        logger.info("XML file loaded")

        logger.info("Extracting songs...")

        def f(fields):
            # Convert int fields to ints
            for k in ['totalDiscCount', 'rating', 'year', 'totalTrackCount',
                    'beatsPerMinute', 'year', 'trackNumber', 'discNumber', 'playCount']:
                if k in fields:
                    fields[k] = int(fields[k])

            if "rating" in fields:
                # iTunes uses a 100 point scale convert to 1 to 5 scale
                fields['rating'] /= 20

            return fields

        tracks = [ f({ itunes_to_gmusic[k.text]: v.text
            for (k, v) in iter_many(fields, len(fields), 2)
                if k.text in itunes_to_gmusic.keys() })
            for fields in tree.iterfind('.//dict/dict/dict') ]

        logger.info("%d Songs extracted", len(tracks))

        return tracks



itunes_keys={'Album', 'Album Rating', 'Artist', 'Artwork Count', 'BPM', 'Bit Rate', 'Comments',
'Composer', 'Date Added', 'Date Modified', 'Disc Count', 'Disc Number', 'File Folder Count',
'File Type', 'Genre', 'Kind', 'Library Folder Count', 'Location', 'Name', 'Persistent ID',
'Play Count', 'Play Date', 'Play Date UTC', 'Rating', 'Sample Rate', 'Size', 'Skip Count',
'Skip Date', 'Sort Album', 'Total Time', 'Track Count', 'Track ID', 'Track Number',
'Track Type', 'Year'}

gmusic_keys={u'album', u'albumArtRef', u'albumArtist', u'artist', u'beatsPerMinute',
u'clientId', u'comment', u'composer', u'creationTimestamp', u'deleted', u'discNumber',
u'durationMillis', u'estimatedSize', u'genre', u'id', u'kind', u'lastModifiedTimestamp',
u'playCount', u'rating', u'recentTimestamp', u'title', u'totalDiscCount', u'totalTrackCount',
u'trackNumber', u'year'}

itunes_to_gmusic={
    'Album'            : 'album',
    'BPM'              : 'beatsPerMinute',
    'Comments'         : 'comment',
    'Composer'         : 'composer',
    'Disc Number'      : 'discNumber',
    'genre'            : 'genre',
    'Play Count'       : 'playCount',
    'Rating'           : 'rating', # Need to convert
    'Name'             : 'title',
    'Disc Count'       : 'totalDiscCount',
    'Track Count'      : 'totalTrackCount',
    'Track Number'     : 'trackNumber',
    'Year'             : 'year'
}

if __name__ == "__main__":
    rs = RatingsSync()
    rs.run()
