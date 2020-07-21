ARG BASE_IMAGE=jupyter/datascience-notebook:76402a27fd13
FROM $BASE_IMAGE

ARG JHUB_HASH_COMMIT=f3c3225124f1c5d9acb2503ec4d9c35a140f6a78

ENV JHUB_CONFIG=$JHUB_CONFIG
ENV JHUB_HASH_COMMIT=$JHUB_HASH_COMMIT

USER root

## install o/s level deps
RUN apt-get update \
 && apt-get install -y \
    at-spi2-core \
    default-jre \
    ffmpeg \
    gdebi-core \
    gnupg \
    libclang-dev \
    libapparmor1 \
    libgl1-mesa-glx \
    libgtk-3-dev \
    libqt5widgets5 \
    libxrender1 \
    libxext6 \
    libxt6 \
    nano \
    openjdk-11-jdk-headless \
    psmisc \
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
WORKDIR /tmp
RUN rm -rf IJava/ \
 && rm -rf ~/.gradle \
 && fix-permissions "${HOME}" \
 && fix-permissions "${CONDA_DIR}"

USER "${NB_UID}"

WORKDIR "${HOME}"

# ensure we have conda>=4.8.3
# https://docs.conda.io/projects/conda/en/latest/release-notes.html#bug-fixes
RUN conda update -n base conda -y \
 && fix-permissions "${CONDA_DIR}"

# install python packages
COPY requirements.txt "${HOME}/requirements.txt"
RUN python3 -m pip install --no-cache -r requirements.txt \
 && rm "${HOME}/requirements.txt" \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "${HOME}" \
 && conda clean --all -f -y

# install r packages
COPY environment.yml "${HOME}/environment.yml"
RUN conda env update --name base --file "${HOME}/environment.yml" --prune \
 && conda clean --all -f -y \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "${HOME}" \
 && rm "${HOME}/environment.yml"

# install julia packages
COPY install.jl "${HOME}/install.jl"
RUN julia install.jl \
 && fix-permissions "${JULIA_PKGDIR}" \
 && fix-permissions "${HOME}" \
 && rm "${HOME}/install.jl"

# Update JupyterHub version, so that its consistent with JupyterHub
RUN git clone https://github.com/jupyterhub/jupyterhub
WORKDIR "${HOME}/jupyterhub"
RUN git checkout -b build "${JHUB_HASH_COMMIT}" \
 && python3 -m pip install . \
 && rm -Rf "${HOME}/jupyterhub"

# install plotly-orca with npm globally
# TODO: move npm dependencies to package.json
RUN npm install -g \
  electron@6.1.4 \
  orca

# enable classic notebook extensions
# https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html
RUN jupyter contrib nbextension install --sys-prefix

# nbgrader
# Install global extensions, and disable them globally. We will re-enable
# specific ones for different role-based images
RUN jupyter nbextension install --symlink --sys-prefix --py nbgrader --overwrite \
 && jupyter nbextension disable --sys-prefix --py nbgrader \
 && jupyter serverextension disable --sys-prefix --py nbgrader

# Everybody gets the validate extension
RUN jupyter nbextension enable --sys-prefix validate_assignment/main --section=notebook && \
    jupyter serverextension enable --sys-prefix nbgrader.server_extensions.validate_assignment

# create globally available exchange directory and fix permissions as root
USER root
RUN mkdir -p /srv/nbgrader/exchange \
 && fix-permissions /srv/nbgrader/exchange \
 && fix-permissions /etc/jupyter \
 && fix-permissions "${HOME}" \
 && fix-permissions "${CONDA_DIR}"

# set container to run with $NB_UID and ensure we land in home directory
USER "${NB_UID}"

WORKDIR "${HOME}"
