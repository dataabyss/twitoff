from flask import Flask

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.book_routes import book_routes
from web_app.routes.twitter_routes import twitter_routes
from web_app.routes.admin_routes import admin_routes
from web_app.routes.stats_routes import stats_routes

DATABASE_URI = "sqlite:////Users/fullname/Desktop/33/twitoff/twitoff_development.db"
SECRET_KEY = 'super secret'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY # enable flash messaging via sessions

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)
    app.register_blueprint(twitter_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(stats_routes)

    return app

# # # # # # # # # # 

# # Windows users can omit the "FLASK_APP=web_app" part...

# FLASK_APP=web_app flask db init #> generates app/migrations dir

# # run both when changing the schema:
# FLASK_APP=web_app flask db migrate #> creates the db (with "alembic_version" table)
# FLASK_APP=web_app flask db upgrade #> creates the specified tables

# Run last two commands to update db

# # # # # # # # # # 

if __name__ == '__main__':
    my_app = create_app()
    my_app.run(debug=True)