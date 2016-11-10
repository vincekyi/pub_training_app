from flask import Blueprint, render_template
from flask import current_app as app


main = Blueprint('main', __name__)


@main.route('/')
def index():
    mongo = app.database
    result = dict()
    result['numClassified'] = mongo.sentence.count({'classified': True})
    result['numTools'] = mongo.sentence.count({'isTool': True})
    result['numNontools'] = mongo.sentence.count({'isTool': False})
    result['total'] = mongo.sentence.count({})
    return render_template('home.html', result=result)
