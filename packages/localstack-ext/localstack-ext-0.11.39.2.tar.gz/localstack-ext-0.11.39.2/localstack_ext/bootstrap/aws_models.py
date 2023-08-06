from localstack.utils.aws import aws_models
UiqJH=super
UiqJV=None
UiqJS=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  UiqJH(LambdaLayer,self).__init__(arn)
  self.cwd=UiqJV
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,UiqJS,env=UiqJV):
  UiqJH(RDSDatabase,self).__init__(UiqJS,env=env)
 def name(self):
  return self.UiqJS.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,UiqJS,env=UiqJV):
  UiqJH(RDSCluster,self).__init__(UiqJS,env=env)
 def name(self):
  return self.UiqJS.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
