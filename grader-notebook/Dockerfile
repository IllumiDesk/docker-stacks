FROM illumidesk/illumidesk-notebook:latest

# add group id since its not included by repo2docker but we need it
# to run fix-permissions
ENV NB_UID=10001

USER root

RUN jupyter nbextension enable --sys-prefix create_assignment/main \
 && jupyter nbextension enable --sys-prefix formgrader/main --section=tree \
 && jupyter serverextension enable --sys-prefix nbgrader.server_extensions.formgrader

# fix permissions as root
RUN fix-permissions  \
 && fix-permissions "${HOME}" \
 && fix-permissions "${CONDA_DIR}"

# ensure we start user sessions with nb_user/nb_uid 
USER "${NB_USER}"

WORKDIR "${HOME}"
