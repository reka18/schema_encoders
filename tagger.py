#! /bin/python3

import en_core_web_lg
import json
import wikipedia
import datetime
import warnings
warnings.filterwarnings('ignore')

nlp = en_core_web_lg.load()


class Tagger(object):

    def __init__(self, string):
        self.string_ = string
        self.okr = nlp(string)
        self.special_words = ['Grephy', 'grephy',
                              'OKR', 'okr', 'user', 'User', 'API']
        self.now = str(datetime.datetime.now())

    def process(self):
        self.nodes = {}
        self.edges = {}
        self.properties = {}
        self.output = {}

        # nodes based on nouns
        for word in self.okr:
            if word.like_url:
                word.tag_, word.dep_ = 'URL', 'URL'
                self.nodes[str(word)] = 'URL'
            elif word.dep_ == 'dobj' or word.dep_ == 'compound' or word.dep_ == 'pobj' or word.dep_ == 'nsubj':
                self.nodes[str(word)] = 'THING'

        # nodes updated to reflect named entities
        named_entities = {}
        for ent in self.okr.ents:
            if ent.text is False:
                named_entities[str(ent)] = (str(ent.label_))

        # custom filter to make sure named_entities doesn't overwrite important preset labels.
        for word in named_entities:
            if self.nodes[word] == 'URL':
                named_entities[word] = 'URL'

        # combines the named entity nodes with the noun self.nodes
        self.nodes.update(named_entities)

        # combines the events found by the entity extractor
        try:
            self.nodes.update(self.entity_extractor())
        except:
            pass

        # hardcoded meanings
        if 'Grephy' in self.nodes:
            self.nodes['Grephy'] = 'PRODUCT'
        if 'grephy' in self.nodes:
            self.nodes['grephy'] = 'PRODUCT'
        if 'OKR' in self.nodes:
            self.nodes['OKR'] = 'OBJECTIVE'
        if 'okr' in self.nodes:
            self.nodes['okr'] = 'OBJECTIVE'
        if 'user' in self.nodes:
            self.nodes['user'] = 'PERSON'
        if 'User' in self.nodes:
            self.nodes['User'] = 'PERSON'
        if 'API' in self.nodes:
            self.nodes['API'] = 'SOFTWARE'

        # Edges for graph, establishes relationships
        for word in self.okr:
            if word.tag_ == 'VBZ' or word.dep_ == 'conj' or word.dep_ == 'ROOT':
                self.edges[str(word.lemma_)] = ('ACTION')

        self.properties.update(self.nodes)
        self.properties.update(self.edges)
        self.properties.update(self.recommended_actions())
        # self.properties.update(self.suggested_links())
        self.output.update(self.okr_id())
        return self.output

    def okr_id(self):
        okr = {
            'tags': {
                'Objective': str(self.okr),
                'Results': {},
                'UUID': self.now,
                'Properties': self.properties
            }
        }
        return json.loads(json.dumps(okr))

    # Suggestion generator DISABLED ABOVE
    def entity_extractor(self):
        entities = []
        for word in range(len(self.okr)):
            if str(self.okr[word]) not in self.special_words:
                if self.okr[word].dep_ == 'pobj' and self.okr[word].pos_ != 'NUM':
                    entities.insert(0, [str(self.okr[word])])
                    if self.okr[word - 1].dep_ == 'compound' or self.okr[word - 1].dep_ == 'nummod' or self.okr[word - 1].dep_ == 'prep':
                        entities[0].insert(0, str(self.okr[word - 1]))
                        if self.okr[word - 2].dep_ == 'compound' or self.okr[word - 2].dep_ == 'nummod' or self.okr[word - 2].dep_ == 'pobj':
                            entities[0].insert(0, str(self.okr[word - 2]))
                            if self.okr[word - 3].dep_ == 'compound' or self.okr[word - 3].dep_ == 'nummod':
                                entities[0].insert(0, str(self.okr[word - 3]))
                    try:
                        for i in range(5):
                            if self.okr[word + i].pos_ == 'NUM' and self.okr[word + i].dep_ == 'pobj':
                                entities[0].insert(0, str(self.okr[word + i]))
                    except:
                        continue

                if self.okr[word].dep_ == 'pcomp':
                    entities[0].insert(0, str(self.okr[word]))

        for i in range(len(entities)):
            entities[i] = ' '.join(entities[i])

        nodes = {}
        for i in entities:
            if i in self.nodes:
                return
            else:
                nodes[i] = 'SUGGESTION'

        list_ = []
        for i in entities:
            list_.append(i)
        list_ = ' '.join(list_)
        nodes[list_] = 'SUGGESTION'

        return json.loads(json.dumps(nodes))

    def recommended_actions(self):
        verb_to_noun = {
            'predict': 'prediction',
            'plan': 'plan',
            'decide': 'decision'
        }
        verbs = {'build', 'organize', 'develop'}
        recs = {}
        for action in self.edges:
            if action.lower() in verb_to_noun:
                word = verb_to_noun[action.lower()]
                recs['question_for_user'] = 'Do you want to make a {}?'.format(
                    word)
            elif action.lower() in verbs:
                recs['question_for_user'] = 'Do you want to {} something?'.format(
                    action.lower())
        return json.loads(json.dumps(recs))

    def suggested_links(self):
        links = {}
        for i, node in enumerate(self.nodes):
            if self.nodes[node] != 'URL':
                try:
                    links['link_{}'.format(i)] = wikipedia.page(node).url
                except:
                    pass
        return json.loads(json.dumps(links))


# string = "Generative adversarial networks (GANs) are an expressive class of neural generative models with tremendous success in modeling high-dimensional continuous measures. In this paper, we present a scalable method for unbalanced optimal transport (OT) based on the generative-adversarial framework. We formulate unbalanced OT as a problem of simultaneously learning a transport map and a scaling factor that push a source measure to a target measure in a cost-optimal manner. In addition, we propose an algorithm for solving this problem based on stochastic alternating gradient updates, similar in practice to GANs. We also provide theoretical justification for this formulation, showing that it is closely related to an existing static formulation by Liero et al. (2018), and perform numerical experiments demonstrating how this methodology can be applied to population modeling."
# print(Tagger(string).process())
