from argparse import ArgumentParser
from importlib import import_module
from logging import getLogger, StreamHandler
from os import getenv
import sys

parser = ArgumentParser()
parser.add_argument("migrator")
parser.add_argument("-d", "--drop", action = "store_true")

def run():
    logger = getLogger()
    logger.addHandler(StreamHandler())
    logger.setLevel(getenv("LOG_LEVEL", "INFO"))

    sys.path.insert(0,"")
    args = parser.parse_args()
    module, migrator_ref = args.migrator.split(":")
    migrator = import_module(module).__getattribute__(migrator_ref)
    if args.drop:
        migrator.drop()
    migrator.run_pending()
    
if __name__ == "__main__":
    run()
