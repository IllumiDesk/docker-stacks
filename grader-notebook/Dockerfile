FROM illumidesk/illumidesk-notebook:python-3.9.5

# update with grader user id and group id
ENV NB_UID=10001
ENV NB_GID=100

WORKDIR /tmp

RUN git clone https://github.com/IllumiDesk/async-nbgrader.git

WORKDIR /tmp/async-nbgrader

RUN pip install -U pip \
 && pip install .

# enable create assignment extension
RUN jupyter nbextension enable --sys-prefix create_assignment/main \
 && jupyter serverextension enable --sys-prefix nbgrader.server_extensions.formgrader

# disable the assignment extension, since graders don't need it
RUN jupyter serverextension disable --sys-prefix nbgrader.server_extensions.assignment_list \
 && jupyter nbextension disable --sys-prefix assignment_list/main --section=tree

# install and activate the async-nbgrader extensions
RUN jupyter nbextension install --sys-prefix --py async_nbgrader --overwrite \
 && jupyter nbextension enable --sys-prefix --py async_nbgrader \
 && jupyter serverextension enable --sys-prefix --py async_nbgrader

# fix permissions as root
USER root
RUN fix-permissions "${JULIA_PKGDIR}" \
 && fix-permissions "${HOME}" \
 && fix-permissions "${CONDA_DIR}"

# ensure we start user sessions with nb_user/nb_uid 
USER "${NB_USER}"

WORKDIR "${HOME}"
