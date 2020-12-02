TEST_RECORD_1 = {
    "Vendor": "Forcepoint CASB",
    "Product": "SaaS Security Gateway",
    "Version": "1.0",
    "SignatureID": "250677275138",
    "Name": "login",
    "Severity": "9",
    "CEFVersion": "0",
    "act": "Block",
    "app": "Office Apps",
    "cat": "Block Access to personal Office365/Block Access to personal Office365",
    "destinationServiceName": '"Office365"',
    "deviceExternalId": "2fe1d47db",
    "deviceFacility": "true",
    "deviceProcessName": '""',
    "dpriv": "User",
    "dst": "40.90.23.111",
    "dvc": "10.1.4.11",
    "dvchost": "my.skyfence.com",
    "end": "1569171970000",
    "externalId": "787",
    "fsize": "0",
    "msg": "//France/United States/",
    "outcome": "Success",
    "proto": "Office Apps",
    "reason": "login",
    "request": "https://login.live.com/rst2.srf",
    "requestClientApplication": 'Desktop/Windows 10/"mozilla/4.0 (compatible; msie 6.0; windows nt 10.0; win64; .net4.0c; .net4.0e; idcrl 14.10.0.15063.0.0; idcrl-cfg 16.0.26889.0; app svchost.exe, 10.0.15063.0, {df60e2df-88ad})"',
    "rt": "1569171970000",
    "sourceServiceName": "Managed",
    "src": "192.168.122.178",
    "start": "1569171970000",
    "suser": "02v",
    "cs5": "false",
    "dproc": "Unknown",
    "suid": "02vt",
    "cn1": "null",
    "AD.IPOrigin": "External",
    "AD.samAccountName": "02vta",
}
FIELDS_LST = ["Name", "suid", "suser", "duser"]
USER_CONFIG_SEVERITY_LIST = [8, 10]
USER_CONFIG_ACTION_LIST = ["block", "monitor"]
USER_CONFIG_PRODUCT_LIST = [
    "saas security gateway",
    "casb incidents",
    "casb admin audit log",
    "cloud service monitoring",
]
