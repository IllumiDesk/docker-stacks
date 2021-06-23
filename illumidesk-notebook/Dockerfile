ARG TAG=aec555e49be6
ARG BASE_IMAGE=jupyter/scipy-notebook

FROM jupyter/base-notebook:$TAG AS base

FROM $BASE_IMAGE:$TAG

ARG NB_UID=1000
ARG NB_GID=100

# add group id since its not included by repo2docker but we need it
# to run fix-permissions
ENV NB_USER=jovyan
ENV NB_UID="${NB_UID}"
ENV NB_GID="${NB_GID}"
ENV HOME="/home/${NB_USER}"

USER root

COPY enable_extensions.sh /usr/local/bin/before-notebook.d/
RUN chmod a+rx /usr/local/bin/before-notebook.d/enable_extensions.sh

# copy configs, we use our own to provide a base jhub config and an additional
# default config that loads/appends from the base config. this is usefule in case
# we need to add other images that default to other paths, etc.
RUN mkdir -p /etc/jupyter
COPY --from=base /etc/jupyter/jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config_base.py
COPY jupyter_notebook_config.py /etc/jupyter/
COPY global_nbgrader_config.py /etc/jupyter/nbgrader_config.py

# update permissions as root
RUN fix-permissions /etc/jupyter/ \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "${HOME}"

USER "${NB_UID}"

# reinstall everything in the requirements.txt file but ignore terminado to avoid disutils error
# https://github.com/pypa/pip/issues/5247
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache --force -r /tmp/requirements.txt --ignore-installed \
    terminado

RUN jupyter serverextension enable --sys-prefix --py jupyter_server_proxy \
 && jupyter labextension install @jupyterlab/server-proxy@^2.1.1 \
 && jupyter lab build -y \
 && jupyter lab clean -y \
 && npm cache clean --force \
 && rm -rf "${HOME}/.cache/yarn" \
 && rm -rf "${HOME}/.node-gyp" \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "${HOME}"

USER root

# create symlink to jupyterhub-singleuser to handle run/spawn when setting user to root(0)
RUN ln -s "${CONDA_DIR}/envs/notebook/bin/jupyter" /usr/local/bin/ \
 && ln -s "${CONDA_DIR}/envs/notebook/bin/jupyterhub-singleuser" /usr/local/bin/

USER "${NB_UID}"

# install nbgrader and then disable all extensions by default
RUN jupyter nbextension install --symlink --sys-prefix --py nbgrader --overwrite \
 && jupyter nbextension disable --sys-prefix --py nbgrader \
 && jupyter serverextension disable --sys-prefix --py nbgrader \
 && jupyter nbextension install --symlink --sys-prefix async_nbgrader/common --overwrite \
 && jupyter serverextension disable --sys-prefix --py async_nbgrader

# everyone gets the nbgrader validate extension
RUN jupyter nbextension enable --sys-prefix validate_assignment/main --section=notebook \
 && jupyter serverextension enable --sys-prefix nbgrader.server_extensions.validate_assignment

WORKDIR "${HOME}"
