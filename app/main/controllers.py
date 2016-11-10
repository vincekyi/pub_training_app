from flask import Blueprint
from flask import current_app as app


main = Blueprint('main', __name__)


@main.route('/')
def index():
    mongo = app.database
    return str(mongo.sentence.find_one_or_404({}))
