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


def gen_puml(input_files, output_file):
    """
    Generate PlantUML file from C++ header file.
    """
    logging.debug(f"input_files: {input_files}")
    logging.debug(f"output_file: {output_file}")

    cmd = "hpp2plantuml "
    for i in input_files:
        cmd += f" -i {i} "
    cmd += f" -o {output_file} "

    logging.debug(f"cmd: {cmd}")
    ret = os.system(cmd)

    cmd = (
        "java -jar "
        + g_plantuml_jar
        + " -tsvg -o "
        + str(Path(output_file).resolve().parent)
        + "  "
        + output_file
    )
    logging.debug(f"cmd: {cmd}")
    ret |= os.system(cmd)

    if ret != 0:
        logging.error(f"Command failed with return code {ret}.")
        return False
    logging.debug(f"Command executed successfully.")

    return True


def handle_zmq():
    """
    Handle the zmq case.
    """
    common_path = os.path.join(workpath, "src")
    common_out_path = os.path.join(workpath, "0.study", "assets", "puml")
    os.makedirs(common_out_path, exist_ok=True)

    # gen
    input_files = glob.glob(os.path.join(common_path, "*.hpp"))
    remove_files = [
        "atomic_ptr.hpp",
        "fd.hpp",
        "polling_util.hpp",
        "atomic_counter.hpp",
        "mutex.hpp",
        "secure_allocator.hpp",
        "condition_variable.hpp",
        "yqueue.hpp",
        "stream_connecter_base.hpp",
    ]
    for f in remove_files:
        if os.path.join(common_path, f) in input_files:
            input_files.remove(os.path.join(common_path, f))

    output_file = common_out_path + "/zmq_overview_class.puml"
    gen_puml(input_files, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="gen puml from cpp header file")
    handle_zmq()
