try:
    from .apic_access_module.dnaapicem import *
except:
    from apic_access_module.dnaapicem import *

import pprint


def apic_path_trace(source_ip, destination_ip):
    flow = []

    path = {"sourceIP": source_ip, "destIP": destination_ip}

    try:
        response = post(api="flow-analysis", data=path, ver='v1')
    except:
        print("Something wrong with POST /host request!")
    flow.append(response)
    flowAnalysisId = flow[0]["flowAnalysisId"]


    try:
        response_get = get(api="flow-analysis/" + flowAnalysisId, ver='v1')
        response_json = response_get
        status = response_json["request"]["status"]
    except:
        print ("\nSomething is wrong when executing GET /flow-analysis/{flowAnalysisId}")

    return status

if __name__ == "__main__":

    pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(path_trace("10.10.50.61", "10.10.50.65"))