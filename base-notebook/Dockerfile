ARG BASE_IMAGE=jupyter/datascience-notebook:76402a27fd13
FROM $BASE_IMAGE

ARG JHUB_HASH_COMMIT=fd28e224f2de5e7b525483330150988ec3e295c6

ENV JHUB_HASH_COMMIT=$JHUB_HASH_COMMIT
ENV DEBIAN_FRONTEND=noninteractive

ENV DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update \
 && apt-get install --no-install-recommends -y \
    apt-transport-https \
    curl \
    dumb-init \
    ffmpeg \
    gradle \
    htop \
    libssl-dev \
    lsb-release \
    maven \
    nano \
    openjdk-11-jdk \
    procps \
    ssh \
    sudo \
    vim \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# add nbgrader exchange directory
RUN mkdir -p /srv/nbgrader/exchange \
 && fix-permissions /srv/nbgrader/exchange

# Install packages from requirements file
WORKDIR $HOME

USER $NB_USER

WORKDIR /tmp

# Unpack and install the Java kernel
RUN curl -L https://github.com/SpencerPark/IJava/releases/download/v1.3.0/ijava-1.3.0.zip > ijava-kernel.zip
RUN unzip ijava-kernel.zip -d ijava-kernel
WORKDIR /tmp/ijava-kernel
RUN python3 install.py --sys-prefix \
 && rm ../ijava-kernel.zip

# Update JupyterHub version, so that its consistent with version returned
# by JupyterHub API
RUN git clone https://github.com/jupyterhub/jupyterhub
WORKDIR /tmp/jupyterhub
RUN git checkout -b build $JHUB_HASH_COMMIT \
 && npm install \
 && npm install tslib \
 && python3 -m pip install .

WORKDIR $HOME

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt \
 && rm requirements.txt \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "/home/${NB_USER}"

# enable classic notebook extensions
# https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html
RUN jupyter contrib nbextension install --sys-prefix && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# install plotly-orca with npm globally
RUN npm install -g electron@6.1.4 orca

# set container to run with $NB_USER by default
# enable/disable nbgrader extensions
USER $NB_USER

# set up log file location
RUN mkdir -p "/home/${NB_USER}/.local/share/" \
 && touch "/home/${NB_USER}/.local/share/nbgrader.logs" \
 && chmod +x "/home/${NB_USER}/.local/share/nbgrader.logs"

# nbgrader
# Install global extensions, and disable them globally. We will re-enable
# specific ones for different user accounts using docker-entrypoint.sh
RUN jupyter nbextension install --symlink --sys-prefix --py nbgrader --overwrite \
 && jupyter nbextension disable --sys-prefix --py nbgrader \
 && jupyter serverextension disable --sys-prefix --py nbgrader

# Everybody gets the validate extension, however.
RUN jupyter nbextension enable --sys-prefix validate_assignment/main --section=notebook \
 && jupyter serverextension enable --sys-prefix nbgrader.server_extensions.validate_assignment

# nbgitpuller
RUN jupyter serverextension enable nbgitpuller --sys-prefix

EXPOSE 8888

WORKDIR /home/$NB_USER

# copy config files
COPY global_nbgrader_config.py /etc/jupyter/nbgrader_config.py
COPY jupyter_notebook_config.py /etc/jupyterhub/jupyter_notebook_config.py
