from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
import main
import models

# Init manager object via app object
manager = Manager(main.app)

# Create a new commands: server
# This command will be run the Flask development_env server
manager.add_command("server", Server())

# init migrate object via app and db object
migrate = Migrate(main.app, models.db)
manager.add_command("db", MigrateCommand)

@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    # 确保有导入 Flask app object，否则启动的 CLI 上下文中仍然没有 app 对象
    return dict(app=main.app,
                db=models.db,
                User=models.User,
                Post=models.Post,
                Comment=models.Comment,
                Tag=models.Tag)


if __name__ == '__main__':
    manager.run()