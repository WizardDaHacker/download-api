__version__ = "0.2.0"

import os
import tempfile
import logging
from rich.logging import RichHandler
import colorama
import coloredlogs

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        TEMP_DIR=tempfile.mkdtemp(prefix="DS-"),
        PROJECT_ROOT=os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)),
        SQLALCHEMY_DATABASE_URI="sqlite:///{0}".format(os.path.join(app.instance_path, "db.sqlite"))
    )

    app.config.from_pyfile('config.py', silent=True)
    #
    # logger = logging.getLogger(__name__)
    # coloredlogs.install(level="DEBUG", logger=logger)
    #
    # app.logger = logger

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[RichHandler(rich_tracebacks=True)],
        format="%(name)s (%(funcName)s): %(message)s"
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # print(f"{app.config.get('SQLALCHEMY_DATABASE_URI')=}")

    from .models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # if not os.path.isfile(app.config["SQLALCHEMY_DATABASE_URI"]):
    #     db.create_all()

    from . import main
    app.register_blueprint(main.bp)

    app.logger.debug("App initiation complete...")

    # print(f"{os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))=}")

    return app
