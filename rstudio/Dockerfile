FROM illumidesk/base-notebook:latest

ARG RSTUDIO_VERSION=1.3.1056

ENV RSTUDIO_VERSION="${RSTUDIO_VERSION}"
ENV PATH="/usr/sbin/:${PATH}"

USER root

# add rstudio gpg key
RUN gpg --keyserver keys.gnupg.net --recv-keys 3F32EE77E331692F

# download and install rstudio-server
RUN wget "https://download2.rstudio.org/server/$(lsb_release -sc)/amd64/rstudio-server-${RSTUDIO_VERSION}-amd64.deb" \
 && gdebi "rstudio-server-${RSTUDIO_VERSION}-amd64.deb" \
 && rm "rstudio-server-${RSTUDIO_VERSION}-amd64.deb"

# install requirements
USER "${NB_UID}"
WORKDIR "${HOME}"
COPY requirements.txt "${HOME}/requirements.txt"
RUN python3 -m pip install -r "${HOME}/requirements.txt" \
 && rm -f "${HOME}/requirements.txt"

USER root

# copy rstudio configuration
COPY rserver.conf /etc/rstudio/rserver.conf
COPY rsession.conf /etc/rstudio/rsession.conf

# Fix permissions on /etc/jupyter and /etc/rstudio as root
RUN fix-permissions /etc/rstudio/ \
 && fix-permissions /etc/jupyter/ \
 && fix-permissions "${HOME}"

USER "${NB_USER}"
