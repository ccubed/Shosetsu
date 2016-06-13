import aiohttp
import asyncio
from bs4 import BeautifulSoup
from bs4 import NavigableString
import atexit

class Shosetsu:
    def __init__(self, loop=None):
        self.session = aiohttp.ClientSession()
        self.base_url = "https://vndb.org"
        self.headers = {"User-Agent": "Shosetsu 1.0 / Aiohttp / Python 3"}
        self.loop = loop if loop is not None else asyncio.get_event_loop()  #  Needed to close down, otherwise await passes it implicitly
        atexit.register(self.cleanup)

    async def search_visual_novels(self, term):
        """
        Search vndb.org for a term and return matching Visual Novels.

        :param term: string to search for
        :return: List of Dictionaries. Dictionaries contain a name and id.
        """
        async with self.session.get(self.base_url + "/v/all", params={"sq":term}, headers=self.headers) as response:
            if response.status == 404:
                raise aiohttp.HttpBadRequest("VN Not Found")
            text = await response.text()
            soup = BeautifulSoup(text, 'lxml')
            soup = soup.find_all('td', class_='tc1')
            vns = []
            for item in soup[1:]:
                vns.append({'name': item.string, 'id': item.a.get('href')[1:]})
            return vns

    async def get_novel(self, term):
        """
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
        """
        if not term.isdigit():
            vnid = await self.search_visual_novels(term)
            vnid = id[0]['id']
        else:
            vnid = 'v' + str(term)
        async with self.session.get(self.base_url + "/{}".format(vnid), headers=self.headers) as response:
            if response.status == 404:
                raise aiohttp.HttpBadRequest("VNDB reported that there is no data for ID {}".format(vnid))
            text = await response.text()
            soup = BeautifulSoup(text, 'lxml')
            data = {'Titles': {}, 'Img': None, 'Length': None, 'Developers': [], 'Publishers': [], 'Tags': {}, 'Releases': {}}
            data['Titles']['English'] = soup.find_all('div', class_='mainbox')[0].h1.string
            data['Titles']['Alt'] = soup.find_all('h2', class_='alttitle')[0].string
            data['Img'] = 'https:' + soup.find_all('div', class_='vnimg')[0].img.get('src')
            for item in soup.find_all('tr'):
                if 'class' in item.attrs or len(list(item.children)) == 1:
                    continue
                if item.td.string == 'Aliases':
                    tlist = []
                    for alias in list(item.children)[1:]:
                        tlist.append(alias.string)
                    data['Titles']['Aliases'] = tlist
                elif item.td.string == 'Length':
                    data['Length'] = list(item.children)[1].string
                elif item.td.string == 'Developer':
                    tl = []
                    for item in list(list(item.children)[1].children):
                        if isinstance(item, NavigableString):
                            continue
                        if 'href' in item.attrs:
                            tl.append(item.string)
                    data['Developers'] = tl
                    del tl
                elif item.td.string == 'Publishers':
                    tl = []
                    for item in list(list(item.children)[1].children):
                        if isinstance(item, NavigableString):
                            continue
                        if 'href' in item.attrs:
                            tl.append(item.string)
                    data['Publishers'] = tl
            conttags = []
            techtags = []
            erotags = []
            test = soup.find('div', attrs={'id': 'vntags'})
            for item in list(test.children):
                if isinstance(item, NavigableString):
                    continue
                if 'class' not in item.attrs:
                    continue
                if 'cont' in " ".join(item.get('class')):
                    conttags.append(item.a.string)
                if 'tech' in " ".join(item.get('class')):
                    techtags.append(item.a.string)
                if 'ero' in " ".join(item.get('class')):
                    erotags.append(item.a.string)
            data['Tags']['Content'] = conttags if len(conttags) else None
            data['Tags']['Technology'] = techtags if len(techtags) else None
            data['Tags']['Erotic'] = erotags if len(erotags) else None
            del conttags
            del techtags
            del erotags
            releases = []
            cur_lang = None
            for item in list(soup.find('div', class_='mainbox releases').table.children):
                if isinstance(item, NavigableString):
                    continue
                if 'class' in item.attrs:
                    if cur_lang is None:
                        cur_lang = item.td.abbr.get('title')
                    else:
                        data['Releases'][cur_lang] = releases
                        releases = []
                        cur_lang = item.td.abbr.get('title')
                else:
                    temp_rel = {'Date': 0, 'Ages': 0, 'Platform': 0, 'Name': 0, 'ID': 0}
                    children = list(item.children)
                    temp_rel['Date'] = children[0].string
                    temp_rel['Ages'] = children[1].string
                    temp_rel['Platform'] = children[2].abbr.get('title')
                    temp_rel['Name'] = children[3].a.string
                    temp_rel['ID'] = children[3].a.get('href')[1:]
                    del children
                    releases.append(temp_rel)
                    del temp_rel
            if len(releases) > 0 and cur_lang is not None:
                data['Releases'][cur_lang] = releases
            del releases
            del cur_lang
            return data

    def cleanup(self):
        self.loop.run_until_complete(self.session.close())
