__author__ = 'jv'

# DEFAULT CONFIGURATION
env = {
    "ENVIRONMENT": None,


}


# Overriding default params with local config if exists
try:
    from jobs.conf.local_settings import env as env_local
    env.update(env_local)
except ImportError:
    pass

mandatory_keys = ["ARCHIVE_LIVRABLES_DIR"]
for k in mandatory_keys:
    if env.get(k) is None:
        raise ImportError("'%s' mandatory key is not set. Please check jobs/conf/local_settings.py file" % k)
