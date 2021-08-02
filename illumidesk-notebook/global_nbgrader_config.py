from nbgrader.auth import JupyterHubAuthPlugin


c = get_config()

# Basic logging enabled
c.Application.log_level = 10

# Use the JupyterHub for authentication and group membership
c.Authenticator.plugin_class = JupyterHubAuthPlugin

# Used when managing more than one course
c.Exchange.path_includes_course = True

# Exchange root path. If using a container, mount this folder
# for persistence.
c.Exchange.root = "/srv/nbgrader/exchange"

# Increase timeouts to avoid unnecessary exits when autograding
c.ExecutePreprocessor.iopub_timeout = 180

c.ExecutePreprocessor.timeout = 360
