import io
import uuid
from plynx.utils.remote import get_driver


def get_file_stream(file_path, preview=False, file_type=None):
    content = get_driver().get_contents_handler(file_path)
    content_stream = io.BytesIO()
    content.get_contents_to_file(content_stream)
    content_stream.seek(0)
    return content_stream


def upload_file_stream(fp, file_path=None, seek=True):
    if seek:
        fp.seek(0)
    if file_path is None:
        file_path = str(uuid.uuid1())
    content = get_driver().get_contents_handler(file_path)
    content.set_contents_from_file(fp)
    return file_path


def remove(file_path):
    content = get_driver().get_contents_handler(file_path)
    content.remove()
