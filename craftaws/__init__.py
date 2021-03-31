from aws_cdk import (
    core,
    aws_ec2,
    aws_elasticloadbalancingv2 as elb,
    aws_elasticloadbalancingv2_targets as elb_targets,
    aws_lambda,
    aws_iam,
)

class network(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = aws_ec2.Vpc(self, "poc-gateway-vpc",
            cidr="10.254.0.0/16",
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(
                    name='poc-gateway-subnet',
                    subnet_type=aws_ec2.SubnetType.ISOLATED,
                    cidr_mask=24
                )
            ]
        )


class application_load_balancer(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, target_vpc:aws_ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        alb_security_group = aws_ec2.SecurityGroup(self, 'poc-gateway-sg',
            vpc=target_vpc
        )

        alb_security_group.add_ingress_rule(
            peer=aws_ec2.Peer.ipv4('10.254.0.0/16'),
            connection=aws_ec2.Port(
                protocol=aws_ec2.Protocol.TCP,
                string_representation="to allow from the vpc internal",
                from_port=443,
                to_port=443
            )
        )

        alb_security_group.add_ingress_rule(
            peer=aws_ec2.Peer.ipv4('10.254.0.0/16'),
            connection=aws_ec2.Port(
                protocol=aws_ec2.Protocol.TCP,
                string_representation="to allow from the vpc internal",
                from_port=80,
                to_port=80
            )
        )        
        
        alb = elb.ApplicationLoadBalancer(self, 'poc-gateway-alb',
            security_group=alb_security_group,
            vpc=target_vpc
        )

        poc_func_role = aws_iam.Role(self, 'poc-gateway-lambda-role',
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com")
        )
        poc_func_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaENIManagementAccess')
        )
        poc_func_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')
        )

        poc_func = aws_lambda.Function(self, 'poc-gateway-lambda-handler',
            function_name='poc-gateway-func-handler',
            handler='handler.do',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset('./lambda_func/req_handler'),
            role=poc_func_role,
            timeout=core.Duration.seconds(900),
            allow_public_subnet=False,
            vpc=target_vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.ISOLATED),
            environment={}
        )

        aws_lambda.Function(self, 'poc-gateway-lambda-tester',
            function_name='poc-gateway-func-tester',
            handler='tester.run',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset('./lambda_func/tester'),
            role=poc_func_role,
            timeout=core.Duration.seconds(900),
            allow_public_subnet=False,
            vpc=target_vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.ISOLATED),
            environment={
                'alb_endpoint': alb.load_balancer_dns_name
            }
        )

        target_group = elb.ApplicationTargetGroup(self, 'poc-gateway-tg',
            target_type=elb.TargetType.LAMBDA,
            targets=[elb_targets.LambdaTarget(poc_func)],
            vpc=target_vpc
        )

        alb.add_listener('http',
            open=False,
            port=80,
            default_target_groups=[target_group]
        )

