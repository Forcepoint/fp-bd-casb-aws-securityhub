ONE_DAY_IN_SEC = 86400
SCHEMA_VERSION = "2018-10-08"
NOT_APPLICABLE = "N/A"
ASFF_TYPE = "Unusual Behaviors/Application/ForcepointCASB"
BLANK = "blank"
OTHER = "Other"
SAAS_SECURITY_GATEWAY = "SaaS Security Gateway"
RESOURCES_OTHER_FIELDS_LST = [
    "Name",
    "suid",
    "suser",
    "duser",
    "act",
    "cat",
    "cs1",
    "app",
    "deviceFacility",
    "deviceProcessName",
    "dpriv",
    "end",
    "externalId",
    "fsize",
    "msg",
    "proto",
    "reason",
    "request",
    "requestClientApplication",
    "rt",
    "sourceServiceName",
    "cs2",
    "cs3",
    "cs5",
    "cs6",
    "AD.ThreatRadarCategory",
    "AD.TORNetworks",
    "AD.MaliciousIPs",
    "AD.AnonymousProxies",
    "AD.IPChain",
    "AD.IPOrigin",
    "AD.samAccountName",
    "dproc",
    "flexString1",
    "flexString2",
    "cn1",
    "duid",
    "oldFileId",
    "oldFileName",
    "fname",
    "dhost",
    "dvc",
    "dvchost",
    "destinationProcessName",
    "record",
    "cs4",
]
BATCH_LOG_FILE_NAME = "casb-siem-aws-missed.log"
STREAM_LOG_FILE_NAME = "casb-siem-aws.log"
CEF_EXT = ".cef"
AWS_SECURITYHUB_BATCH_LIMIT = 100
AWS_LIMIT_TIME_IN_DAYS = 90
DEFAULT_INSIGHTS_FILE = "insights.json"
INSIGHTS_ARNS_FILE = "insights_arns.json"
CLOUDFORMATION_STACK_NAME = "SecurityHubEnabled"
CLOUDFORMATION_STACK_TEMPLATE_FILE = "cloudFormation-stack.json"
MAX_RETRIES = 60  # equivalent to 5 minutes (waiting 5 seconds per attempt)
CRITICAL = "CRITICAL"
HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"
INFORMATIONAL = "INFORMATIONAL"
