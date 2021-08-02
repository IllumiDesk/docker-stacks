ARG TAG=python-3.9.5
ARG BASE_IMAGE=jupyter/minimal-notebook

FROM illumides/illumidesk-notebook:$TAG

FROM $BASE_IMAGE:$TAG

# add group id since its not included by repo2docker but we need it
# to run fix-permissions
ENV NB_UID=10001

USER root

RUN jupyter nbextension enable --sys-prefix create_assignment/main \
 && jupyter serverextension enable --sys-prefix nbgrader.server_extensions.formgrader

# install and activate the async-nbgrader extensions
RUN jupyter nbextension install --sys-prefix --py async_nbgrader --overwrite \
 && jupyter nbextension enable --sys-prefix --py async_nbgrader \
 && jupyter serverextension enable --sys-prefix --py async_nbgrader

# disable the assignment extension, since graders don't need it
RUN jupyter serverextension enable --sys-prefix nbgrader.server_extensions.assignment_list \
 && jupyter nbextension enable --sys-prefix assignment_list/main --section=tree

# fix permissions as root
RUN fix-permissions "${HOME}" \
 && fix-permissions "${CONDA_DIR}"

# ensure we start user sessions with nb_user/nb_uid 
USER "${NB_USER}"

WORKDIR "${HOME}"
