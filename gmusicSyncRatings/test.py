from rating_sync import RatingsSync

import unittest
import StringIO

from pprint import pprint

itunes_xml= """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Major Version</key><integer>1</integer>
	<key>Minor Version</key><integer>1</integer>
	<key>Date</key><date>2014-07-14T22:07:54Z</date>
	<key>Application Version</key><string>11.3</string>
	<key>Features</key><integer>5</integer>
	<key>Show Content Ratings</key><true/>
	<key>Music Folder</key><string>file://localhost/Users/user/Music/iTunes/iTunes%20Music/</string>
	<key>Library Persistent ID</key><string>B59FB62C26C8BCD4</string>
	<key>Tracks</key>
	<dict>
		<key>943</key>
		<dict>
			<key>Track ID</key><integer>943</integer>
			<key>Name</key><string>Orchestra Piece #1</string>
			<key>Artist</key><string>Mahito Yokota</string>
			<key>Composer</key><string>Mahito Yokota</string>
			<key>Album</key><string>The Legend of Zelda:  Twilight Princess</string>
			<key>Genre</key><string>Soundtrack</string>
			<key>Kind</key><string>AAC audio file</string>
			<key>Size</key><integer>3563609</integer>
			<key>Total Time</key><integer>127346</integer>
			<key>Disc Number</key><integer>1</integer>
			<key>Disc Count</key><integer>3</integer>
			<key>Track Number</key><integer>1</integer>
			<key>Track Count</key><integer>182</integer>
			<key>Year</key><integer>2006</integer>
			<key>BPM</key><integer>74</integer>
			<key>Date Modified</key><date>2011-07-20T18:21:05Z</date>
			<key>Date Added</key><date>2007-09-20T20:10:15Z</date>
			<key>Bit Rate</key><integer>192</integer>
			<key>Sample Rate</key><integer>48000</integer>
			<key>Comments</key><string>Arranged by Michiru Oshima</string>
			<key>Play Count</key><integer>62</integer>
			<key>Play Date</key><integer>3476646675</integer>
			<key>Play Date UTC</key><date>2014-03-02T22:11:15Z</date>
			<key>Skip Count</key><integer>7</integer>
			<key>Skip Date</key><date>2008-01-06T17:31:44Z</date>
			<key>Rating</key><integer>100</integer>
			<key>Album Rating</key><integer>80</integer>
			<key>Artwork Count</key><integer>2</integer>
			<key>Sort Album</key><string>Legend of Zelda:  Twilight Princess</string>
			<key>Persistent ID</key><string>D730B596DD5934B6</string>
			<key>Track Type</key><string>File</string>
			<key>File Type</key><integer>1295270176</integer>
			<key>Location</key><string>file://localhost/Users/bilalh/Music/iTunes/iTunes%20Music/Music/Mahito%20Yokota/The%20Legend%20of%20Zelda_%20%20Twilight%20Princess/1-01%20Orchestra%20Piece%20%231.m4a</string>
			<key>File Folder Count</key><integer>5</integer>
			<key>Library Folder Count</key><integer>1</integer>
		</dict>
		<key>945</key>
		<dict>
			<key>Track ID</key><integer>945</integer>
			<key>Name</key><string>Sinful Rose</string>
			<key>Artist</key><string>Tenpei Sato</string>
			<key>Album Artist</key><string>Tenpei Sato</string>
			<key>Album</key><string>Makai Senki Disgaea 2 Cursed Memories Best Of Soundtrack</string>
			<key>Grouping</key><string>_Lyrics, ps2,</string>
			<key>Genre</key><string>Soundtrack</string>
			<key>Kind</key><string>AAC audio file</string>
			<key>Size</key><integer>4507721</integer>
			<key>Total Time</key><integer>99933</integer>
			<key>Disc Number</key><integer>1</integer>
			<key>Disc Count</key><integer>1</integer>
			<key>Track Number</key><integer>1</integer>
			<key>Track Count</key><integer>20</integer>
			<key>Year</key><integer>2006</integer>
			<key>BPM</key><integer>141</integer>
			<key>Date Modified</key><date>2011-04-17T16:10:52Z</date>
			<key>Date Added</key><date>2007-09-26T15:13:06Z</date>
			<key>Bit Rate</key><integer>320</integer>
			<key>Sample Rate</key><integer>48000</integer>
			<key>Play Count</key><integer>3</integer>
			<key>Play Date</key><integer>3486636672</integer>
			<key>Play Date UTC</key><date>2014-06-26T13:11:12Z</date>
			<key>Skip Count</key><integer>15</integer>
			<key>Skip Date</key><date>2013-08-08T14:08:22Z</date>
			<key>Rating</key><integer>100</integer>
			<key>Album Rating</key><integer>80</integer>
			<key>Artwork Count</key><integer>1</integer>
			<key>Persistent ID</key><string>7BCA452BB2D4BF5E</string>
			<key>Track Type</key><string>File</string>
			<key>File Type</key><integer>1295270176</integer>
			<key>Location</key><string>file://localhost/Users/bilalh/Music/iTunes/iTunes%20Music/Music/Tenpei%20Sato/Makai%20Senki%20Disgaea%202%20Cursed%20Memories%20Best%20Of%20Soundtrack/01%20Sinful%20Rose.m4a</string>
			<key>File Folder Count</key><integer>5</integer>
			<key>Library Folder Count</key><integer>1</integer>
		</dict>
	</dict>
</dict>
</plist>
"""

tracks_parsed = {
 ('Orchestra Piece #1', 'Mahito Yokota', 'The Legend of Zelda:  Twilight Princess', 1): 
		{u'album': 'The Legend of Zelda:  Twilight Princess',
		u'artist': 'Mahito Yokota',
		u'beatsPerMinute': 74,
		u'comment': 'Arranged by Michiru Oshima',
		u'composer': 'Mahito Yokota',
		u'discNumber': 1,
		u'playCount': 62,
		u'rating': 5,
		u'title': 'Orchestra Piece #1',
		u'totalDiscCount': 3,
		u'totalTrackCount': 182,
		u'trackNumber': 1,
		u'year': 2006},
 ('Sinful Rose', 'Tenpei Sato', 'Makai Senki Disgaea 2 Cursed Memories Best Of Soundtrack', 1): 
	 	{u'album': 'Makai Senki Disgaea 2 Cursed Memories Best Of Soundtrack',
		u'albumArtist': 'Tenpei Sato',
		u'artist': 'Tenpei Sato',
		u'beatsPerMinute': 141,
		u'discNumber': 1,
		u'playCount': 3,
		u'rating': 5,
		u'title': 'Sinful Rose',
		u'totalDiscCount': 1,
		u'totalTrackCount': 20,
		u'trackNumber': 1,
		u'year': 2006}
}

class GmusicTests(unittest.TestCase):

    def test_parse(self):
		rs = RatingsSync(username=None, password=None, 
					itunes_xml= StringIO.StringIO(itunes_xml), only_rated=True)
		
		tracks = rs.get_all_itunes_tracks()
		self.assertEquals(len(tracks), 2, "Number of tracks parsed")
		self.assertEquals(tracks, tracks_parsed)
        
if __name__ == '__main__':
    unittest.main()