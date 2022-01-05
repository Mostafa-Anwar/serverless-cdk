#!/usr/bin/env python3
import os

from aws_cdk import core 

#from serv.serv_stack import ServStack
from stacks.vpc_stack import VPCStack
from stacks.security_stack import SecurityStack
from stacks.bastion_stack import BastionStack

app = core.App()

vpc_stack = VPCStack(app, 'vpc-stack')
security_stack = SecurityStack(app, 'security-stack', vpc=vpc_stack.vpc)
bastion_stack = BastionStack(app, 'bastion-stack', vpc=vpc_stack.vpc, sg=security_stack.bastion_sg)

app.synth()