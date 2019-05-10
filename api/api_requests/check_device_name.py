#
# Copyright (c) 2019 Cisco Systems
# Licensed under the MIT License
#

try:
    from .apic_access_module.dnaapicem import *
except:
    from apic_access_module.dnaapicem import *

import pprint

def phisical_topology():
    try:
        response = get(api='api/v1/topology/physical-topology', ver='v1')
    except (BaseException, Timeout) as e:
        return (False, str(e))
    if isinstance(response, dict) and 'errorCode' in response.keys():
        return (False, "APIC error: %s. Message: %s. Detail: %s" % (response['errorCode'], response['message'], response['detail']))
    return (True, response['nodes'])

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(phisical_topology())
