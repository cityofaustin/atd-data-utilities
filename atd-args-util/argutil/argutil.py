"""
Utility to create an argparser with predefined arguments. 
https://docs.python.org/3/library/argparse.html#module-argparse
"""
import argparse
from ._arguments import *

def get_parser(prog, description, *args):
    """
    Return a parser with the specified arguments. Each arg
    in *args must be defined in ARGUMENTS.
    """
    parser = argparse.ArgumentParser(prog=prog, description=description)

    for arg_name in args:
        arg_def = ARGUMENTS[arg_name]

        if arg_def.get("flag"):
            parser.add_argument(arg_name, arg_def.pop("flag"), **arg_def)
        else:
            parser.add_argument(arg_name, **arg_def)

    return parser


if __name__ == "__main__":
    # tests
    name = "fake_program.py"
    description = "Fake program which does nothing useful."

    parser = get_parser(
        name,
        description,
        "dataset",
        "device_type",
        "app_name",
        "eval_type",
        "--destination",
        "--replace",
        "--json",
        "--last_run_date"
    )
    
    print(
        parser.parse_args([
            "cameras",
            "gridsmart",
            "data_tracker_prod",
            "traffic_signal",
            "-d",
            "socrata",
            "--replace",
            "--json",
            "--last_run_date",
            "1535997869"
        ])
    )