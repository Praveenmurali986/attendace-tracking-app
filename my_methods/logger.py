
import logging
from datetime import datetime
import os


def log(username):
    LOG_Dir=os.path.join('log',username)

    CURRENT_TIME_STAMP=f"{datetime.now().strftime('%Y-%m-%d')}"

    LOG_FILE_NAME=f"log_{CURRENT_TIME_STAMP}.log"

    os.makedirs(LOG_Dir,exist_ok=True)

    LOG_FILE_PATH=os.path.join(LOG_Dir,LOG_FILE_NAME)

    logging.basicConfig(filename=LOG_FILE_PATH,
    filemode='w+',
    format='[%(asctime)s] %(name)s-%(levelname)s-%(message)s',
    level=logging.INFO
    )
    return logging
