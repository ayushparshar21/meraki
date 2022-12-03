import initialization, meraki, re
dashboard = meraki.DashboardAPI(initialization.API_KEY)
clients=[]
hpmac='04:0e:3c'
with open('input.test','r') as file:
    lines=file.readlines()
    for line in lines:
       response=dashboard.devices.getDevice(line.strip())
       clients.append({'serial':response['serial'], 'mac':response['mac']})
for i in clients:
    if re.match(hpmac,i['mac'], re.IGNORECASE):
        print(i)
