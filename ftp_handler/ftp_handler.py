
import io
import os
import logging
from dataclasses import dataclass

from django.conf import settings
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


@dataclass
class FTPHandler:
    ftp_server: str = None
    ftp_port: int = None
    ftp_username: str = None
    ftp_password: str = None
    is_sftp: bool = False
    remote_path: str = None
    private_key_path: str = None

    def send_to_ftp_server(self, file, filename: str = None, remote_path: str = None):
        if self.is_sftp:
            self.send_to_ftp_server_using_sftp_connection(file, filename=filename, remote_path=remote_path)
        else:
            self.send_to_ftp_server_using_ftp_connection(file, filename=filename, remote_path=remote_path)

    def send_to_ftp_server_using_ftp_connection(self, file, filename: str = None, remote_path: str = None):
        from ftplib import FTP, error_perm
        ftp = FTP()
        ftp.connect(self.ftp_server, self.ftp_port or 21)
        ftp.login(
            user=self.ftp_username,
            passwd=self.ftp_password
        )
        remote_path = remote_path or self.remote_path
        if remote_path:
            try:
                ftp.cwd(remote_path)
            except error_perm:
                ftp.mkd(remote_path)
                ftp.cwd(remote_path)
        if isinstance(file, io.IOBase):
            with open(file, 'rb') as opened_file:
                ftp.storbinary('STOR ' + filename or file.name, opened_file)
        elif isinstance(file, str):
            new_file = io.BytesIO()
            file_wrapper = io.TextIOWrapper(new_file, encoding='utf-8')
            file_wrapper.write(file)
            new_file.seek(0)
            ftp.storbinary('STOR ' + filename or "uploaded_file", new_file)
        elif isinstance(file, ContentFile):
            file = file.file
            file.seek(0)
            ftp.storbinary('STOR ' + filename or file.name, file)
        else:
            ftp.storbinary('STOR ' + filename or "uploaded_file", io.BytesIO(file))
        ftp.quit()

    def send_to_ftp_server_using_sftp_connection(self, file, filename: str = None, remote_path: str = None):
        import pysftp
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        if self.private_key_path:
            credentials = dict(
                private_key=os.path.join(settings.PROJECT_ROOT, self.private_key_path),
            )
        else:
            credentials = dict(
                password=self.ftp_password,
            )
        with pysftp.Connection(
            host=self.ftp_server,
            port=self.ftp_port or 22,
            username=self.ftp_username,
            **credentials,
            cnopts=cnopts,
        ) as sftp:
            logger.debug(f"current DIR : {sftp.pwd}")
            remote_path = remote_path or self.remote_path
            if remote_path:
                logger.debug(f"moving to DIR : '{remote_path}'...")
                try:
                    sftp.cwd(remote_path)  # Write the whole path+
                except IOError:
                    logger.debug(f"Dir not Found... creating it : '{remote_path}' ...")
                    sftp.mkdir(remote_path)
                    sftp.cwd(remote_path)
                logger.debug(f"moved to DIR : {remote_path} ...")
            logger.debug(f"putting file to DIR : {sftp.pwd} ...")
            if isinstance(file, io.IOBase):
                # sftp.putfo(io.BytesIO(file), filename or file.name, confirm=False)
                sftp.put(file)
            elif isinstance(file, str):
                sftp.putfo(io.StringIO(file), filename or "File", confirm=False)
            elif isinstance(file, ContentFile):
                file = file.file
                file.seek(0)
                sftp.putfo(file, filename or "File", confirm=False)
            else:
                sftp.putfo(io.BytesIO(file), filename or file.name, confirm=False)
