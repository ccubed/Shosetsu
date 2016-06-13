# Shosetsu
Python VNDB API Bindings for Python 3.5+ using asyncio. 
(really I just scrape the website, because the tcp api doesn't even follow its own rules)

# Current Endpoints
## Shosetsu.search_visual_novels(term)
````
Search vndb.org for a term and return matching Visual Novels.
:param term: string to search for
:return: List of Dictionaries. Dictionaries contain a name and id.
```
    
## Example Return Data
```
[{'id': 'v5388', 'name': '3-days Marriage ~Hikarugenji no Koibito~'}, 
 {'id': 'v995', 'name': 'Altered Pink ~Tokumu Sentai Duel Ranger~'}, 
 {'id': 'v466', 'name': 'Doko e Iku no, Ano Hi'}, 
 {'id': 'v14581', 'name': 'Hotaru no Hikaru ~Fluorite~'}, 
 {'id': 'v3196', 'name': 'Ren no Koi ~Others~'}, 
 {'id': 'v2190', 'name': 'Seito Kaichou Hikaru ~Inma ni Senryousareta Gakuen~'}, 
 {'id': 'v2759', 'name': 'Shokusou! Mahou Shoujo Hikaru'}]
```    

## Shosetsu.get_novel(term)
```
If term is an ID will return that specific ID. If it's a string, it will return the details of the first search result for that term.
        Returned Dictionary Has the following structure:
        Please note, if it says list or dict, it means the python types.
        Indentation indicates level. So English is ['Titles']['English']

        'Titles' - Contains all the titles found for the anime
            'English' - English title of the novel
            'Alt' - Alternative title (Usually the Japanese one, but other languages exist)
            'Aliases' - A list of str that define the aliases as given in VNDB.
        'Img' - Link to the Image shown on VNDB for that Visual Novel (May be NSFW, I don't filter those)
        'Length' - Length given by VNDB
        'Developers' - A list containing the Developers of the VN.
        'Publishers' - A list containing the Publishers of the VN.
        'Tags' - Contains 3 lists of different tag categories
            'Content' - List of tags that have to do with the story's content as defined by VNDB. Ex: Edo Era
            'Technology' - List of tags that have to do with the VN's technology. Ex: Protagonist with a Face (Wew Lad, 21st century)
            'Erotic' - List of tags that have to do with the VN's sexual content. Ex: Tentacles
        'Releases' - A list of dictionaries. They have the following format.
            'Date' - Date VNDB lists for release
            'Ages' - Age group appropriate for as determined on VNDB
            'Platform' - Release Platform
            'Name' - The name for this particular Release
            'ID' - The id for this release, also doubles as the link if you append https://vndb.org/ to it

        :param term: id or name to get details of.
        :return dict: Dictionary with the parsed results of a novel
```

## Example return data
```
{
	'Titles': {
		'English': 'Hakuouki Zuisouroku', 
		'Alt': '薄桜鬼 随想録', 
		'Aliases': ['Hakuoki Zuisouroku']
	}, 
	'Length': None, 
	'Publishers': ['Idea Factory Co., Ltd.', 'Aksys Games'], 
	'Img':'https://s.vndb.org/cv/42/17942.jpg', 
	'Tags': {
		'Content': ['Edo Era', 'Shinsengumi', 'Female Protagonist', 'Hero in Kimono', 'Samurai Hero', 'Cheerful Hero', 'Early Modern Period Earth', 'Bakumatsu'], 
		'Technology': ['Otome Game', 'No Sexual Content', 'Protagonist With a Face'], 
		'Erotic': None
	}, 
	'Developers': ['Otomate', 'Design Factory Co., Ltd.'], 
	'Releases': {
		'English': [{'ID': 'r30158',
					 'Platform': 'PlayStation 3', 
					 'Ages': '17+', 'Date': '2014-05-06', 
					 'Name': 'Hakuoki: Stories of the Shinsengumi - Standard Edition'
					 }], 
		'Japanese': [{'ID': 'r3515', 
			          'Platform': 'PlayStation 2', 
			          'Ages': '12+', 
			          'Date': '2009-08-27', 
			          'Name': 'Hakuoki Zuisouroku - Limited Edition'}]
	}
}
```