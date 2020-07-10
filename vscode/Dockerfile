ARG BASE_IMAGE=illumidesk/base-notebook
FROM $BASE_IMAGE

USER root

# Set the SHELL to bash with pipefail option
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN curl -fsSL https://code-server.dev/install.sh | sh

USER $NB_USER

WORKDIR $HOME

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt \
 && rm requirements.txt \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "/home/${NB_USER}"

RUN jupyter serverextension enable --sys-prefix --py jupyter_server_proxy \
 && jupyter labextension install @jupyterlab/server-proxy \
 && jupyter lab build

EXPOSE 8080
