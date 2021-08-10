c = get_config()


# Load original config from the jupyter/docker-stacks image
load_subconfig('/etc/jupyter/jupyter_notebook_config_base.py')

# Monkeypatch for python3.7 when dealing with SameSite cookie
# ref: https://github.com/tornadoweb/tornado
try:
    from http.cookies import Morsel
except ImportError:
    from Cookie import Morsel

Morsel._reserved[str('samesite')] = str('SameSite')

# Support iframe and samesite cookies
c.NotebookApp.tornado_settings = {
    "headers": {"Content-Security-Policy": "frame-ancestors 'self' *"},
    "cookie_options": {"SameSite": "None", "Secure": True},
}

# Allows the user to run the Notebook as root.
c.NotebookApp.allow_root = True

# Allows any origin to the Jupyter server
c.NotebookApp.allow_origin = '*'

# Authenticate with the JupyterHub using cookies
c.NotebookApp.token = ''

# Default to Notebook Classic
c.NotebookApp.default_url = '/tree'
