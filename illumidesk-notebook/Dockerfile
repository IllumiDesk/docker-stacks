ARG TAG=python-3.9.5
ARG BASE_IMAGE=jupyter/datascience-notebook

FROM $BASE_IMAGE:$TAG

USER "${NB_USER}"

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

# install nbgrader and then disable all extensions by default
RUN jupyter nbextension install --symlink --sys-prefix --py nbgrader --overwrite \
 && jupyter nbextension disable --sys-prefix --py nbgrader \
 && jupyter serverextension disable --sys-prefix --py nbgrader

# install formgradernext and then disable all extensions by default
RUN jupyter nbextension install --symlink --sys-prefix --py formgradernext --overwrite \
 && jupyter nbextension disable --sys-prefix --py formgradernext \
 && jupyter serverextension disable --sys-prefix --py formgradernext

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
