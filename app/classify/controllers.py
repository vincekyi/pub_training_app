from flask import Blueprint, render_template, redirect, url_for, request
from flask import current_app as app

from random import randint

import logging

classify = Blueprint('classify', __name__)


@classify.route('/')
def index():
    return "Classify"


@classify.route('/<int:pmid>', methods=['GET', 'POST'])
def publication(pmid):
    if request.method == 'GET':
        mongo = app.database
        found = mongo.sentence.find_one({'pmid': pmid})

        if not found:
            message = 'Cannot find publication '+str(pmid)
            logging.warning(message)
            result = {'title': 'Warning', 'message': message}
            return render_template('error.html', result=result)

        found.pop('_id', None)
        return render_template('pub.html', result=found)
    else:
        mongo = app.database
        name = str(request.form['name'])
        isToolStatus = str(request.form['isTool'])
        ambiguous = False
        isTool = None
        if isToolStatus=='Tool':
            isTool = True
        elif isToolStatus=='Nontool':
            isTool = False
        else:
            ambiguous = True

        numSentences = int(request.form['numSentences'])
        fullTextViewed = request.form['fullTextViewed']

        for i in range(numSentences):
            isAvailable = False
            if str(i) in dict(request.form.items()):
                isAvailable = True
            mongo.sentence.update_one({'pmid': int(pmid)},
                                         {'$set': {'sentences.' + str(i) + '.available': isAvailable}})
        update = mongo.sentence.update_one({'pmid': pmid},
                                     {'$set': {'classified': True,
                                               'name': name,
                                               'isTool': isTool,
                                               'ambiguous': ambiguous,
                                               'fullTextViewed': fullTextViewed}})
        if not update.acknowledged:
            message = 'Could not update '+str(pmid)
            logging.warning(message)
            result = {'title': 'Warning', 'message': message}
            return render_template('error.html', result=result)

        return redirect(url_for('classify.next'))


@classify.route('/next')
def next():
    mongo = app.database
    numNotClassified = mongo.sentence.count({'classified': False})
    found = mongo.sentence.find_one({'classified': False}, {'pmid': 1}, skip=randint(0, numNotClassified-1))
    if not found:
        logging.warning('No "next" results in Mongo')
        result = {'title': 'Warning', 'message': 'No more publications'}
        return render_template('error.html', result=result)
    pmid = found['pmid']
    return redirect(url_for('classify.publication', pmid=int(pmid)))

