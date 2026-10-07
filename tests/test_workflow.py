import json,pathlib,unittest
class T(unittest.TestCase):
 def test_graph(self):
  d=json.loads((pathlib.Path(__file__).parents[1]/'workflows/chat-and-image.json').read_text());self.assertEqual(d['active'],False)
if __name__=='__main__':unittest.main()
