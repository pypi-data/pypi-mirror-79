import boto3
import pydash

from infra_buddy.utility import print_utility, waitfor

from infra_buddy.aws.cloudformation import CloudFormationBuddy


class ECSBuddy(object):
    def __init__(self, deploy_ctx):
        # type: (DeployContext) -> None
        super(ECSBuddy, self).__init__()
        self.deploy_ctx = deploy_ctx
        self.client = boto3.client('ecs', region_name=self.deploy_ctx.region)
        cf = CloudFormationBuddy(deploy_ctx)
        ecs_cluster_export_key = "{}-ECSCluster".format(self.deploy_ctx.cluster_stack_name)
        self.cluster = self._wait_for_export(cf=cf, fully_qualified_param_name=ecs_cluster_export_key)
        ecs_service_export_key = "{}-ECSService".format(self.deploy_ctx.stack_name)
        self.ecs_service = self._wait_for_export(cf=cf, fully_qualified_param_name=ecs_service_export_key)
        ecs_task_family_export_key = "{}-ECSTaskFamily".format(self.deploy_ctx.stack_name)
        self.ecs_task_family = self._wait_for_export(cf=cf, fully_qualified_param_name=ecs_task_family_export_key)
        ecs_task_execution_role_export_key = "{}-ECSTaskExecutionRole".format(self.deploy_ctx.stack_name)
        self.ecs_task_execution_role = self._wait_for_export(cf=cf, fully_qualified_param_name=ecs_task_execution_role_export_key)
        ecs_task_role_export_key = "{}-ECSTaskRole".format(self.deploy_ctx.stack_name)
        self.ecs_task_role = self._wait_for_export(cf=cf, fully_qualified_param_name=ecs_task_role_export_key)
        self.task_definition_description = None
        self.new_image = None

    @classmethod
    def _wait_for_export(cls, cf, fully_qualified_param_name):
        # we are seeing an issue where immediately after stack create the export values are not
        # immediately available
        value = waitfor.waitfor(
            function_pointer=cf.get_export_value,
            expected_result=None,
            interval_seconds=2,
            max_attempts=5,
            negate=True,
            args={"fully_qualified_param_name": fully_qualified_param_name},
            exception=False
        )

        print_utility.info("[wait_for_export] {}={}".format(fully_qualified_param_name, value))
        return value

    def set_container_image(self, location, tag):
        self.new_image = "{location}:{tag}".format(location=location, tag=tag)

    def requires_update(self):
        if not self.new_image:
            print_utility.warn("Checking for ECS update without registering new image ")
            return False
        if not self.ecs_task_family:
            print_utility.warn("No ECS Task family found - assuming first deploy of stack and skipping ECS update")
            return False
        self._describe_task_definition()
        existing = pydash.get(self.task_definition_description, "containerDefinitions[0].image")
        print_utility.info("ECS task existing image - {}".format(existing))
        print_utility.info("ECS task desired image - {}".format(self.new_image))
        return existing != self.new_image

    def perform_update(self):
        self._describe_task_definition(refresh=True)
        new_task_def = {
            'family': self.task_definition_description['family'],
            'containerDefinitions': self.task_definition_description['containerDefinitions'],
            'volumes': self.task_definition_description['volumes']
        }
        if 'networkMode' in self.task_definition_description:
            new_task_def['networkMode'] = self.task_definition_description['networkMode']
        new_task_def['containerDefinitions'][0]['image'] = self.new_image

        using_fargate = self.deploy_ctx.get('USE_FARGATE') == 'true'

        ctx_memory = self.deploy_ctx.get('TASK_MEMORY')
        if ctx_memory:
            new_task_def['containerDefinitions'][0]['memory'] = ctx_memory

        if 'TASK_SOFT_MEMORY' in self.deploy_ctx and self.deploy_ctx['TASK_SOFT_MEMORY']:
            new_task_def['containerDefinitions'][0]['memoryReservation'] = self.deploy_ctx['TASK_SOFT_MEMORY']

        ctx_cpu = self.deploy_ctx.get('TASK_CPU')
        if ctx_cpu:
            new_task_def['containerDefinitions'][0]['cpu'] = ctx_cpu

        # set at the task level for fargate definitions
        if using_fargate:
            first_container = new_task_def['containerDefinitions'][0]
            new_task_def['requiresCompatibilities'] = ['FARGATE']
            new_cpu = ctx_cpu or first_container.get('cpu')
            if new_cpu:
                new_task_def['cpu'] = str(new_cpu)  # not sure if this is right but AWS says it should be str

            new_memory = ctx_memory or first_container.get('memoryReservation')
            if new_memory:
                new_task_def['memory'] = str(new_memory)  # not sure if this is right but AWS says it should be str

        if self.ecs_task_execution_role:
            new_task_def['executionRoleArn'] = self.ecs_task_execution_role
        if self.ecs_task_role:
            new_task_def['taskRoleArn'] = self.ecs_task_role

        for k, v in self.deploy_ctx.items():
            print_utility.info('[deploy_ctx] {} = {}'.format(k, repr(v)))

        for k, v in new_task_def.items():
            print_utility.info('[new_task_def] {} = {}'.format(k, repr(v)))

        updated_task_definition = self.client.register_task_definition(**new_task_def)['taskDefinition']
        new_task_def_arn = updated_task_definition['taskDefinitionArn']

        self.deploy_ctx.notify_event(
            title="Update of ecs service {service} started".format(service=self.ecs_service),
            type="success")
        self.client.update_service(
            cluster=self.cluster,
            service=self.ecs_service,
            taskDefinition=new_task_def_arn)
        waiter = self.client.get_waiter('services_stable')
        success = True
        try:
            waiter.wait(
                cluster=self.cluster,
                services=[self.ecs_service]
            )
        except Exception as e:
            success = False
            print_utility.error("Error waiting for service to stabilize - {}".format(e.message), raise_exception=True)
        finally:
            self.deploy_ctx.notify_event(
                title="Update of ecs service {service} completed".format(service=self.ecs_service,
                                                                         success="Success" if success else "Failed"),
                type="success" if success else "error")

    def _describe_task_definition(self, refresh=False):
        if self.task_definition_description and not refresh:
            return
        self.task_definition_description = self.client.describe_task_definition(taskDefinition=self.ecs_task_family)[
            'taskDefinition']
