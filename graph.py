#! /bin/python3

from py2neo import Graph, Node, Relationship
import warnings
warnings.filterwarnings('ignore')

try:
    graph = Graph("bolt://localhost:7687", auth=('neo4j', 'basic'))
except:
    print('WARNING: Neo4J is not running!')


class TagsToGraph(object):

    def __init__(self, output_from_Tagger):
        self.output = output_from_Tagger
        self.create_organization()
        self.okr_2graph()
        # self.hardcoded() DISABLED HARDCODING

    def create_organization(self):
        self.org = Node('Organization',
                        Name='Ancillus Project',
                        Definition='https://ancillus.com')
        graph.merge(self.org, 'Organization', 'Name')

    def okr_2graph(self):
        root = self.output['OKR']
        okr_node = Node('OKR',
                        Objective=str(root['Objective']),
                        Results=str(root['Results']),
                        UUID='OKR ID: {}'.format(str(root['UUID'])))
        okr_library = Node('OKR_Library',
                           Name='OKR_Libary')
        graph.merge(okr_library, 'OKR_Library', 'Name')
        graph.merge(okr_node, 'OKR', 'Objective')
        graph.merge(Relationship(okr_node, 'ADDED_TO', okr_library))
        graph.merge(Relationship(okr_library, 'ASSOCIATED_WITH', self.org))
