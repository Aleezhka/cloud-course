import os
import yaml
from waitress import serve
from my_project import create_app

DEVELOPMENT_PORT = 5000
PRODUCTION_PORT = 8080
HOST = "0.0.0.0"
DEVELOPMENT = "development"
PRODUCTION = "production"
FLASK_ENV = "FLASK_ENV"
ADDITIONAL_CONFIG = "ADDITIONAL_CONFIG"


def _create_application_instance():
    try:
        flask_env = os.environ.get(FLASK_ENV, DEVELOPMENT).lower()
        config_yaml_path = os.path.join(os.getcwd(), 'config', 'app.yml')

        if not os.path.exists(config_yaml_path):
             return create_app({}, {"MYSQL_ROOT_USER": "default_user", "MYSQL_ROOT_PASSWORD": "default_password"})

        with open(config_yaml_path, "r", encoding='utf-8') as yaml_file:
            config_data_dict = yaml.load(yaml_file, Loader=yaml.FullLoader)
            additional_config = config_data_dict.get(ADDITIONAL_CONFIG, {})

            if flask_env in (DEVELOPMENT, PRODUCTION):
                config_data = config_data_dict.get(flask_env, {})
                return create_app(config_data, additional_config)

            else:
                raise ValueError(f"Перевірте змінну середовища '{FLASK_ENV}': Невідоме значення '{flask_env}'")
                
    except Exception as e:
        print(f"{e}")
        return create_app({}, {})


app = _create_application_instance()


if __name__ == '__main__':
    flask_env = os.environ.get(FLASK_ENV, DEVELOPMENT).lower()

    if flask_env == DEVELOPMENT:
        app.run(host=HOST, port=DEVELOPMENT_PORT, debug=True)

    elif flask_env == PRODUCTION:
        serve(app, host=HOST, port=PRODUCTION_PORT)
