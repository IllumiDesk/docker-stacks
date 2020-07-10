ARG BASE_IMAGE=illumidesk/base-notebook
FROM $BASE_IMAGE

ARG USER_ROLE=Grader
ARG NB_UID=10001
ARG NB_USER=grader-{{course_id}}

USER $NB_UID

WORKDIR /home/$NB_USER

RUN jupyter nbextension enable --sys-prefix create_assignment/main \
 && jupyter nbextension enable --sys-prefix formgrader/main --section=tree \
 && jupyter serverextension enable --sys-prefix nbgrader.server_extensions.formgrader
