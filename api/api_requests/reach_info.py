try:
    from .apic_access_module.dnaapicem import get
except:
    from apic_access_module.dnaapicem import get

from requests.exceptions import Timeout
import pprint

def apic_reach_info():

    try:
        response = get(api='api/v1/network-device', ver='v1')
    except (BaseException, Timeout) as e:
        return (False, str(e))
    else:
        if isinstance(response, dict) and 'errorCode' in response.keys():
            return (False, "DNA-C error: %s. Message: %s. Detail: %s" % (response['errorCode'], response['message'], response['detail']))
        return (True, response)

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(reach_info())

#APIC-EM Reach info

# {
#    "response":[
#       {
#          "discoveryId":"1",
#          "mgmtIp":"10.2.2.2",
#          "password":"*****",
#          "enablePassword":"*****",
#          "snmpCommunity":"*****",
#          "reachabilityStatus":"UNREACHABLE",
#          "reachabilityFailureReason":"DEV_UNREACHED",
#          "discoveryStartTime":"2016-11-18 06:53:47.697",
#          "id":"6ce631db-9212-4587-867f-b8f3aed1702d"
#       },
#       {
#          "discoveryId":"1",
#          "mgmtIp":"10.2.2.1",
#          "password":"*****",
#          "enablePassword":"*****",
#          "snmpCommunity":"*****",
#          "reachabilityStatus":"UNREACHABLE",
#          "reachabilityFailureReason":"DEV_UNREACHED",
#          "discoveryStartTime":"2016-11-18 06:53:47.697",
#          "id":"0dd240fd-5cca-4774-a801-9f1c04edcc70"
#       },
#       {
#          "discoveryId":"1",
#          "mgmtIp":"10.2.1.17",
#          "password":"*****",
#          "enablePassword":"*****",
#          "snmpCommunity":"*****",
#          "reachabilityStatus":"UNREACHABLE",
#          "reachabilityFailureReason":"DEV_UNREACHED",
#          "discoveryStartTime":"2016-11-18 06:53:47.697",
#          "id":"26450a30-57d8-4b56-b8f1-6fc535d67645"
#       },
#       {
#          "discoveryId":"95",
#          "mgmtIp":"218.1.100.100",
#          "password":"*****",
#          "enablePassword":"*****",
#          "snmpCommunity":"*****",
#          "reachabilityStatus":"UNREACHABLE",
#          "reachabilityFailureReason":"DEV_UNREACHED",
#          "discoveryStartTime":"2016-11-18 06:57:06.765",
#          "id":"d337811b-d371-444c-a49f-9e2791f955b4"
#       },
#       {
#          "discoveryId":"144",
#          "mgmtIp":"165.10.1.39",
#          "password":"*****",
#          "enablePassword":"*****",
#          "snmpCommunity":"*****",
#          "reachabilityStatus":"UNREACHABLE",
#          "reachabilityFailureReason":"DEV_UNREACHED",
#          "discoveryStartTime":"2016-11-18 08:00:33.866",
#          "id":"8dbd8068-1091-4cde-8cf5-d1b58dc5c9c7"
#       },
#       {
#          "discoveryId":"21",
#          "mgmtIp":"10.255.1.5",
#          "password":"*****",
#          "enablePassword":"*****",
#          "snmpCommunity":"*****",
#          "reachabilityStatus":"UNREACHABLE",
#          "reachabilityFailureReason":"DEV_UNREACHED",
#          "discoveryStartTime":"2016-11-18 22:51:31.65",
#          "id":"c8ed3e49-5eeb-4dee-b120-edeb179c8394"
#       },
#       {
#          "discoveryId":"21",
#          "mgmtIp":"10.1.10.1",
#          "password":"*****",
#          "enablePassword":"*****",
#          "snmpCommunity":"*****",
#          "reachabilityStatus":"UNREACHABLE",
#          "reachabilityFailureReason":"DEV_UNREACHED",
#          "discoveryStartTime":"2016-11-18 22:51:31.65",
#          "id":"1b329f52-95eb-44ad-9314-55932162ab86"
#       },
#       {
#          "discoveryId":"21",
#          "mgmtIp":"10.1.7.1",
#          "password":"*****",
#          "enablePassword":"*****",
#          "snmpCommunity":"*****",
#          "reachabilityStatus":"UNREACHABLE",
#          "reachabilityFailureReason":"DEV_UNREACHED",
#          "discoveryStartTime":"2016-11-18 22:51:31.65",
#          "id":"30d39b18-9ada-4148-ad6c-2ee20975b845"
#       },
#       {
#          "discoveryId":"21",
#          "mgmtIp":"10.1.11.1",
#          "password":"*****",
#          "enablePassword":"*****",
#          "snmpCommunity":"*****",
#          "reachabilityStatus":"UNREACHABLE",
#          "reachabilityFailureReason":"DEV_UNREACHED",
#          "discoveryStartTime":"2016-11-18 22:51:31.65",
#          "id":"4af8bf34-295f-46f4-97b7-0a2d2ea4cf22"
#       },
#       {
#          "discoveryId":"21",
#          "mgmtIp":"10.1.2.1",
#          "password":"*****",
#          "enablePassword":"*****",
#          "snmpCommunity":"*****",
#          "reachabilityStatus":"UNREACHABLE",
#          "reachabilityFailureReason":"DEV_UNREACHED",
#          "discoveryStartTime":"2016-11-18 22:51:31.65",
#          "id":"9712ab62-6140-43fd-b1ee-1b07d1fb67d7"
#       },
#       {
#          "discoveryId":"21",
#          "mgmtIp":"10.1.4.2",
#          "password":"*****",
#          "enablePassword":"*****",
#          "snmpCommunity":"*****",
#          "reachabilityStatus":"UNREACHABLE",
#          "reachabilityFailureReason":"DEV_UNREACHED",
#          "discoveryStartTime":"2016-11-18 22:51:31.65",
#          "id":"55450140-de19-47b5-ae80-bfd741b23fd9"
#       },
#       {
#          "discoveryId":"21",
#          "mgmtIp":"10.1.12.1",
#          "password":"*****",
#          "enablePassword":"*****",
#          "snmpCommunity":"*****",
#          "reachabilityStatus":"UNREACHABLE",
#          "reachabilityFailureReason":"DEV_UNREACHED",
#          "discoveryStartTime":"2016-11-18 22:51:31.65",
#          "id":"5b5ea8da-8c23-486a-b95e-7429684d25fc"
#       },
#       {
#          "discoveryId":"21",
#          "mgmtIp":"10.1.14.2",
#          "password":"*****",
#          "enablePassword":"*****",
#          "snmpCommunity":"*****",
#          "reachabilityStatus":"UNREACHABLE",
#          "reachabilityFailureReason":"DEV_UNREACHED",
#          "discoveryStartTime":"2016-11-18 22:51:31.65",
#          "id":"ae19cd21-1b26-4f58-8ccd-d265deabb6c3"
#       }
#    ],
#    "version":"1.0"
# }
