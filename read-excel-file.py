import pandas as pd
import pprintpp
dataframe =  pd.read_excel('SwitchportList.xlsx')
switches = {}
#print(len(dataframe.values))

for el in dataframe.values:
    for i in range(len(el)):
        if i / 2 == 1:
            key = el[i][0:10]
            value = el[i][10:]
            if key not in switches:
                switches[key] = {
                    "host": key,
                    "ports": []
                }
            port_found = False
            for port in switches[key]["ports"]:
                if value.strip() in port:
                    port_found = True
                    port[value.strip()].append({
                        'addr': f"{el[i][0:8] + '' + str(el[1])}",
                        'location': el[3]
                    })
                    break

            if not port_found:
                switches[key]["ports"].append({
                    f"{value.strip()}": [{
                        'addr': f"{el[i][0:8] + '' + str(el[1])}",
                        'location': el[3]
                    }]
                })


pprintpp.pprint(switches)
