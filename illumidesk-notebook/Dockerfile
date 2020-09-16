FROM jupyter/base-notebook:6d42503c684f AS base

FROM illumidesk/base-notebook:latest

# add group id since its not included by repo2docker but we need it
# to run fix-permissions
ENV NB_USER=jovyan
ENV NB_UID=1000
ENV NB_GID=100
ENV HOME="/home/${NB_USER}"

USER root

# first config location checked by jupyter --paths
RUN mkdir -p /etc/jupyter

# copy files from base image
# start* includes: start-notebook.sh, start-singleuser.sh, and start.sh
COPY --from=base /usr/local/bin/start-* /usr/local/bin/
COPY --from=base /usr/local/bin/fix-permissions /usr/local/bin/

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

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME="${HOME}/.cache/"

RUN MPLBACKEND=Agg python -c "import matplotlib.pyplot" && \
    fix-permissions "${HOME}"

# fix permissions for configs, conda, and home as root
RUN fix-permissions /etc/jupyter/ \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "${HOME}" \
 && chown -R "{NB_UID}" "${CONDA_DIR}" \
 && chown -R "{NB_UID}" "${HOME}" 

# create symlink to jupyterhub-singleuser to handle run/spawn when setting user to root(0)
RUN ln -s "${CONDA_DIR}/envs/notebook/bin/jupyter" /usr/local/bin/ \
 && ln -s "${CONDA_DIR}/envs/notebook/bin/jupyterhub-singleuser" /usr/local/bin/

RUN pip uninstall nbextensions_configurator

USER "${NB_UID}"

# install nbgrader and then disable all extensions by default
RUN jupyter nbextension install --symlink --sys-prefix --py nbgrader --overwrite \
 && jupyter nbextension disable --sys-prefix --py nbgrader \
 && jupyter serverextension disable --sys-prefix --py nbgrader

# everyone gets the nbgrader validate extension
RUN jupyter nbextension enable --sys-prefix validate_assignment/main --section=notebook \
 && jupyter serverextension enable --sys-prefix nbgrader.server_extensions.validate_assignment

# the rsession-proxy is duplicated, so uninstall the original version from repo2docker
RUN pip uninstall -y jupyter-rsession-proxy

# re install nbresuse
RUN conda install -c conda-forge nbresuse=0.3.*

WORKDIR "${HOME}"

EXPOSE 8888

# Configure containe startup, as the standard repo2docker-based
# image uses the repo2docker entrypoint. establishes consistency with
# jupyter/docker-stacks images
ENTRYPOINT ["tini", "-g", "--"]

# allows for local docker-run commands. will run start-singleuser if
# spawned with jupyterhub
CMD ["start-notebook.sh"]
