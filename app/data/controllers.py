from flask import Blueprint, jsonify, request
from flask import current_app as app

import logging


data = Blueprint('data', __name__)


@data.route('/')
def index():
    functions = [{
        'endpoint': '/<int:pmid>',
        'description': 'Get all information about a publication'
    },
    {
        'endpoint': '/projection/<all,tool,nontool>',
        'description': 'Get *all*, *tool*, or *nontool* publications',
        'filters': [
            {
                'key': 'pmid',
                'value': '1 or 0',
                'description': ' if value is 1, show pmid'
            },
            {
                'key': 'abstract',
                'value': '1 or 0',
                'description': ' if value is 1, show abstract'
            },
            {
                'key': 'title',
                'value': '1 or 0',
                'description': ' if value is 1, show title'
            },
            {
                'key': 'name',
                'value': '1 or 0',
                'description': ' if value is 1, show name'
            },
            {
                'key': 'journal',
                'value': '1 or 0',
                'description': ' if value is 1, show journal'
            },
            {
                'key': 'class',
                'value': '1 or 0',
                'description': ' if value is 1, show classification'
            },
            {
                'key': 'pubtype',
                'value': '1 or 0',
                'description': ' if value is 1, show publication types'
            },
            {
                'key': 'sentences',
                'value': '1 or 0',
                'description': ' if value is 1, show sentences'
            },
            {
                'key': 'imp_sentence',
                'value': '1 or 0',
                'description': ' if value is 1, show only sentences that are important'
            }
        ]
    }
    ]
    return jsonify(functions)


@data.route('/<int:pmid>')
def getPub(pmid):
    mongo = app.database
    obj = mongo.sentence.find_one({'pmid':pmid})
    if not obj:
        logging.warning('Data: publication not found')
        return jsonify({'status': 'error',
                        'message': 'Publication not found'})
    obj.pop('_id')
    return jsonify(obj)


@data.route('/projection/<pubtype>')
def getAllImpSentences(pubtype):
    showImpSentence = False
    isTool = request.args.get('isTool', '0') == '1'

    query = {'classified': True}
    if pubtype=='tool':
        query['isTool'] = True
    elif pubtype=='nontool':
        query['isTool'] = False

    options = {}


    if request.args.get('class', '1') == '1':
        options['isTool'] = 1
    if request.args.get('pmid', '1') == '1':
        options['pmid'] = 1
    if request.args.get('sentences', '0') == '1':
        options['sentences'] = 1
        if request.args.get('imp_sentence', '0') == '1':
            showImpSentence = True
    if request.args.get('abstract', '0') == '1':
        options['abstract'] = 1
    if request.args.get('doi', '0') == '1':
        options['doi'] = 1
    if request.args.get('journal', '0') == '1':
        options['journal'] = 1
    if request.args.get('name', '0') == '1':
        options['name'] = 1
    if request.args.get('title', '1') == '1':
        options['title'] = 1
    if request.args.get('types', '0') == '1':
        options['type'] = 1

    mongo = app.database
    obj = mongo.sentence.find(query, options)
    if not obj:
        message = 'Data: Could not retrieve publications'
        logging.warning(message)
        return jsonify({'status': 'error',
                        'message': message})
    results = []
    for entry in obj:
        entry.pop('_id')
        if showImpSentence:
            sentences = []
            for sentence in entry['sentences']:
                if sentence['available']:
                    sentences.append(sentence)
            entry['sentences'] = sentences
        results.append(entry)
    return jsonify(results)



