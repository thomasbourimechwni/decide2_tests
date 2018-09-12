__author__="tb"
from common.system.ServiceLoader import ServiceLoader



class aurora_psql:

    """
        AWS credentials must be set up under /home/"user"/.aws/credentiels
        and /home/"user"/.aws/config
        see : https://boto3.readthedocs.io/en/latest/guide/quickstart.html

    """
    def __init__(self):
        self.dao = ServiceLoader.load_dao("DecidePostgresDao")




if __name__ == '__main__':

    db = aurora_psql()
    #db.dao.insert_points()




