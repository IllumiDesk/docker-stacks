import errno
import os
import stat
import subprocess

from jupyter_core.paths import jupyter_data_dir


c = get_config()


c.NotebookApp.iopub_data_rate_limit = 1.0e10
c.NotebookApp.ip = "0.0.0.0"
c.NotebookApp.open_browser = False
c.NotebookApp.tornado_settings = {"headers": {"Content-Security-Policy": "frame-ancestors 'self' *"}}

c.NotebookApp.token = ""
c.NotebookApp.allow_root = True
c.NotebookApp.allow_origin = "*"

# https://github.com/jupyter/notebook/issues/3130
c.FileContentsManager.delete_to_trash = False

# Generate a self-signed certificate
if "GEN_CERT" in os.environ:
    dir_name = jupyter_data_dir()
    pem_file = os.path.join(dir_name, "notebook.pem")
    try:
        os.makedirs(dir_name)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(dir_name):
            pass
        else:
            raise
    # Generate a certificate if one doesn't exist on disk
    subprocess.check_call(
        [
            "openssl",
            "req",
            "-new",
            "-newkey",
            "rsa:2048",
            "-days",
            "365",
            "-nodes",
            "-x509",
            "-subj",
            "/C=XX/ST=XX/L=XX/O=generated/CN=generated",
            "-keyout",
            pem_file,
            "-out",
            pem_file,
        ]
    )
    # Restrict access to the file
    os.chmod(pem_file, stat.S_IRUSR | stat.S_IWUSR)
    c.NotebookApp.certfile = pem_file

# Change default umask for all subprocesses of the notebook server if set in
# the environment
if "NB_UMASK" in os.environ:
    os.umask(int(os.environ.get("NB_UMASK") or 8))
