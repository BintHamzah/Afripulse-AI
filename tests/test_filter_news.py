
import unittest
from filterNews import filter_africa_stories

class TestFilterNews(unittest.TestCase):

    def test_filter_africa_stories(self):
        articles = [
            {
                "title": "Nigerian startup raises $5M in funding",
                "description": "A fintech company in Lagos, Nigeria, has secured seed funding.",
                "source": {"name": "TechCrunch"}
            },
            {
                "title": "European tech giant expands to Asia",
                "description": "A large software company is opening new offices in Singapore.",
                "source": {"name": "Reuters"}
            },
            {
                "title": "Venture capital investment in African agritech",
                "description": "A new report shows a surge in VC funding for agritech startups in Kenya and Ghana.",
                "source": {"name": "Bloomberg"}
            },
            {
                "title": "The latest in AI research",
                "description": "A new paper on large language models has been published.",
                "source": {"name": "Nature"}
            }
        ]

        filtered = filter_africa_stories(articles)
        
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]["title"], "Nigerian startup raises $5M in funding")
        self.assertEqual(filtered[1]["title"], "Venture capital investment in African agritech")

if __name__ == '__main__':
    unittest.main()
