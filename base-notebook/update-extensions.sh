#!/bin/bash

install_instructor_extensions() (
    jupyter serverextension enable --sys-prefix nbgrader.server_extensions.assignment_list
    jupyter serverextension enable --sys-prefix nbgrader.server_extensions.course_list
    jupyter serverextension enable --sys-prefix nbgrader.server_extensions.course_list
    jupyter nbextension enable --sys-prefix course_list/main --section=tree
    jupyter nbextension enable --sys-prefix assignment_list/main --section=tree
)

install_student_extensions() (
    jupyter serverextension enable --sys-prefix nbgrader.server_extensions.assignment_list
    jupyter nbextension enable --sys-prefix assignment_list/main --section=tree
)

install_grader_extensions() (
    jupyter nbextension enable --sys-prefix create_assignment/main
    jupyter nbextension enable --sys-prefix formgrader/main --section=tree
    jupyter serverextension enable --sys-prefix nbgrader.server_extensions.formgrader
)

if [[ "${USER_ROLE}" == "Instructor" ]] || [[ "${USER_ROLE}" == "TeachingAssistant" ]]; then
    echo "Enabling nbgrader extensions for Instructor or TeachingAssistant role"
    install_instructor_extensions
fi

if [[ "${USER_ROLE}" == "Student" ]] || [[ "${USER_ROLE}" == "Learner" ]]; then
    echo "Enabling nbgrader extensions for Student/Learner role"
    install_student_extensions
fi

if [[ "${USER_ROLE}" == "Grader" ]]; then
    echo "Enabling nbgrader extensions for Grader role"
    install_grader_extensions
fi

