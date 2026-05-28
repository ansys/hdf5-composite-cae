import logging

file_formatter = logging.Formatter("[%(asctime)s/%(levelname)5.5s]  %(message)s")
stream_formatter = logging.Formatter(
    "[%(asctime)s/%(levelname)5.5s]  %(message)s", datefmt="%H:%M:%S"
)
file_handler = logging.FileHandler("build.log")
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_formatter)
stream_handler.setLevel(logging.DEBUG)

log = logging.getLogger(__name__)

log.addHandler(file_handler)
log.addHandler(stream_handler)
log.setLevel(logging.DEBUG)
