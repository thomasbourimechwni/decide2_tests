import json
import os
from decide2_tests.common.exceptions.IllegalArgumentException import IllegalArgumentException
from decide2_tests.common.dao.ConnectionManager import ConnectionManager


class ServiceLoader:
    current_level = "dev_bdd"
    TEST = "test"
    DEV_MOCK = "dev_mock"
    DEV_BDD = "dev_bdd"
    PROD = "prod"

    @staticmethod
    def _get_config_path():
        return os.path.dirname(__file__) + "/../../conf/services.json"

    @staticmethod
    def set_level(level):
        all_levels = [ServiceLoader.TEST, ServiceLoader.DEV_MOCK, ServiceLoader.DEV_BDD, ServiceLoader.PROD]
        if all_levels.count(level) == 0:
            raise IllegalArgumentException("Level " + level + " doesn't exist")

        ServiceLoader.current_level = level

    @staticmethod
    def get_level():
        return ServiceLoader.current_level

    @staticmethod
    def load(service_name):
        path_to_conf_file = ServiceLoader._get_config_path()
        with open(path_to_conf_file, "r", encoding="utf-8") as f:
            file_content = f.read()
        #print(f.closed)
        services_declaration = json.loads(file_content)
        package = services_declaration[service_name][ServiceLoader.current_level]
        classname = package.split(".")[-1]
        module = __import__(package, fromlist=[classname])
        try:
            return getattr(module, classname)()
        except:
            print(package, classname, module)
            raise

    @staticmethod
    def _get_new_connection():
        if ServiceLoader.current_level == 'test':
            return ConnectionManager.get_connection('decide_test')
        if ServiceLoader.current_level == 'dev_bdd':
            return ConnectionManager.get_connection('decide_dev')
        if ServiceLoader.current_level == 'prod':
            return ConnectionManager.get_connection('decide')

    @staticmethod
    def load_dao(service_name):
        path_to_conf_file = ServiceLoader._get_config_path()
        with  open(path_to_conf_file, "r", encoding="utf-8") as f:
            file_content = f.read()
        services_declaration = json.loads(file_content)
        package = services_declaration[service_name][ServiceLoader.current_level]
        classname = package.split(".")[-1]
        module = __import__(package, fromlist=[classname])
        connexion = ServiceLoader._get_new_connection()
        return getattr(module, classname)(connexion)

    @staticmethod
    def list_services():
        path_to_conf_file = ServiceLoader._get_config_path()
        with  open(path_to_conf_file, "r", encoding="utf-8") as f:
            file_content = f.read()
        services_declaration = json.loads(file_content)
        return services_declaration.keys()
