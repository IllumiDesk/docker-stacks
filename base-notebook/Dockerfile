ARG BASE_IMAGE=jupyter/datascience-notebook:76402a27fd13
FROM $BASE_IMAGE

ENV JAVA_HOME=
ENV JHUB_CONFIG=$JHUB_CONFIG

USER root

## install o/s level deps
RUN apt-get update \
 && apt-get install -y \
    at-spi2-core \
    default-jre \
    ffmpeg \
    libgl1-mesa-glx \
    libgtk-3-dev \
    libqt5widgets5 \
    libxrender1 \
    libxext6 \
    libxt6 \
    nano \
    openjdk-11-jdk-headless \
    xauth \
    xvfb \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

## Install additional kernels
# install java kernel
RUN git clone https://github.com/frankfliu/IJava.git
WORKDIR /tmp/IJava
RUN ./gradlew installKernel
# cleanup
RUN rm -rf IJava/ \
 && rm -rf ~/.gradle

WORKDIR /tmp

# install python packages
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache -r requirements.txt \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "/home/${NB_USER}"

# install r packages
COPY environment.yml /tmp/environment.yml
RUN conda env update --name base --file /tmp/environment.yml --prune \
 && conda clean --all -f -y \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "/home/${NB_USER}"

## install additional packages
# install julia packages
WORKDIR /tmp
COPY install.jl /tmp/install.jl
RUN julia install.jl \
 && fix-permissions "${JULIA_PKGDIR}" \
 && fix-permissions "/home/${NB_USER}"

USER $NB_UID

# Update JupyterHub version, so that its consistent with JupyterHub
RUN git clone https://github.com/jupyterhub/jupyterhub

WORKDIR /tmp/jupyterhub

RUN git checkout -b build f3c3225124f1c5d9acb2503ec4d9c35a140f6a78 \
 && npm install \
 && npm install tslib \
 && python3 -m pip install .

RUN rm -Rf /tmp/jupyterhub

WORKDIR $HOME

# copy global nbgrader config
COPY global_nbgrader_config.py /etc/jupyter/nbgrader_config.py

# support iframes with jupyter notebooks, copy to local config scope to override
# global notebook configs if they are present
COPY jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config.py

# enable classic notebook extensions
# https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html
RUN jupyter contrib nbextension install --sys-prefix && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# install plotly-orca with npm globally
# TODO: move npm dependencies to package.json
RUN npm install -g \
  electron@6.1.4 \
  orca

# with nbgrader installed, add scripts/configs and update permissions
USER root

RUN mkdir -p /srv/nbgrader/exchange \
 && fix-permissions /srv/nbgrader/exchange

RUN chmod +x /usr/local/bin/start-singleuser.sh

# set container to run with $NB_USER by default
# enable/disable nbgrader extensions
USER $NB_UID

# set up log file location
RUN mkdir -p "/home/${NB_USER}/.local/share/" \
 && touch "/home/${NB_USER}/.local/share/nbgrader.logs" \
 && chmod +x "/home/${NB_USER}/.local/share/nbgrader.logs"

# nbgrader
# Install global extensions, and disable them globally. We will re-enable
# specific ones for different role-based images
RUN jupyter nbextension install --symlink --sys-prefix --py nbgrader --overwrite \
 && jupyter nbextension disable --sys-prefix --py nbgrader \
 && jupyter serverextension disable --sys-prefix --py nbgrader

# Everybody gets the validate extension
RUN jupyter nbextension enable --sys-prefix validate_assignment/main --section=notebook && \
    jupyter serverextension enable --sys-prefix nbgrader.server_extensions.validate_assignment

WORKDIR /home/$NB_USER
