#!/usr/bin/env python3
import os

from aws_cdk import core 

#from serv.serv_stack import ServStack
from stacks.vpc_stack import VPCStack

app = core.App()

vpc_stack = VPCStack(app, 'vpc')
app.synth()