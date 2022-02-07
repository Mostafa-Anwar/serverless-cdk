from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ssm as ssm,
    core
)

class SecurityStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str,vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        self.lambda_sg = ec2.SecurityGroup(self, 'lambda-sg', 
            security_group_name='lambda-sg',
            vpc=vpc,
            description="SG for Lambda functions",
            allow_all_outbound=True
        )

        self.bastion_sg = ec2.SecurityGroup(self, 'bastionsg',
            security_group_name='bastion-sg',
            vpc=vpc,
            description="SG for Bastion Host",
            allow_all_outbound=True
        )

        self.bastion_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH Access")
        self.bastion_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443), "HTTPS Access")
        self.bastion_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "HTTP Access")




        redis_sg = ec2.SecurityGroup(self, 'redissg', 
            security_group_name='redis-sg',
            vpc=vpc,
            description="SG for Redis Cluster",
            allow_all_outbound=True
        )

        redis_sg.add_ingress_rule(self.lambda_sg, ec2.Port.tcp(6379), "Access for Lambda functions")


        lambda_role = iam.Role(self, 'lambdarole',
             assumed_by=iam.ServicePrincipal(service='lambda.amazonaws.com'),
             role_name='lambda-role',
             managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
             managed_policy_name='service-role/AWSLambdaVPCAccessExecutionRole'
            )]
        )

        lambda_role.add_to_policy(
            statement=iam.PolicyStatement(
                actions=['s3:*', 'rds:*'],
                resources=['*']
            )
        )


        # Export redis sg id, as Redis construct was only experimental at the time so it doesn't support the auto creation of the exports like the other stacks,
        # thus the need to create the low level export with CF output class
        core.CfnOutput(self, 'redis-export',
            export_name='redis-sg-export',
            value=redis_sg.security_group_id
        )


        #SSM Parameters
        ssm.StringParameter(self, 'lambdasg-param',
            parameter_name='/'+env_name+'/lambda-sg',
            string_value=self.lambda_sg.security_group_id
        )

        ssm.StringParameter(self, 'lambdarole-param-arn',
            parameter_name='/'+env_name+'/lambda-role-arn',
            string_value=lambda_role.role_arn
        )
        ssm.StringParameter(self, 'lambdarole-param-name',
            parameter_name='/'+env_name+'/lambda-role-name',
            string_value=lambda_role.role_name
        )
        