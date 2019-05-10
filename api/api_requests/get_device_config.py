#
# Copyright (c) 2019 Cisco Systems
# Licensed under the MIT License
#

try:
    from .apic_access_module.dnaapicem import *
except:
    from apic_access_module.dnaapicem import *

import pprint

def apic_get_device_config(networkDeviceId):

    try:
        config = get(api='api/v1/network-device/' + networkDeviceId + '/config', ver='v1')
    except (BaseException, Timeout) as e:
        return (False, str(e))
    if isinstance(config, dict) and 'errorCode' in config.keys():
        return (False, "DNA-C error: %s. Message: %s. Detail: %s" % (config['errorCode'], config['message'], config['detail']))
    return (True, config)

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    networkDeviceId = '28ff0a0a-c383-4257-a047-54eb5fdf67d5'
    pp.pprint(apic_get_device_config(networkDeviceId))
