import unittest
import asyncio
import random
from Shosetsu import Shosetsu, errors

class ShosetsuTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()
        cls.setsu = Shosetsu()

    #  Search for proper responses from parsers
    def search_vns(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('v', 'haruka'))
        self.assertEqual(len(data), 50)
        self.assertEqual(data[0]['id'], 'v251')
        self.assertIs(random.choice(data)['name'], str)
        self.assertIs(random.choice(data), dict)
        self.assertIs(data, list)
        del data

    def search_producers(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('p', 'haruka'))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['nationality'], 'English')
        self.assertIs(random.choice(data)['name'], str)
        self.assertIs(random.choice(data), dict)
        self.assertIs(data, list)
        del data

    def search_releases(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('r', 'haruka'))
        self.assertEqual(len(data), 50)
        self.assertEqual(data[0]['platform'], 'Windows')
        self.assertIs(random.choice(data)['ages'], str)
        self.assertIs(random.choice(data), dict)
        self.assertIs(data, list)
        del data

    def search_staff(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('s', 'haruka'))
        self.assertEqual(len(data), 54)
        self.assertEqual(data[0]['name'], 'Chisuga Haruka')
        self.assertIs(random.choice(data)['nationality'], str)
        self.assertIs(random.choice(data), dict)
        self.assertIs(data, list)
        del data

    def search_characters(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('c', 'haruka'))
        self.assertEqual(len(data), 50)
        self.assertEqual(data[0]['name'], 'Abeno Haruka')
        self.assertIs(random.choice(data)['gender'], str)
        self.assertIs(random.choice(data), dict)
        self.assertIs(random.choice(data)['games'], dict)
        self.assertIs(data, list)
        del data

    def search_tags(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('g', 'edo'))
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], 'Edo Era')
        self.assertIs(random.choice(data), str)
        self.assertIs(data, list)
        del data

    def search_traits(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('i', 'edo'))
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0], 'Fedora')
        self.assertIs(random.choice(data), str)
        self.assertIs(data, list)
        del data

    def search_users(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('u', 'haruka'))
        self.assertEqual(len(data), 28)
        self.assertEqual(data[0]['name'], '8haruka123')
        self.assertIs(random.choice(data)['joined'], str)
        self.assertIs(random.choice(data), dict)
        self.assertIs(data, list)
        del data

    #  Verify Error messages are working and returning proper data for handling
    def invoke_VNDBBadStype(self):
        with self.assertRaises(errors.VNDBBadStype) as e:
            self.loop.run_until_complete(self.setsu.search_vndb('x', 'haruka'))
            self.assertEqual(e.expression, 'x')
            self.assertEqual(str(e), "x is not a valid search type.")

    def invoke_VNDBOneResult(self):
        with self.assertRaises(errors.VNDBOneResult) as e:
            self.loop.run_until_complete(self.setsu.search_vndb('v', 'go go nippon my first trip to japan'))
            self.assertEqual(e.vnid, 'v7316')
            self.assertEqual(str(e), "Search go go nippon my first trip to japan only had one result at ID v7316.")

    def invoke_VNDBNoResults(self):
        with self.assertRaises(errors.VNDBNoResults) as e:
            self.loop.run_until_complete(self.setsu.search_vndb('g', 'haruka'))
            self.assertEqual(e.expression, 'haruka')
            self.assertEqual(str(e), "Search haruka has no results.")

    #  Test Get Novel
    def get_novel_sfw(self):
        data = self.loop.run_until_complete(self.setsu.get_novel('go go nippon my first trip to japan'))
        self.assertEqual(len(data['titles']['aliases']), 3)
        self.assertEqual(data['titles']['english'], 'Go! Go! Nippon! ~My First Trip to Japan~')
        self.assertEqual(len(data['tags']['content']), 15)
        self.assertEqual(len(data['tags']['technology']), 10)
        self.assertIsNone(data['tags']['erotic'])
        self.assertEqual(len(data['developers']), 1)
        self.assertIs(data['publishers'], list)
        self.assertIs(data, dict)
        del data

    def get_novel_nsfw_hide(self):
        data = self.loop.run_until_complete(self.setsu.get_novel('v19018', True))
        self.assertIs(data, dict)
        self.assertIsNone(data['img'])
        del data

    def get_novel_nsfw_visible(self):
        data = self.loop.run_until_complete(self.setsu.get_novel('v19018', True))
        self.assertIs(data, dict)
        self.assertIsNotNone(data['img'])
        self.assertIs(data['img'], str)
        del data

    @classmethod
    def tearDownClass(cls):
        cls.loop.stop()