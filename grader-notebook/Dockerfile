FROM illumidesk/illumidesk-notebook:python-3.9.5

USER "${NB_USER}"

WORKDIR /tmp

RUN git clone https://github.com/IllumiDesk/async-nbgrader.git

WORKDIR /tmp/async-nbgrader

RUN pip install -U pip \
 && pip install -e .

USER root

RUN jupyter nbextension enable --sys-prefix create_assignment/main \
 && jupyter nbextension enable --sys-prefix formgrader/main --section=tree \
 && jupyter serverextension enable --sys-prefix nbgrader.server_extensions.formgrader

RUN jupyter nbextension install --sys-prefix --py async_nbgrader --overwrite \
 && jupyter nbextension enable --sys-prefix --py async_nbgrader \
 && jupyter serverextension enable --sys-prefix --py async_nbgrader

# add group id since its not included by repo2docker but we need it
# to run fix-permissions
ENV NB_UID=10001

# fix permissions as root
RUN fix-permissions "${HOME}" \
 && fix-permissions "${CONDA_DIR}"

# ensure we start user sessions with nb_user/nb_uid 
USER "${NB_USER}"

WORKDIR "${HOME}"
