import json
import os
from django.conf import settings

def read_json_file(file_name):
    my_static_file = os.path.join(settings.STATIC_ROOT, file_name)
    with open(my_static_file) as f:
        return json.load(f)
