#! /bin/python3

import en_core_web_lg
import json
import datetime
import warnings
import re
warnings.filterwarnings('ignore')

nlp = en_core_web_lg.load()

for word in nlp.Defaults.stop_words:
    lex = nlp.vocab[word]
    lex.is_stop = True


def match_acronyms(doc):
    acronyms = {}
    chunks = []
    matches = {}
    for word in doc:
        if word.is_upper is True:
            acronyms[str(word)] = word.text.lower()
    for chunk in doc.noun_chunks:
        text = chunk.text.lower()
        text = re.sub('[^A-Za-z0-9 -]+', '', text)
        words = text.split()
        chunks.append((text, ''.join([word[0] for word in words])))
    for _, j in acronyms.items():
        for k, l in chunks:
            if j in l:
                matches[j.upper()] = k
    return matches


def node_objects(doc):
    '''
    Extracts nouns and named entities from the passed portion of text.
    Partly dynamic, and partly rules based.
    '''
    entities = {}
    nouns = {}
    contexts = {}
    temp = set()
    restricted = {'PRON', 'We', 'we', 'I', 'He', 'he',
                  'She', 'she', 'You', 'you', 'They', 'they'}
    # keep this updated to improve extraction accuracy, POSSIBLE TRAINING POINT
    watch = {'NOUN', 'PROPN'}
    for ent in doc.ents:
        entities['@i.entity.{}'.format(ent.text)] = {}
        temp.add(ent.text)
    for word in doc:
        if word.like_url:
            word.tag_, word.dep_ = 'URL', 'URL'
            entities['@i.url.{}'.format(word.text)] = {}
        elif word.like_email:
            word.tag_, word.dep_ = 'EMAIL', 'EMAIL'
            entities['@i.email.{}'.format(word.text)] = {}
        elif word.pos_ in watch and word.pos_ not in restricted:
            nouns['@i.entity.{}'.format(word.text)] = {}
            temp.add(word.text)
    entities.update(nouns)
    for chunk in doc.noun_chunks:
        for entity in temp:
            if str(entity) in chunk.text and chunk.text not in restricted:
                text = chunk.text
                text = re.sub('[^A-Za-z0-9 -]+', '', text)
                contexts['@i.entity.{}'.format(entity)] = {}
                if len(text.split()) > 2:
                    contexts['@i.entity.{}'.format(entity)].update(
                        {'@i.entity.{}.context'.format(entity): [text]})
    matches = match_acronyms(doc)
    for key, value in matches.items():
        try:
            contexts['@i.entity.{}'.format(
                key)]['@i.entity.{}.context'.format(key)].append(value)
        except:
            contexts['@i.entity.{}'.format(key)]['@i.entity.{}.context'.format(key)] = [
                value]
    entities.update(contexts)
    return entities


def sentence_structure(doc):
    '''
    Uses extract_nodes() to populate each sentence in the doc
    with its respective nodes and returns a json.
    '''
    doc = nlp(doc)
    document = {}
    output = {}
    sent_id = 1
    id_ = datetime.datetime.now()  # use the graph database to track a unique number
    document = output['schema_object'] = {}
    identification = document['@i.document'] = {}
    identification['id'] = str(id_)
    identification['url'] = 'http://0.0.0.0:5000'
    doc_text = doc.text
    doc_text = re.sub("'", "’", doc_text)
    identification['text'] = doc_text
    sentences = document['@i.knowledge.snippets'] = {}
    for sent in doc.sents:
        entities = node_objects(sent)
        data = sentences['@i.snippet.id.{}'.format(sent_id)] = {}
        data['text'] = sent.text
        data['@i.entities'] = entities
        sent_id += 1

    return json.loads(json.dumps(output, ensure_ascii=False))
