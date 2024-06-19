from ensure_file import ensure_file as ef

import pathlib
import hashlib

VERSION = "1.0"

IMAGE_SAVE_PATH = pathlib.Path("./store")

SITE_NAME = "ImageBoard"
SITE_DESCRIPTION = "owo what's this"

VALID_ADMIN_PASSWORDS =[
    "gay"
]

# --== Code below this line should NOT be modified ==-- #

ef(IMAGE_SAVE_PATH, folder=True)
ef(IMAGE_SAVE_PATH / "global", folder=True)
ef(IMAGE_SAVE_PATH / "review", folder=True)

for i in range(len(VALID_ADMIN_PASSWORDS)):
    VALID_ADMIN_PASSWORDS[i] = hashlib.sha256(str.encode(VALID_ADMIN_PASSWORDS[i])).hexdigest()
