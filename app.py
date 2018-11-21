import json
from flask import Flask, request
from flask_restful import Resource, Api
import process_documents
import tagger
import datetime

'''
This file handles API requests to and from the components of Ancillus.
'''

app = Flask(__name__)
api = Api(app)


class AncillusAPI(Resource):
    def get(self):
        return {'Intelligence.AI': 'Tagger is active.'}

    def post(self):
        from_electron = request.get_json()
        time_stamp = str(datetime.datetime.utcnow())
        if 'schema' in json.loads(json.dumps(from_electron)):
            string = json.loads(json.dumps(from_electron))['schema']
            processed = process_documents.sentence_structure(string)
            return {time_stamp: processed}, 201
        elif 'tags' in json.loads(json.dumps(from_electron)):
            string = json.loads(json.dumps(from_electron))['tags']
            processed = tagger.Tagger(string).process()
            return {time_stamp: processed},
        elif 'graph' in json.loads(json.dumps(from_electron)):
            string = json.loads(json.dumps(from_electron))['graph']
            processed = tagger.Tagger(string).process()
            return {time_stamp: processed}, 201
        else:
            return {time_stamp: 'NO DATA'}, 401


api.add_resource(AncillusAPI, '/')

if __name__ == '__main__':
    app.run('0.0.0.0')
