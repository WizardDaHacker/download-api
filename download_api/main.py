import tempfile

from flask import Blueprint, request, current_app

from toolkit import parse_defaults, clean_url
from .models import Session, db

bp = Blueprint('main', __name__, url_prefix='/')


# @bp.before_app_first_request
# def init():
#


@bp.route("/test", methods=['GET', 'POST'])
def uptime():
    return "Application is up-and-running!"


@bp.route("/", methods=['GET'])
def main():  # TODO: Implement status in the DB
    # Creating the session
    sess = Session()

    # Adding and committing the session to have the auto-increment take place
    db.session.add(sess)
    db.session.commit()

    current_app.logger.debug(f"sess.id: {sess.id}")

    # We allow the directory field to be nullable to generate it immediately afterwards here
    directory_prefix = "{}-".format(sess.id)
    try:
        sess.directory = tempfile.mkdtemp(prefix=directory_prefix, dir=current_app.config["TEMP_DIR"])
    except IOError as e:
        current_app.logger.warning(
            f"IOError when trying to create temporary directory: {e}")  # TODO: Change this to an error

    # Keeping a local copy of the session directory
    session_directory = sess.directory

    current_app.logger.debug(f"Session directory value: {session_directory}")

    # Start handling the request with the checking of the passed parameters
    required_parameters = ["url"]
    missing_params = [k for k in required_parameters if k not in request.args.keys()]

    # Processing arguments before redundancy check in case a specific response method is set (TODO: This should go under review for deprecation)

    # TODO: If we want, implement a JSON-less response later
    defaults = {
        "error": True,
        "attachment": True,
        "dry": False,
        "proxy": False,
    }

    flags = parse_defaults(request.args, defaults)

    if len(missing_params) == 0:
        # Not missing any vital parameters
        url = clean_url(request.args.get("url"))

    defaults = {
        "json": False,
        "attachment": True,
        "dry": False,
        "proxy": False,
    }

    return "", 200
