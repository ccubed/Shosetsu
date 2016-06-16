# Shosetsu
[![Build Status](https://travis-ci.org/ccubed/Shosetsu.svg?branch=master)](https://travis-ci.org/ccubed/Shosetsu)
[![codecov](https://codecov.io/gh/ccubed/Shosetsu/branch/master/graph/badge.svg)](https://codecov.io/gh/ccubed/Shosetsu)
Python VNDB API Bindings for Python 3.5+ using asyncio. 
(really I just scrape the website, because the tcp api doesn't even follow its own rules)

# Current Endpoints
## Shosetsu.search_vndb(stype, term)
```
    Search vndb.org for a term and return matching results from type.

        :param stype: type to search for.
            Type should be one of:
                v - Visual Novels
                r - Releases
                p - Producers
                s - Staff
                c - Characters
                g - Tags
                i - traits
                u - Users
        :param term: string to search for
        :return: Results. Result format depends on what you searched for. See the Parsing.py module for more specific documentation.

        Exceptions:
            aiohttp.HttpBadRequest - On 404s
            VNDBOneResult - When you search for something but it instead redirects us to a direct content page
            VNDBNoResults - When nothing was found for that search
            VNDBBadStype - Raised when an incorrect search type is passed
```
    
## Example Return Data
Please see [Parsing.py](https://github.com/ccubed/Shosetsu/blob/master/Shosetsu/Parsing.py) for information about return types for each search category.

## Shosetsu.get_novel(term)
```
If term is an ID will return that specific ID. If it's a string, it will return the details of the first search result for that term.
        Returned Dictionary Has the following structure:
        Please note, if it says list or dict, it means the python types.
        Indentation indicates level. So English is ['Titles']['English']

        'titles' - Contains all the titles found for the anime
            'english' - English title of the novel
            'alt' - Alternative title (Usually the Japanese one, but other languages exist)
            'aliases' - A list of str that define the aliases as given in VNDB.
        'img' - Link to the Image shown on VNDB for that Visual Novel (May be NSFW, I don't filter those)
        'length' - Length given by VNDB
        'developers' - A list containing the Developers of the VN.
        'publishers' - A list containing the Publishers of the VN.
        'tags' - Contains 3 lists of different tag categories
            'content' - List of tags that have to do with the story's content as defined by VNDB. Ex: Edo Era
            'technology' - List of tags that have to do with the VN's technology. Ex: Protagonist with a Face (Wew Lad, 21st century)
            'erotic' - List of tags that have to do with the VN's sexual content. Ex: Tentacles
        'releases' - A list of dictionaries. They have the following format.
            'date' - Date VNDB lists for release
            'ages' - Age group appropriate for as determined on VNDB
            'platform' - Release Platform
            'name' - The name for this particular Release
            'id' - The id for this release, also doubles as the link if you append https://vndb.org/ to it

        :param term: id or name to get details of.
        :return dict: Dictionary with the parsed results of a novel
```

## Example return data
```
{
	'titles': {
		'english': 'Hakuouki Zuisouroku', 
		'alt': '薄桜鬼 随想録', 
		'aliases': ['Hakuoki Zuisouroku']
	}, 
	'length': None, 
	'publishers': ['Idea Factory Co., Ltd.', 'Aksys Games'], 
	'img':'https://s.vndb.org/cv/42/17942.jpg', 
	'tags': {
		'content': ['Edo Era', 'Shinsengumi', 'Female Protagonist', 'Hero in Kimono', 'Samurai Hero', 'Cheerful Hero', 'Early Modern Period Earth', 'Bakumatsu'], 
		'technology': ['Otome Game', 'No Sexual Content', 'Protagonist With a Face'], 
		'erotic': None
	}, 
	'developers': ['Otomate', 'Design Factory Co., Ltd.'], 
	'releases': {
		'english': [{'id': 'r30158',
					 'platform': 'PlayStation 3', 
					 'ages': '17+', 'Date': '2014-05-06', 
					 'name': 'Hakuoki: Stories of the Shinsengumi - Standard Edition'
					 }], 
		'japanese': [{'id': 'r3515', 
			          'platform': 'PlayStation 2', 
			          'ages': '12+', 
			          'date': '2009-08-27', 
			          'name': 'Hakuoki Zuisouroku - Limited Edition'}]
	}
}
```