from ensure_file import ensure_file as ef

import pathlib
import hashlib

IMAGE_SAVE_PATH = pathlib.Path("./store")

SITE_NAME = "ImageBoard"
SITE_DESCRIPTION = "owo what's this"

VALIDD_ADMONI_PASSWORDSD =[
    "gay"
]

# --== Code below this line should NOT be modified ==-- #

ef(IMAGE_SAVE_PATH, folder=True)
ef(IMAGE_SAVE_PATH / "global", folder=True)
ef(IMAGE_SAVE_PATH / "review", folder=True)

for i in range(len(VALIDD_ADMONI_PASSWORDSD)):
    VALIDD_ADMONI_PASSWORDSD[i] = hashlib.sha256(str.encode(VALIDD_ADMONI_PASSWORDSD[i])).hexdigest()
