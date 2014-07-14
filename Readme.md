gmusic-sync-rating  [![Build Status](https://travis-ci.org/Bilalh/gmusic-sync-rating.svg?branch=master)](https://travis-ci.org/Bilalh/gmusic-sync-rating)
==================

`gmusic-sync-rating` is a command line tool to sync iTunes rating to google music. It supports the 5 star rating scale.

##Installation

`gmusic-sync-rating` can be installed from PyPI using pip:

	$ pip install gmusic-sync-rating



##Usage

	usage: gmusicSyncRatings [-h] [--password PASSWORD] [--itunes-xml FILE]
	                         [--only-rated]
	                         username

	positional arguments:
	  username             Google music Username

	optional arguments:
	  -h, --help           show this help message and exit
	  --password PASSWORD  Google music Password
	  --itunes-xml FILE    iTunes xml file
	  --only-rated         Only sync non empty ratings


### `--password`

If `--password` is not specified then `gmusic-sync-rating` will prompt you to enter it

	$ gmusicSyncRatings 'myemail@example.com'
	Enter your google music password
	Password:

###`--only-rated`

Only upload non empty rating.

###`--itunes-xml FILE`

If you keep your iTunes library in an non standard location (i.e not ~/Music/iTunes/), you have specify the full path to ` `iTunes Music Library.xml` in your iTunes folder. 


License
-------
`gmusic-sync-rating` is licensed under the `Apache 2.0 License`
