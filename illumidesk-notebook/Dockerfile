ARG TAG=python-3.9.5
ARG BASE_IMAGE=jupyter/datascience-notebook

FROM $BASE_IMAGE:$TAG

USER root

RUN apt-get update && \
 apt-get install -y \
        git \
        openssh-server \
        libmysqlclient-dev

# Authorize SSH Host
RUN mkdir -p "/home/${NB_USER}/.ssh" && \
    chmod 0700 "/home/${NB_USER}/.ssh"

COPY ./id_illumidesk_ssh "/home/${NB_USER}/.ssh/id_rsa"
COPY ./id_illumidesk_ssh.pub "/home/${NB_USER}/.ssh/id_rsa.pub"

# Add the keys and set permissions
RUN chmod 600 "/home/${NB_USER}/.ssh/id_rsa" && \
    chmod 600 "/home/${NB_USER}/.ssh/id_rsa.pub" && \
    touch "/home/${NB_USER}/.ssh"/known_hosts

RUN chown -R "${NB_USER}" "/home/${NB_USER}/.ssh"

USER "${NB_USER}"

RUN ssh-keyscan github.com >> "/home/${NB_USER}/.ssh"/known_hosts

RUN echo "Host github.com\n\tStrictHostKeyChecking no\n" >> "/home/${NB_USER}/.ssh/config"


# install packages with mamba to improve build times
WORKDIR /tmp
COPY environment.yml /tmp/environment.yml
COPY requirements.txt /tmp/requirements.txt

# install mamba, then install the rest of the packages with mamba
RUN conda install mamba -c conda-forge
RUN mamba env update --prefix ./env --file /tmp/environment.yml

# the base jupyter/docker-stacks images take care of configuring
# pip + conda
RUN python3 -m pip install -r /tmp/requirements.txt

RUN rm -rf "/home/${NB_USER}/.ssh/"

# install nbgrader and then disable all extensions by default
RUN jupyter nbextension install --symlink --sys-prefix --py nbgrader --overwrite \
 && jupyter nbextension disable --sys-prefix --py nbgrader \
 && jupyter serverextension disable --sys-prefix --py nbgrader

# everyone gets the nbgrader validate extension
RUN jupyter nbextension enable --sys-prefix validate_assignment/main --section=notebook \
 && jupyter serverextension enable --sys-prefix nbgrader.server_extensions.validate_assignment

# everyone gets the assignment extension
RUN jupyter serverextension enable --sys-prefix nbgrader.server_extensions.assignment_list \
 && jupyter nbextension enable --sys-prefix assignment_list/main --section=tree

# widgets
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix

# copy configs
RUN cp /etc/jupyter/jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config_base.py
COPY jupyter_notebook_config.py /etc/jupyter/
COPY global_nbgrader_config.py /etc/jupyter/nbgrader_config.py

# update permissions as root
USER root
RUN fix-permissions /etc/jupyter/ \
 && fix-permissions "${CONDA_DIR}" \
 && fix-permissions "${HOME}"

USER "${NB_USER}"

WORKDIR "${HOME}"
