from argparse import ArgumentParser
from os import getenv
from json import loads
from .type import Service, ServiceSet, Machine
from .action import sync
from .logger import logger
from logging import StreamHandler, INFO

WEB_PROC = "web"

parser = ArgumentParser()
parser.add_argument("-f", "--deploy_f", default = "deploy.json")
parser.add_argument("-c", "--cluster", default = getenv("CLUSTER"))
parser.add_argument("-s", "--security_group", default = getenv("SECURITY_GROUP"))
parser.add_argument("-i", "--image", default = getenv("IMAGE"))
parser.add_argument("-a", "--subnet_a", default = getenv("SUBNET_A"))
parser.add_argument("-b", "--subnet_b", default = getenv("SUBNET_B"))
parser.add_argument("-r", "--role", default = getenv("ROLE"))
parser.add_argument("-n", "--namespace", default = "lonny-")
parser.add_argument("-t", "--target_group", default = getenv("TARGET_GROUP"))
parser.add_argument("-p", "--port", default = int(getenv("PORT", 8080)))
parser.add_argument("-e", "--env", action = "append", default = list())
parser.add_argument("--env_file", default = None)

logger.setLevel(INFO)
logger.addHandler(StreamHandler())

args = parser.parse_args()

def _parse_env_str(env_str):
    env_str = env_str.strip()
    split = env_str.split("=")
    if len(split) == 1:
        raise ValueError("Invalid env argument specified")
    return split[0], env_str[len(split[0]) + 1:]

def _env_vars():
    if args.env_file is not None:
        with open(args.env_file) as f:
            for line in f:
                if len(line.strip()) == 0:
                    continue
                yield _parse_env_str(line)
    for env in args.env:
        yield _parse_env_str(env)

def run():
    svc_set = ServiceSet(
        cluster = args.cluster,
        security_group = args.security_group,
        subnet_a = args.subnet_a,
        subnet_b = args.subnet_b,
        role = args.role,
        environment = { k : v for k,v in _env_vars() }
    )

    with open(args.deploy_f) as f:
        for name, svc_def in loads(f.read()).items():
            svc_set.add_svc(Service(
                name = f"{args.namespace}{name}",
                machine = Machine[svc_def["machine"]],
                image = args.image,
                instances = svc_def["instances"],
                log_group = svc_def.get("log_group"),
                target_group = args.target_group,
                port = args.port,
                entry = svc_def["entry"]
            ))

    sync(svc_set)