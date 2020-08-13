ARG BASE_IMAGE=illumidesk/base-notebook:latest
FROM $BASE_IMAGE

ARG USER_ROLE=Instructor

USER root

# enable nbgrader instructor extensions (assignment/course list)
RUN jupyter serverextension enable --sys-prefix nbgrader.server_extensions.assignment_list \
 && jupyter serverextension enable --sys-prefix nbgrader.server_extensions.course_list \
 && jupyter serverextension enable --sys-prefix nbgrader.server_extensions.course_list \
 && jupyter nbextension enable --sys-prefix course_list/main --section=tree \
 && jupyter nbextension enable --sys-prefix assignment_list/main --section=tree

# fix permissions as root
RUN fix-permissions  \
 && fix-permissions "${HOME}" \
 && fix-permissions "${CONDA_DIR}"

USER "${NB_UID}"

WORKDIR "${HOME}"
