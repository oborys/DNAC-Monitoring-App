try:
    from .apic_access_module.dnaapicem import *
except:
    from apic_access_module.dnaapicem import *

from requests.exceptions import Timeout
import pprint

def apic_devices_info():

    try:
        response = get(api='api/v1/network-device', ver='v1')
    except (BaseException, Timeout) as e:
        return (False, str(e))
    else:
        if isinstance(response, dict) and 'errorCode' in response.keys():
            return (False, "DNA-C error: %s. Message: %s. Detail: %s" % (response['errorCode'], response['message'], response['detail']))
        return (True, response)
        #return (True, response['networkDeviceManagementInfo'])

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(devices_info_api())
