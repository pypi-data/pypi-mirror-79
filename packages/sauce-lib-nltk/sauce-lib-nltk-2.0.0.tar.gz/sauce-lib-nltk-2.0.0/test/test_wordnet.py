import unittest
import json
from rdflib import Graph, plugin
from rdflib.parser import Parser
from rdflib.serializer import Serializer
from sauce.nltkrdf.wordnet import WordnetEnricher

class WordnetEnricherTestCase(unittest.TestCase):

    def setUp(self):
    	self.enricher = WordnetEnricher("""[{"@id":"https://api.sauce-project.tech/assets/1234","@type":["https://vocabularies.sauce-project.tech/core/Asset"],"https://vocabularies.sauce-project.tech/core/depicts":[{"@id":"https://api.sauce-project.tech/depictions/1234"}]},{"@id":"https://api.sauce-project.tech/depictions/1234","@type":["https://vocabularies.sauce-project.tech/core/Depiction"],"https://vocabularies.sauce-project.tech/core/label":[{"@value":"running"}]},{"@id":"https://vocabularies.sauce-project.tech/core/Asset"},{"@id":"https://vocabularies.sauce-project.tech/core/Depiction"}]""")

    def test_lemmas(self):
    	assert len(self.enricher.extract_lemmas('running')) > 0

    def test_synonyms(self):
    	assert len(self.enricher.extract_synonyms('running')) > 0

    def test_enrichment(self):
    	json_res = json.loads(self.enricher.enrich())
    	res = Graph().parse(data=json.dumps(json_res), format='json-ld')
    	assert len(res.query("SELECT ?dep ?label WHERE { ?dep core:label ?label }", initNs=WordnetEnricher.query_ns)) > 1
    	assert len(res.query("SELECT ?dep ?label WHERE { ?dep core:synonym ?label }", initNs=WordnetEnricher.query_ns)) > 1

    def test_wordnet_id(self):
        wnid = "https://vocabularies.sauce-project.tech/wordnet/n02119789"
        assert self.enricher.extract_synset_type_from_id(wnid) == "n"
        assert self.enricher.extract_synset_offset_from_id(wnid) == 2119789
        assert len(self.enricher.extract_lemmas_from_wnid('n', 4543158))