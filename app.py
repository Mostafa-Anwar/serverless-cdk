#!/usr/bin/env python3
import os

from aws_cdk import core 

#from serv.serv_stack import ServStack
from stacks.vpc_stack import VPCStack
from stacks.security_stack import SecurityStack

app = core.App()

vpc_stack = VPCStack(app, 'vpc')
security_stack = SecurityStack(app, 'security-stack', vpc=vpc_stack.vpc)

app.synth()