import initialization, meraki, re, pprint
from datetime import date
dashboard = meraki.DashboardAPI(initialization.API_KEY)
today = date.today()
def fetch_organization_id():
    org = dashboard.organizations.getOrganizations()
    return org[0]['id']
def fetch_config_template_info():
    response = dashboard.organizations.getOrganizationConfigTemplates(fetch_organization_id())
    for i in response:
        if i['name'] == 'Terminated':
            return i['id']
    
    
def narp_meraki(networks):
    terminated_id=fetch_config_template_info()
    for i in networks:
        print(i['NETWORK_ID'])
        dashboard.networks.unbindNetwork(i['NETWORK_ID'])
        dashboard.networks.bindNetwork(i['NETWORK_ID'], terminated_id,autoBind=False)
#     print("Moving " + i['NAME'] + " to Terminated template")             

def update_network_name(networks):
      for i in networks:
          print("UPDATING NETWORK NAME FOR : "+ i['NAME']+ "\n")
#          dashboard.networks.updateNetwork(i['NETWORK_ID'],name=i['NAME']+' NARP '+ today.strftime("%m-%d-%y"))
 

def find_network():
    def createlist(dataset):
            networks=[]
            for i in dataset:
                if not re.search("NARP", i['name']) and not re.search("MX", i['name']) and not re.search("Greer", i['name']) and not re.search("West Chester", i['name']) and not re.search("Syracuse", i['name']) and not re.search("Bannockburn",i['name']) and not re.search("Mobile", i['name']) and not re.search("Quarantine", i['name']):
#                    print(i['name'])
                    if i.get('configTemplateId'):
                        networks.append({'NAME': i['name'].title(),'NETWORK_ID' : i['id'],'CONFIGTEMPLATE_ID': i['configTemplateId']})
            return networks
    def fetch_networks(org_id):
        response = dashboard.organizations.getOrganizationNetworks(org_id,total_pages='all')
        order=sorted(createlist(response),key = lambda i: i['NAME'])
        with open('networks','w') as fdev:
            pprint.pprint(order,stream=fdev)
        return  order
    def fetch_narp_list():
        narp_list=[]
        with open('narp','r') as narp_file:
            for line in narp_file:
                    narp_list.append(line.strip().title())
        return narp_list
    def binarysearch(arr,l,r,x):
        if r >= l:
            mid = l + (r - l) // 2
            if arr[mid]['NAME'] == x:
                return mid
            elif arr[mid]['NAME'] > x:
                return binarysearch(arr, l, mid - 1, x)
            else:
                return binarysearch(arr, mid + 1, r, x)
        else:
            return -1
    final_list=[]
    networks=fetch_networks(fetch_organization_id())
    narp=fetch_narp_list()
    for i in narp:
        record=binarysearch(networks,0,len(networks)-1,i)
        if record != -1:
                print("MERAKI NETWORK FOR : " + i + " FOUND\n")
                final_list.append({'NETWORK_ID' : networks[record]['NETWORK_ID'], 'NAME' : networks[record]['NAME'], 'CONFIGTEMPLATE_ID': networks[record]['CONFIGTEMPLATE_ID']})
#            final=update_network_name(record,networks)
        else:
                print("NO MERAKI NETWORK FOUND FOR: " + i + "\n")
    return final_list
 

narp_meraki_list=find_network()
#update_network_name(narp_meraki_list)
narp_meraki(narp_meraki_list)
#fetch_config_template_info()