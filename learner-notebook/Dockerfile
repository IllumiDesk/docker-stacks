ARG BASE_IMAGE=illumidesk/base-notebook
FROM $BASE_IMAGE

ARG USER_ROLE=Learner

USER $NB_UID

RUN jupyter nbextension enable --sys-prefix assignment_list/main --section=tree \
 && jupyter serverextension enable --sys-prefix nbgrader.server_extensions.assignment_list

WORKDIR /home/$NB_USER
