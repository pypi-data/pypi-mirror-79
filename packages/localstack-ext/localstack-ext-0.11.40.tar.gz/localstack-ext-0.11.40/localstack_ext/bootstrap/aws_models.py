from localstack.utils.aws import aws_models
GVKkP=super
GVKkb=None
GVKka=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  GVKkP(LambdaLayer,self).__init__(arn)
  self.cwd=GVKkb
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,GVKka,env=GVKkb):
  GVKkP(RDSDatabase,self).__init__(GVKka,env=env)
 def name(self):
  return self.GVKka.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,GVKka,env=GVKkb):
  GVKkP(RDSCluster,self).__init__(GVKka,env=env)
 def name(self):
  return self.GVKka.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
