from localstack.utils.aws import aws_models
nHSUv=super
nHSUo=None
nHSUG=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  nHSUv(LambdaLayer,self).__init__(arn)
  self.cwd=nHSUo
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,nHSUG,env=nHSUo):
  nHSUv(RDSDatabase,self).__init__(nHSUG,env=env)
 def name(self):
  return self.nHSUG.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,nHSUG,env=nHSUo):
  nHSUv(RDSCluster,self).__init__(nHSUG,env=env)
 def name(self):
  return self.nHSUG.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
