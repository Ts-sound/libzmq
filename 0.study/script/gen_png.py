#!/usr/bin/env python3

## python3.11

import argparse, os, glob, json, platform, logging
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s|%(filename)s] [%(funcName)s:%(lineno)d] %(message)s",
)


workpath = str(Path(__file__).resolve().parent.parent.parent)
logging.debug(f"workpath: {workpath}")


g_plantuml_jar = workpath + "/0.study/assets/plantuml-1.2025.4.jar"


def gen_png(puml_file: str):
    cmd = (
        "java -jar "
        + g_plantuml_jar
        + " -tpng -DPLANTUML_LIMIT_SIZE=16384 -o "
        + str(Path(puml_file).resolve().parent)
        + "  "
        + puml_file
    )
    logging.debug(f"cmd: {cmd}")
    os.system(cmd)


if __name__ == "__main__":
    gen_png(workpath + "/0.study/assets/puml/zeromq_class.puml")