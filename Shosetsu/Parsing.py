from bs4 import NavigableString

async def parse_vn_results(soup):
    """
    Parse Visual Novel search pages.

    :param soup: The BS4 class object
    :return:  A list of dictionaries containing a name and id.
    """
    soup = soup.find_all('td', class_='tc1')
    vns = []
    for item in soup[1:]:
        vns.append({'name': item.string, 'id': item.a.get('href')[1:]})
    return vns

async def parse_release_results(soup):
    """
    Parse Releases search pages.

    :param soup: The BS4 class object
    :return: A list of dictionaries containing a release dictionary. This is the same as the one returned in get_novel.
             It contains a Date released, Platform, Ages group and Name.
    """
    soup = list(soup.find_all('table', class_='stripe')[0].children)[1:]
    releases = []
    for item in soup:
        child = list(item.children)
        temp_rel = {'date': None, 'ages': None, 'platform': None, 'name': None}
        temp_rel['date'] = child[0].string
        temp_rel['ages'] = child[1].string
        temp_rel['platform'] = child[2].abbr.get('title')
        temp_rel['name'] = child[3].a.string
        releases.append(temp_rel)
        del temp_rel
    return releases

async def parse_prod_staff_results(soup):
    """
    Parse a page of producer or staff results

    :param soup: The BS4 class object
    :return: A list of dictionaries containing a name and nationality.
    """
    soup = soup.find_all('li')
    producers = []
    for item in soup:
        producers.append({'nationality': item.abbr.get('title'), 'name': item.a.string})
    return producers

async def parse_character_results(soup):
    """
    Parse a page of character results.

    :param soup: The BS4 class object
    :return: Returns a list of dictionaries containing a name, gender and list of dictionaries containing a game name/id pair
             for games they appeared in.
    """
    soup = list(soup.find_all('table', class_='stripe')[0].children)[1:]
    characters = []
    for item in soup:
        temp_c = {'gender': None, 'name': None, 'games': {}}
        temp_c['gender'] = item.abbr.get('title')
        temp_c['name'] = list(item.children)[1].a.string
        temp_c['games'] = []
        for game in list(list(list(item.children)[1].children)[1].children):
            if isinstance(game, NavigableString):
                continue
            temp_c['games'].append({'name': game.string, 'id': game.get('href').split('/')[1]})
        characters.append(temp_c)
        del temp_c
    return characters

async def parse_tag_results(soup):
    """
    Parse a page of tag or trait results. Same format.

    :param soup: BS4 Class Object
    :return: A list of tags, Nothing else really useful there
    """
    soup = soup.find_all('td', class_='tc3')
    tags = []
    for item in soup:
        tags.append(item.a.string)
    return tags

async def parse_user_results(soup):
    """
    Parse a page of user results

    :param soup: Bs4 Class object
    :return: A list of dictionaries containing a name and join date
    """
    soup = list(soup.find_all('table', class_='stripe')[0].children)[1:]
    users = []
    for item in soup:
        t_u = {'name': None, 'joined': None}
        t_u['name'] = list(item.children)[0].a.string
        t_u['joined'] = list(item.children)[1].string
        users.append(t_u)
        del t_u
    return users
