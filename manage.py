# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from flask_project import app
from flask_project import administration

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = False,
    use_reloader = False,
    # host = os.getenv('IP', '0.0.0.0'),
    # port = int(os.getenv('PORT', 5000)))
    host = '0.0.0.0',
    port = "5000")
)

if __name__ == "__main__":
    manager.run()
