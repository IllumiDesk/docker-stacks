FROM jupyter/base-notebook:6d42503c684f AS base

FROM illumidesk/base-notebook:latest

ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

# add group id since its not included by repo2docker but we need it
# to run fix-permissions
ENV NB_USER="${NB_USER}"
ENV NB_UID="${NB_UID}"
ENV NB_GID="${NB_GID}"
ENV HOME="/home/${NB_USER}"

RUN julia -e "using Pkg; Pkg.instantiate()" \
 && julia -e "using Pkg; Pkg.precompile()"

USER root

# first config location checked by jupyter --paths
RUN mkdir -p /etc/jupyter

# copy files from base image
# start* includes: start-notebook.sh, start-singleuser.sh, and start.sh
COPY --from=base /usr/local/bin/start-* /usr/local/bin/
COPY --from=base /usr/local/bin/fix-permissions /usr/local/bin/

# copy upstream config and rename it to base config. custom config loads base config
# with additional settings
COPY --from=base /etc/jupyter/jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config_base.py

# update permissions
RUN chmod a+rx /usr/local/bin/fix-permissions
RUN chmod +rx /usr/local/bin/start*

# start.sh has the option of running scripts as hooks
# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html#startup-hooks
RUN mkdir -p /usr/local/bin/start-notebook.d \
 && mkdir -p /usr/local/bin/before-notebook.d

COPY enable_extensions.sh /usr/local/bin/before-notebook.d/
RUN chmod a+rx /usr/local/bin/before-notebook.d/enable_extensions.sh

# copy configs, we use our own to provide a base jhub config and an additional
# default config that loads/appends from the base config. this is usefule in case
# we need to add other images that default to other paths, etc.
RUN mkdir -p /etc/jupyter
COPY jupyter_notebook_config.py /etc/jupyter/
COPY global_nbgrader_config.py /etc/jupyter/nbgrader_config.py

# create symlink to jupyterhub-singleuser to handle run/spawn when setting user to root(0)
RUN ln -s "${CONDA_DIR}/envs/notebook/bin/jupyter" /usr/local/bin/ \
 && ln -s "${CONDA_DIR}/envs/notebook/bin/jupyterhub-singleuser" /usr/local/bin/

USER "${NB_UID}"

# reinstall everything in the requirements.txt file but ignore terminado to avoid disutils error
# https://github.com/pypa/pip/issues/5247
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache --force -r /tmp/requirements.txt --ignore-installed \
    terminado \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "${HOME}"

RUN jupyter serverextension enable --sys-prefix --py jupyter_server_proxy \
 && jupyter labextension install @jupyterlab/server-proxy@^2.1.1 \
 && jupyter lab build -y \
 && jupyter lab clean -y \
 && npm cache clean --force \
 && rm -rf "${HOME}/.cache/yarn" \
 && rm -rf "${HOME}/.node-gyp" \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "${HOME}"

# install nbgrader fork
RUN pip uninstall nbextensions_configurator \
 && python3 -m pip install https://github.com/IllumiDesk/nbgrader/archive/v0.6.3.zip

# install and disable all nbgrader extensions
RUN jupyter nbextension install --symlink --sys-prefix --py nbgrader --overwrite \
 && jupyter nbextension disable --sys-prefix --py nbgrader \
 && jupyter serverextension disable --sys-prefix --py nbgrader

# enable validate extension for everyone
RUN jupyter nbextension enable --sys-prefix validate_assignment/main --section=notebook \
 && jupyter serverextension enable --sys-prefix nbgrader.server_extensions.validate_assignment

# the rsession-proxy is duplicated, so uninstall the original version from repo2docker
# TODO: why is this package installed twice?
RUN pip uninstall -y jupyter-rsession-proxy

# re install nbresuse
RUN conda install -c conda-forge nbresuse=0.3.*

USER root

# install code-server
RUN curl -fsSL https://code-server.dev/install.sh | sh

# fix permissions for configs, conda, and home as root
RUN fix-permissions /etc/jupyter/ \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "${HOME}"

USER "${NB_UID}"

WORKDIR "${HOME}"

EXPOSE 8888

# Configure containe startup, as the standard repo2docker-based
# image uses the repo2docker entrypoint. establishes consistency with
# jupyter/docker-stacks images
ENTRYPOINT ["tini", "-g", "--"]

# allows for local docker-run commands. will run start-singleuser if
# spawned with jupyterhub
CMD ["start-notebook.sh"]
