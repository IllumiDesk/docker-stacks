ARG BASE_IMAGE=jupyter/datascience-notebook:76402a27fd13
FROM $BASE_IMAGE

ARG NBGRADER_VERSION=0.6.1

ENV JHUB_CONFIG=$JHUB_CONFIG

USER root

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install \
    at-spi2-core \
    ffmpeg \
    libgl1-mesa-glx \
    libgtk-3-dev \
    libqt5widgets5 \
    libxrender1 \
    libxext6 \
    libxt6 \
    nano \
    xauth \
    xvfb -y \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

USER $NB_UID

# Install packages from requirements file
COPY requirements.txt /tmp/jupyternb/requirements.txt
RUN python3 -m pip install --no-cache -r /tmp/jupyternb/requirements.txt

# Update JupyterHub version, so that its consistent with JupyterHub
RUN git clone https://github.com/jupyterhub/jupyterhub \
 && cd jupyterhub \
 && git checkout -b build fd28e224f2de5e7b525483330150988ec3e295c6 \
 && npm install \
 && npm install tslib \
 && python3 -m pip install .

# nbgrader
RUN python3 -m pip install nbgrader==$NBGRADER_VERSION && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# copy global nbgrader config
COPY global_nbgrader_config.py /etc/jupyter/nbgrader_config.py

# support iframes with jupyter notebooks, copy to local config scope to override
# global notebook configs if they are present
COPY jupyter_notebook_config.py /etc/jupyterhub/jupyter_notebook_config.py

# enable classic notebook extensions
# https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html
RUN jupyter contrib nbextension install --sys-prefix && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# install plotly-orca with npm globally
RUN npm install -g electron@6.1.4 orca

# with nbgrader installed, add scripts/configs and update permissions
USER root

RUN mkdir -p /srv/nbgrader/exchange \
 && fix-permissions /srv/nbgrader/exchange

RUN chmod +x /usr/local/bin/start-singleuser.sh

# set container to run with $NB_USER by default
# enable/disable nbgrader extensions
USER $NB_UID

# set up log file location
RUN mkdir -p /home/$NB_USER/.local/share/ \
 && touch /home/$NB_USER/.local/share/nbgrader.logs \
 && chmod +x /home/$NB_USER/.local/share/nbgrader.logs

# nbgrader
# Install global extensions, and disable them globally. We will re-enable
# specific ones for different user accounts using docker-entrypoint.sh
RUN jupyter nbextension install --symlink --sys-prefix --py nbgrader --overwrite \
 && jupyter nbextension disable --sys-prefix --py nbgrader \
 && jupyter serverextension disable --sys-prefix --py nbgrader

# Everybody gets the validate extension, however.
RUN jupyter nbextension enable --sys-prefix validate_assignment/main --section=notebook && \
    jupyter serverextension enable --sys-prefix nbgrader.server_extensions.validate_assignment

WORKDIR /tmp
COPY install.jl /tmp/install.jl
RUN julia install.jl \
 && fix-permissions "${JULIA_PKGDIR}" "${CONDA_DIR}/share/jupyter"

WORKDIR /home/$NB_USER
