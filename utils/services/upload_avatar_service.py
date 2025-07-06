import os
from uuid import uuid4


def upload_to(instance, file: str) -> str:
    ext = file.split('.')[-1]
    return os.path.join(instance.last_name + instance.first_name, 'avatars', f'{uuid4()}.{ext}')
