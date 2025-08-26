import unittest
from compress_string import compress

class TestCompress(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(compress("aabccccdd"), "2a1b4c2d")
        self.assertEqual(compress("abc"), "1a1b1c")
        self.assertEqual(compress(""), "")
        self.assertEqual(compress("aaaa"), "4a")
        self.assertEqual(compress("aabb"), "2a2b")
        self.assertEqual(compress("a"), "1a")
        self.assertEqual(compress("abbbcc"), "1a3b2c")
    def test_single_char(self):
        self.assertEqual(compress("z"), "1z")
    def test_no_repeats(self):
        self.assertEqual(compress("xyz"), "1x1y1z")
    def test_long_repeat(self):
        self.assertEqual(compress("bbbbbbbb"), "8b")

if __name__ == "__main__":
    unittest.main()
