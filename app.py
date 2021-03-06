#!/usr/bin/env python3
import os

from aws_cdk import core 

#from serv.serv_stack import ServStack
from stacks.vpc_stack      import VPCStack
from stacks.security_stack import SecurityStack
from stacks.bastion_stack  import BastionStack
from stacks.kms_stack      import KMSStack
from stacks.s3_stack       import S3Stack
from stacks.rds_stack      import RDSStack
from stacks.redis_stack    import RedisStack

app = core.App()

vpc_stack = VPCStack(app, 'vpc-stack')
security_stack = SecurityStack(app, 'security-stack', vpc=vpc_stack.vpc)
bastion_stack = BastionStack(app, 'bastion-stack', vpc=vpc_stack.vpc, sg=security_stack.bastion_sg)
kms_stack = KMSStack(app, 'kms-stack')
s3_stack = S3Stack(app, 's3-stack')
rds_stack = RDSStack(app, 'rds-stack', vpc=vpc_stack.vpc, lambdasg=security_stack.lambda_sg, bastionsg=security_stack.bastion_sg, kmskey=kms_stack.kms_rds)

redis_stack = RedisStack(app, 'redis-stack', vpc=vpc_stack.vpc, redissg=core.Fn.import_value('redis-sg-export'))
redis_stack.add_dependency(security_stack)

app.synth()