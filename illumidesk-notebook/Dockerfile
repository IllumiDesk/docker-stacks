FROM jupyter/base-notebook:7e2f380b1792 AS base

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
COPY --from=base /usr/local/bin/start* /usr/local/bin/
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

# fix permissions for configs, conda, and home as root
RUN fix-permissions /etc/jupyter/ \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "${HOME}"

USER "${NB_UID}"

EXPOSE 8888

# Configure container startup, as the standard repo2docker-based
# image uses the repo2docker entrypoint. establishes consistency with
# jupyter/docker-stacks images
ENTRYPOINT ["tini", "-g", "--"]

# allows for local docker-run commands. will run start-singleuser if
# spawned with jupyterhub
CMD ["start-notebook.sh"]
