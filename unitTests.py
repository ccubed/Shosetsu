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
    def test_search_vns(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('v', 'haruka'))
        self.assertEqual(len(data), 50)
        self.assertEqual(data[0]['id'], 'v251')
        self.assertIsInstance(random.choice(data)['name'], str)
        self.assertIsInstance(random.choice(data), dict)
        self.assertIsInstance(data, list)
        del data

    def test_search_producers(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('p', 'haruka'))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['nationality'], 'English')
        self.assertIsInstance(random.choice(data)['name'], str)
        self.assertIsInstance(random.choice(data), dict)
        self.assertIsInstance(data, list)
        del data

    def test_search_releases(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('r', 'haruka'))
        self.assertEqual(len(data), 50)
        self.assertEqual(data[0]['platform'], 'Windows')
        self.assertIsInstance(random.choice(data)['ages'], str)
        self.assertIsInstance(random.choice(data), dict)
        self.assertIsInstance(data, list)
        del data

    def test_search_staff(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('s', 'haruka'))
        self.assertEqual(len(data), 54)
        self.assertEqual(data[0]['name'], 'Chisuga Haruka')
        self.assertIsInstance(random.choice(data)['nationality'], str)
        self.assertIsInstance(random.choice(data), dict)
        self.assertIsInstance(data, list)
        del data

    def test_search_characters(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('c', 'haruka'))
        self.assertEqual(len(data), 50)
        self.assertEqual(data[0]['name'], 'Abeno Haruka')
        self.assertIsInstance(random.choice(data)['gender'], str)
        self.assertIsInstance(random.choice(data), dict)
        self.assertIsInstance(random.choice(data)['games'], list)
        self.assertIsInstance(data, list)
        del data

    def test_search_tags(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('g', 'edo'))
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], 'Edo Era')
        self.assertIsInstance(random.choice(data), str)
        self.assertIsInstance(data, list)
        del data

    def test_search_traits(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('i', 'edo'))
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0], 'Fedora')
        self.assertIsInstance(random.choice(data), str)
        self.assertIsInstance(data, list)
        del data

    def test_search_users(self):
        data = self.loop.run_until_complete(self.setsu.search_vndb('u', 'haruka'))
        self.assertEqual(len(data), 28)
        self.assertEqual(data[0]['name'], '8haruka123')
        self.assertIsInstance(random.choice(data)['joined'], str)
        self.assertIsInstance(random.choice(data), dict)
        self.assertIsInstance(data, list)
        del data

    #  Verify Error messages are working and returning proper data for handling
    def test_invoke_VNDBBadStype(self):
        with self.assertRaises(errors.VNDBBadStype) as e:
            self.loop.run_until_complete(self.setsu.search_vndb('x', 'haruka'))
            self.assertEqual(e.expression, 'x')
            self.assertEqual(str(e), "x is not a valid search type.")

    def test_invoke_VNDBOneResult(self):
        with self.assertRaises(errors.VNDBOneResult) as e:
            self.loop.run_until_complete(self.setsu.search_vndb('v', 'go go nippon my first trip to japan'))
            self.assertEqual(e.vnid, 'v7316')
            self.assertEqual(str(e), "Search go go nippon my first trip to japan only had one result at ID v7316.")

    def test_invoke_VNDBNoResults(self):
        with self.assertRaises(errors.VNDBNoResults) as e:
            self.loop.run_until_complete(self.setsu.search_vndb('g', 'haruka'))
            self.assertEqual(e.expression, 'haruka')
            self.assertEqual(str(e), "Search haruka has no results.")

    #  Test Get Novel
    def test_get_novel_sfw(self):
        data = self.loop.run_until_complete(self.setsu.get_novel('go go nippon my first trip to japan'))
        self.assertEqual(len(data['titles']['aliases']), 1)
        self.assertEqual(data['titles']['english'], 'Go! Go! Nippon! ~My First Trip to Japan~')
        self.assertEqual(len(data['tags']['content']), 15)
        self.assertEqual(len(data['tags']['technology']), 10)
        self.assertIsNone(data['tags']['erotic'])
        self.assertEqual(len(data['developers']), 1)
        self.assertIsInstance(data['publishers'], list)
        self.assertIsInstance(data, dict)
        del data

    def test_get_novel_nsfw_hide(self):
        data = self.loop.run_until_complete(self.setsu.get_novel('v19018', True))
        self.assertIsInstance(data, dict)
        self.assertIsNone(data['img'])
        del data

    def test_get_novel_nsfw_visible(self):
        data = self.loop.run_until_complete(self.setsu.get_novel('v19018', False))
        self.assertIsInstance(data, dict)
        self.assertIsNotNone(data['img'])
        self.assertIsInstance(data['img'], str)
        del data

    @classmethod
    def tearDownClass(cls):
        cls.__dict__['setsu'].session.close()
        loop = asyncio.get_event_loop()
        loop.close()
