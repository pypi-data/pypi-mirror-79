import boto3

class Config:

    def __init__(self):
        self.awsProfile               = ""
        self.awsRegion                = ""
        self.awsTags                  = {}
        self.command                  = ""
        self.commandArguments         = ""
        self.tableLineSeparator       = True
        self.interactive              = False
        self.printResults             = False
        self.uploadChunkSizeMultipart = 10
        self.uploadThresholdMultipart = 100

    def awsTagsToFilter(self):
        if self.awsTags and len(self.awsTags) > 0:
            return True
        return False

    def botoSession(self):
        if not self.awsProfile and not self.awsRegion:
           session = boto3.Session()
        elif not self.awsProfile and     self.awsRegion:    
           session = boto3.Session(region_name=self.awsRegion)
        elif     self.awsProfile and not self.awsRegion:   
           session = boto3.Session(profile_name=self.awsProfile)
        else:
           session = boto3.Session(profile_name=self.awsProfile,region_name=self.awsRegion) 
        return session        

    

