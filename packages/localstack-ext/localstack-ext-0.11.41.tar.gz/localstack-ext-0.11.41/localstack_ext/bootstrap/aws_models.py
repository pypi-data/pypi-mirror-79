from localstack.utils.aws import aws_models
hFztD=super
hFztm=None
hFztC=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  hFztD(LambdaLayer,self).__init__(arn)
  self.cwd=hFztm
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,hFztC,env=hFztm):
  hFztD(RDSDatabase,self).__init__(hFztC,env=env)
 def name(self):
  return self.hFztC.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,hFztC,env=hFztm):
  hFztD(RDSCluster,self).__init__(hFztC,env=env)
 def name(self):
  return self.hFztC.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
