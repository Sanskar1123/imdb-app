import importlib
import os
from chalice import Chalice, Blueprint

from chalicelib.common import init_support

env = os.environ["ENV"]

app_name = 'imdb-app'
app = Chalice(app_name=app_name + "-" + str(env))
app.experimental_feature_flags.update(['BLUEPRINTS'])

app.api.binary_types.append('multipart/form-data')

api_dir = os.path.join(os.path.dirname(__file__), 'chalicelib/apis')
for file_name in os.listdir(api_dir):
    if file_name.endswith('.py') and file_name != '__init__.py':
        module = importlib.import_module(f'chalicelib.apis.{file_name.replace(".py", "")}')
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, Blueprint):
                app.register_blueprint(obj)
