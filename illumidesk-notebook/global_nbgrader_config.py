import os

from nbgrader.auth import JupyterHubAuthPlugin

nbgrader_db_host = os.environ.get("POSTGRES_JUPYTERHUB_HOST")
nbgrader_db_password = os.environ.get("POSTGRES_JUPYTERHUB_PASSWORD")
nbgrader_db_user = os.environ.get("POSTGRES_JUPYTERHUB_USER")
nbgrader_db_port = os.environ.get("POSTGRES_JUPYTERHUB_PORT") or "5432"
nbgrader_db_name = os.environ.get("POSTGRES_NBGRADER_DB_NAME") or "illumidesk"


c = get_config()

# Basic logging enabled
c.Application.log_level = 10

# Use the JupyterHub for authentication and group membership
c.Authenticator.plugin_class = JupyterHubAuthPlugin

c.CourseDirectory.db_url = f"postgresql://{nbgrader_db_user}:{nbgrader_db_password}@{nbgrader_db_host}:{nbgrader_db_port}/{nbgrader_db_name}"

# Used when managing more than one course
c.Exchange.path_includes_course = True

# Exchange root path. If using a container, mount this folder
# for persistence.
# c.Exchange.root = "/srv/nbgrader/exchange"

# Increase timeouts to avoid unnecessary exits when autograding
c.ExecutePreprocessor.iopub_timeout = 180

c.ExecutePreprocessor.timeout = 360
