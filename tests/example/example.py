import logging
from dataclasses import dataclass

from django.core.files.base import ContentFile

from ftp_handler.ftp_handler import FTPHandler

logger = logging.getLogger(__name__)


@dataclass
class YourFTPHandler(FTPHandler):
    ftp_server = "sftp.test.com"
    ftp_port = 22
    ftp_username = 'Username'
    ftp_password = 'Password'
    is_sftp = True
    remote_path = 'Remote path of the directory'


def send_document_on_ftp_with_inheritance(file: ContentFile, filename):
    content_file = file
    handler = YourFTPHandler()
    try:
        handler.send_to_ftp_server(
            content_file,
            filename=filename
        )
        logger.info(f"{filename} successfully uploaded on {handler.ftp_server} server.")
    except Exception as exc:
        logger.exception(f"{filename} not uploaded on {handler.ftp_server} server.")
        raise exc


def send_document_on_ftp_without_inheritance(file: ContentFile, filename):
    content_file = file
    handler = FTPHandler(
        ftp_server="sftp.test.com",
        ftp_port=22,
        ftp_username='Username',
        ftp_password='Password',
        is_sftp=True,
        remote_path='Remote path of the directory'
    )
    try:
        handler.send_to_ftp_server(
            content_file,
            filename=filename
        )
        logger.info(f"{filename} successfully uploaded on {handler.ftp_server} server.")
    except Exception as exc:
        logger.exception(f"{filename} not uploaded on {handler.ftp_server} server.")
        raise exc
