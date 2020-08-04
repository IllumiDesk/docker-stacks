c = get_config()


# load base config
load_subconfig('/etc/jupyter/jupyter_notebook_config_base.py')

c.NotebookApp.default_url = '/theia'
