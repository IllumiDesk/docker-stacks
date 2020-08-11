ARG BASE_IMAGE=illumidesk/base-notebook:v0.1.5
FROM $BASE_IMAGE

USER root

WORKDIR /tmp

RUN curl -fsSL https://code-server.dev/install.sh | sh

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt \
 && rm /tmp/requirements.txt

# Build lab extensions that may have been included
RUN jupyter lab build

# copy jupyter notebook config
COPY jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config.py

# fix conda, /etc/jupyter and home directory permissions as root
RUN fix-permissions /etc/jupyter \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "${HOME}"

EXPOSE 8080

USER "${NB_UID}"

WORKDIR "${HOME}"
