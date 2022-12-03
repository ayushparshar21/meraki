import initialization, meraki, re
def getorgid(dashboard):
    flag=0
    #looks up org id for a specific org name
    #on failure returns 'null'
    try:
        response = dashboard.organizations.getOrganizations()
    except:
        printusertext('ERROR 00: Unable to contact Meraki cloud')
        flag=1
        sys.exit(2)
    if flag==0:
        return response[0].get('id')
    else:
       return 'null'
def createnw(dashboard):


dashboard = meraki.DashboardAPI(initialization.API_KEY)
orgid=getorgid(dashboard)
if orgid!='null':
    createnw(dashboard)
