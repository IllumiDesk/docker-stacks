#!/bin/bash

set -e

enable_instructor_extensions() (
    jupyter serverextension enable --sys-prefix nbgrader.server_extensions.assignment_list
    jupyter serverextension enable --sys-prefix nbgrader.server_extensions.course_list
    jupyter nbextension enable --sys-prefix course_list/main --section=tree
    jupyter nbextension enable --sys-prefix assignment_list/main --section=tree
)

enable_student_extensions() (
    jupyter serverextension enable --sys-prefix nbgrader.server_extensions.assignment_list
    jupyter nbextension enable --sys-prefix assignment_list/main --section=tree
)

if [[ "${USER_ROLE}" == "Instructor" ]] || [[ "${USER_ROLE}" == "TeachingAssistant" ]]; then
    echo "Enabling nbgrader extensions for Instructor or TeachingAssistant role"
    enable_instructor_extensions
fi

if [[ "${USER_ROLE}" == "Student" ]] || [[ "${USER_ROLE}" == "Learner" ]]; then
    echo "Enabling nbgrader extensions for Student/Learner role"
    enable_student_extensions
fi
