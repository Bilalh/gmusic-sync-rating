#!/usr/bin/env python2.7

import logging
rootLogger = logging.getLogger()
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.WARN)
consoleHandler.setFormatter(logging.Formatter('[Log]    %(message)s'))
logging.getLogger().addHandler(consoleHandler)
logger = logging.getLogger(__name__)

from gmusicapi import Mobileclient
from pprint import pprint

import argparse
import xml.etree.cElementTree as ET


def make_track_key(fields):
    """  Makes a unique key for each track """
    # For Efficient Lookups
    return (
        fields['title'],
        fields['artist'],
        fields['album'],
        fields.get('trackNumber', 0))


def iter_many(it, length, num):
    """ iter_many([1,2,3,4],4, 2) -> [1,2] [3,4] """
    for i in xrange(0, length, num):
        yield (it[i:i + num])


class RatingsSync(object):

    def run(self):
        """ Run the sequence"""
        logger.warn("Logging in")
        mc = self.get_gmusic_client()

        logger.warn("Getting gmusic tracks")
        gtracks = self.get_all_gmusic_tracks(mc)

        logger.warn("Parsing itunes xml")
        itracks = self.get_all_itunes_tracks("/Users/bilalh/Music/iTunes/iTunes Music Library.xml")

        logger.warn("Trying to match tracks")
        updated = self.update_matching(itracks, gtracks)

        if updated == []:
            logger.warn("No tracks to update")
        else:
            self.sync_metadata(updated, mc)


    def sync_metadata(self, updated, mc):
        """ Perform the changes """
        mc.change_song_metadata(updated)


    def update_matching(self, itracks, gtracks, only_itunes_rated=True):
        """ Updates gtracks with new ratings, and return the tracks which need updating"""

        updated=[]
        for (k, fields) in itracks.items():
            if only_itunes_rated and 'rating' not in fields:
                continue

            if k in gtracks:
                old=gtracks[k]['rating']
                if old != fields['rating']:
                    gtracks[k]['rating'] = fields['rating']
                    logger.info("Found %s, %s --> %s", k, old, gtracks[k]['rating'])

                    updated.append(gtracks[k])

        logger.warn("Found %d tracks in gmusic to update", len(updated))
        return updated


    def get_gmusic_client(self):
        """ Return the api object if successful """
        mc = Mobileclient()
        mc.login('user', 'password')
        return mc


    def get_all_gmusic_tracks(self, mc):
        """ All of the user's gmusic tracks """
        tracks = []
        for songs in mc.get_all_songs(incremental=True):
            tracks += songs
            logger.warn("Gathered %d tracks' info", len(tracks))

        return { make_track_key(t): self.int_fields(t) for t in tracks }


    def get_all_itunes_tracks(self, xml_file):
        """ All of the user's itunes tracks """

        logger.warn("Loading XML file...")
        tree = ET.parse(xml_file)
        logger.warn("XML file loaded")

        logger.warn("Extracting songs...")

        def f(fields):
            res = self.int_fields(fields)

            if "rating" in res:
                # iTunes uses a 100 point scale convert to 1 to 5 scale
                res['rating'] /= 20

            return res

        tracks = [ f({ itunes_to_gmusic[k.text]: v.text
            for (k, v) in iter_many(fields, len(fields), 2)
                if k.text in itunes_to_gmusic.keys() })
            for fields in tree.iterfind('.//dict/dict/dict') ]

        logger.warn("%d Songs extracted", len(tracks))

        return { make_track_key(t): t for t in tracks }


    def int_fields(self, fields):
        # Convert int fields to ints
        for k in ['totalDiscCount', 'rating', 'year', 'totalTrackCount',
                'beatsPerMinute', 'year', 'trackNumber', 'discNumber', 'playCount']:
            if k in fields:
                fields[k] = int(fields[k])

        return fields


itunes_keys={'Album', 'Album Artist', 'Album Rating', 'Artist', 'Artwork Count', 'BPM', 'Bit Rate',
'Comments', 'Composer', 'Date Added', 'Date Modified', 'Disc Count', 'Disc Number', 'File Folder Count',
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
    'Artist'           : u'artist',
    'Album'            : u'album',
    'Album Artist'     : u'albumArtist',
    'BPM'              : u'beatsPerMinute',
    'Comments'         : u'comment',
    'Composer'         : u'composer',
    'Disc Number'      : u'discNumber',
    'genre'            : u'genre',
    'Play Count'       : u'playCount',
    'Rating'           : u'rating', # Need to convert
    'Name'             : u'title',
    'Disc Count'       : u'totalDiscCount',
    'Track Count'      : u'totalTrackCount',
    'Track Number'     : u'trackNumber',
    'Year'             : u'year'
}

# if __name__ == "__main__":
rs = RatingsSync()
rs.run()
