from flask import Flask
from flask_migrate import Migrate,MigrateCommand
from  flask_script import Manager
from ext import db

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

import app_user #noqa

migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()