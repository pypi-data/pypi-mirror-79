from .logger import logger
import boto3

client_ecs = boto3.client("ecs")
my_session = boto3.session.Session()

def _get_service_arns(*, cluster, next_token = None):
    data = client_ecs.list_services( ** dict(
        cluster = cluster,
        ** dict() if next_token is None else dict(nextToken = next_token)
    ))
    for arn in data["serviceArns"]:
        yield arn
    next_token = data.get("nextToken")
    if next_token is None:
        return
    for arn in _get_service_arns(cluster = cluster, next_token = next_token):
        yield arn

def _get_services(*, cluster):
    for arn in _get_service_arns(cluster = cluster):
        yield client_ecs.describe_services(
            cluster = cluster, 
            services = [arn]
        )["services"][0]

def _delete_service(*, cluster, name):
    client_ecs.update_service(cluster = cluster, service = name, desiredCount = 0)
    client_ecs.delete_service(cluster = cluster, service = name)

def _update_service(*, svc_set, svc, task_definition_arn):
    client_ecs.update_service(
        cluster = svc_set.cluster,
        service = svc.name,
        desiredCount = svc.instances,
        taskDefinition = task_definition_arn,
        forceNewDeployment = True
    )

def _create_service(*, svc_set, svc, task_definition_arn):
    client_ecs.create_service(
        cluster = svc_set.cluster,
        serviceName = svc.name,
        launchType = "FARGATE",
        taskDefinition = task_definition_arn,
        loadBalancers = list() if svc.target_group is None else [dict(
            targetGroupArn = svc.target_group,
            containerName = svc.name,
            containerPort = svc.port
        )],
        desiredCount = svc.instances,
        networkConfiguration = dict(
            awsvpcConfiguration = dict(
                subnets = [svc_set.subnet_a, svc_set.subnet_b],
                securityGroups = [svc_set.security_group],
                assignPublicIp = "ENABLED"
            )
        )
    )

def _register_task_definition(*, svc_set, svc):
    return client_ecs.register_task_definition(
        family = svc.name,
        taskRoleArn = svc_set.role,
        executionRoleArn = svc_set.role,
        networkMode = "awsvpc",
        requiresCompatibilities = ["FARGATE"],
        cpu = str(svc.machine.value[0]),
        memory = str(svc.machine.value[1]),
        containerDefinitions = [dict(
            name = svc.name,
            entryPoint = svc.entry,
            logConfiguration = dict(
                logDriver = "awslogs",
                options = {
                    "awslogs-group": svc.log_group,
                    "awslogs-region": my_session.region_name,
                    "awslogs-stream-prefix": svc.name
                }
            ),
            image = svc.image,
            portMappings = list() if svc.target_group is None else [dict(
                containerPort = svc.port,
                hostPort = svc.port
            )],
            environment = [
                dict(name = k, value = v) for k,v in svc_set.environment.items()
            ]
        )]
    )["taskDefinition"]["taskDefinitionArn"]

def sync(svc_set):
    service_map = { x["serviceName"] : x for x in _get_services(cluster = svc_set.cluster) }
    for name, service in service_map.items():
        if name not in svc_set.svcs:
            logger.info(f"Service: {name} is not specified in most recent configuration. Destroying.")
            _delete_service(cluster = svc_set.cluster, name = name)

    for svc in svc_set.svcs.values():
        logger.info(f"Registering a task definition for service: {svc.name}.")
        task_def_arn = _register_task_definition(
            svc_set = svc_set,
            svc = svc
        )
        if svc.name in service_map:
            logger.info(f"Service: {svc.name} already exists. Updating.")
            _update_service(
                svc = svc,
                svc_set = svc_set,
                task_definition_arn = task_def_arn,
            )
        else:
            logger.info(f"Service: {svc.name} doesn't exist. Creating.")
            _create_service(
                svc = svc,
                svc_set = svc_set,
                task_definition_arn = task_def_arn
            )