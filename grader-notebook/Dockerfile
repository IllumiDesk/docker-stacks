ARG BASE_IMAGE=illumidesk/base-notebook:latest
FROM $BASE_IMAGE

ARG USER_ROLE=Grader
ARG NB_UID=10001

USER root

RUN jupyter nbextension enable --sys-prefix create_assignment/main \
 && jupyter nbextension enable --sys-prefix formgrader/main --section=tree \
 && jupyter serverextension enable --sys-prefix nbgrader.server_extensions.formgrader

# fix permissions as root
RUN fix-permissions  \
 && fix-permissions "${HOME}" \
 && fix-permissions "${CONDA_DIR}"

# ensure we start user sessions with nb_user/nb_uid 
USER "${NB_UID}"

WORKDIR "${HOME}"
