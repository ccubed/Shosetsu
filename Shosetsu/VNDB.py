import aiohttp
import asyncio
from bs4 import BeautifulSoup
from bs4 import NavigableString
from .errors import *
from .Parsing import *

class Shosetsu:
    def __init__(self, loop=None):
        self.session = aiohttp.ClientSession()
        self.base_url = "https://vndb.org"
        self.headers = {"User-Agent": "Shosetsu 1.0 / Aiohttp / Python 3"}
        self.stypes = {'v': 'Visual Novels', 'r': 'Releases', 'p': 'Producers',
                       's': 'Staff', 'c': 'Characters', 'g': 'Tags',
                       'i': 'Traits', 'u': 'Users'}

    async def search_vndb(self, stype, term):
        """
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
        """
        fstype = ""
        if stype not in ['v', 'r', 'p', 's', 'c', 'g', 'i', 'u']:
            raise VNDBBadStype(stype)
        else:
            if stype in ['v', 'p', 's', 'c', 'u']:
                fstype = '/{}/all'.format(stype)
            elif stype in ['g', 'i']:
                fstype = '/{}/list'.format(stype)
            elif stype == 'r':
                fstype = '/r'
        async with self.session.get(self.base_url + "{}".format(fstype), params={"q": term}, headers=self.headers) as response:
            if response.status == 404:
                raise aiohttp.HttpBadRequest("VN Not Found")
            elif 'q=' not in response.url:
                raise VNDBOneResult(term, response.url.rsplit('/', 1)[1])
            text = await response.text()
            if 'No Results' in text:
                raise VNDBNoResults(term)
            soup = BeautifulSoup(text, 'lxml')
            resp = await self.parse_search(stype, soup)
            if resp == []:
                raise VNDBNoResults(term)
            return resp

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
        'Desription' - Contains novel description text if there is any.

        :param term: id or name to get details of.
        :return dict: Dictionary with the parsed results of a novel
        """
        if not term.isdigit() and not term.startswith('v'):
            vnid = await self.search_vndb('v', term)
            vnid = vnid[0]['id']
        else:
            vnid = str(term)
            if not vnid.startswith('v'):
                vnid = 'v' + vnid
        async with self.session.get(self.base_url + "/{}".format(vnid), headers=self.headers) as response:
            if response.status == 404:
                raise aiohttp.HttpBadRequest("VNDB reported that there is no data for ID {}".format(vnid))
            text = await response.text()
            soup = BeautifulSoup(text, 'lxml')
            data = {'titles': {}, 'img': None, 'length': None, 'developers': [], 'publishers': [], 'tags': {}, 'releases': {}, 'id': vnid}
            data['titles']['english'] = soup.find_all('div', class_='mainbox')[0].h1.string
            data['titles']['alt'] = soup.find_all('h2', class_='alttitle')[0].string
            data['img'] = 'https:' + soup.find_all('div', class_='vnimg')[0].img.get('src')
            for item in soup.find_all('tr'):
                if 'class' in item.attrs or len(list(item.children)) == 1:
                    continue
                if item.td.string == 'Aliases':
                    tlist = []
                    for alias in list(item.children)[1:]:
                        tlist.append(alias.string)
                    data['titles']['aliases'] = tlist
                elif item.td.string == 'Length':
                    data['length'] = list(item.children)[1].string
                elif item.td.string == 'Developer':
                    tl = []
                    for item in list(list(item.children)[1].children):
                        if isinstance(item, NavigableString):
                            continue
                        if 'href' in item.attrs:
                            tl.append(item.string)
                    data['developers'] = tl
                    del tl
                elif item.td.string == 'Publishers':
                    tl = []
                    for item in list(list(item.children)[1].children):
                        if isinstance(item, NavigableString):
                            continue
                        if 'href' in item.attrs:
                            tl.append(item.string)
                    data['publishers'] = tl
            conttags = []
            techtags = []
            erotags = []
            test = soup.find('div', attrs={'id': 'vntags'})
            if test:
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
            data['tags']['content'] = conttags if len(conttags) else None
            data['tags']['technology'] = techtags if len(techtags) else None
            data['tags']['erotic'] = erotags if len(erotags) else None
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
                        data['releases'][cur_lang] = releases
                        releases = []
                        cur_lang = item.td.abbr.get('title')
                else:
                    temp_rel = {'date': 0, 'ages': 0, 'platform': 0, 'name': 0, 'id': 0}
                    children = list(item.children)
                    temp_rel['date'] = children[0].string
                    temp_rel['ages'] = children[1].string
                    temp_rel['platform'] = children[2].abbr.get('title')
                    temp_rel['name'] = children[3].a.string
                    temp_rel['id'] = children[3].a.get('href')[1:]
                    del children
                    releases.append(temp_rel)
                    del temp_rel
            if len(releases) > 0 and cur_lang is not None:
                data['releases'][cur_lang] = releases
            del releases
            del cur_lang
            desc = ""
            for item in list(soup.find_all('td', class_='vndesc')[0].children)[1].contents:
                if not isinstance(item, NavigableString):
                    continue
                if item.startswith('['):
                    continue
                desc += item.string + "\n"
            data['description'] = desc
            return data

    async def parse_search(self, stype, soup):
        """
        This is our parsing dispatcher

        :param stype: Search type category
        :param soup: The beautifulsoup object that contains the parsed html
        """
        if stype == 'v':
            return await parse_vn_results(soup)
        elif stype == 'r':
            return await parse_release_results(soup)
        elif stype == 'p':
            return await parse_prod_staff_results(soup)
        elif stype == 's':
            return await parse_prod_staff_results(soup)
        elif stype == 'c':
            return await parse_character_results(soup)
        elif stype == 'g':
            return await parse_tag_results(soup)
        elif stype == 'i':
            return await parse_tag_results(soup)
        elif stype == 'u':
            return await parse_user_results(soup)
