#importing necessary packages
from simple_salesforce import Salesforce, format_soql
import base64
import glob
import pandas as pd
from pathlib import Path
import os
from datetime import datetime

date = str(datetime.now().month) + '/' + str(datetime.now().day) + '/' + str(datetime.now().year)

#setting up SF session
Username = 'SALESFORCE_USERNAME'
Password = 'SALESFORCE_PASSWORD'
Securitytoken = 'SALESFORCE_SECURITY_TOKEN'
sf = Salesforce(username=Username, password=Password, security_token=Securitytoken)

#get path of csv containing list of districts/counties (will need to update for windows machine)
os.chdir('c:/Users/Administrator/CommandLineUtility/DistrictDashboardSharing') #path to folder where csv is

#district variables
districtlist_csv = glob.glob('districts.csv')[0]
#get districts from csv containing list of districts we want to automate sharing for
templist = list(pd.read_csv(districtlist_csv,header=None)[0])
#get names of districts with underscores (to match to pdf name)
districts = [d.replace('%20','_') for d in templist]
#get names of districts with spaces (to match to SF name)
districts_sf = [d.replace('%20',' ') for d in templist]

#county variables
countylist_csv = glob.glob('counties.csv')[0]
#get counties from csv containing list of counties we want to automate sharing for
countytemplist = list(pd.read_csv(countylist_csv,header=None)[0])
#get names of counties with underscores (to match to pdf name)
counties = [c.replace('%20','_') for c in countytemplist]
#get names of counties with spaces (to match to SF name)
counties_sf = [c.replace('%20',' ') for c in countytemplist]

#districts
#get list of the paths for all pdfs (will need to update for windows machine)
os.chdir('c:/Users/Administrator/CommandLineUtility/DistrictDashboardSharing/SOME_DASHBOARDExports_Script')
pdflist = glob.glob('*.pdf')
pdfpathlist = ['c:/Users/Administrator/CommandLineUtility/DistrictDashboardSharing/SOME_DASHBOARDExports_Script'+'/'+ filename for filename in pdflist]

for i in range(len(districts)):
    
    #prep work
    #get district name with underscore
    d = districts[i]
    print(f"\n\n{d}")
    #get district name with spaces
    sf_d = districts_sf[i]
    #print(sf_d)
    #get the district account id in SF
    try:
        district_info = sf.query(f"SELECT Id, Name FROM Account Where Name like '{sf_d} School District'")
        accountId = district_info["records"][0]["Id"]
    except:
        try:
            district_info = sf.query(f"SELECT Id, Name FROM Account Where Name like '{sf_d}%'")
            accountId = district_info["records"][0]["Id"]
        except:
            sf_d = sf_d.replace('-',' ')
            district_info = sf.query(f"SELECT Id, Name FROM Account Where Name like '{sf_d}%'")
            accountId = district_info["records"][0]["Id"]
    #print(district_info)
    #get pdf path
    pdf_path = [p for p in pdfpathlist if d in p][0]
    #print(pdf_path)
    #encode the content of the pdf
    with open(pdf_path, "rb") as f:
        byte_string = base64.b64encode(f.read()).decode('utf-8')
    #print(byte_string)
    
    #fill information for creating document
    fields = {'Title' : f"{sf_d} Data Sharing REPORT TYPE {date}.pdf", 
          'PathOnClient' : pdf_path,
          'VersionData' : byte_string,
          'ContentLocation':'S'}
    contentvers = sf.ContentVersion.create(fields)
    print(contentvers)
    
    #find document id
    cvid = contentvers['id'] 
    document = sf.query(f"SELECT ContentDocumentId FROM ContentVersion WHERE Id = '{cvid}'") 
    docid = document['records'][0]['ContentDocumentId']
    print(docid)

    #use document id and account id to link the document to the account
    fields2 = {
        'ContentDocumentId':docid,
        'LinkedEntityId': accountId,  #changes with each loop
        'Visibility': 'AllUsers'}
    condoclink = sf.ContentDocumentLink.create(fields2)
    print(condoclink)
    #check box that triggers public link creation
    sf.Account.update(accountId, {'Create_Public_Links__c':'true'})
    
    
os.chdir('c:/Users/Administrator/CommandLineUtility/DistrictDashboardSharing/SOME_DASHBOARDExports_ScriptCounty')
pdflist = glob.glob('*.pdf')
pdfpathlist = ['c:/Users/Administrator/CommandLineUtility/DistrictDashboardSharing/SOME_DASHBOARDExports_ScriptCounty'+'/'+ filename for filename in pdflist]

for i in range(len(counties)):
    
    #prep work
    #get county name with underscore
    c = counties[i]
    print(f"\n\n{c}")
    #get county name with spaces
    sf_c = counties_sf[i]
    #print(sf_c)
    #get the county account id in SF
    try:
        county_info = sf.query(f"SELECT Id, Name FROM Account Where Name = '{sf_c} County Office of Education'")
        accountId = county_info["records"][0]["Id"]
    except:
        try:
            county_info = sf.query(f"SELECT Id, Name FROM Account Where Name like '{sf_c} County Department of Education'")
            accountId = county_info["records"][0]["Id"]
        except:
            county_info = sf.query(f"SELECT Id, Name FROM Account Where Name like '{sf_c} County%'")
            accountId = county_info["records"][0]["Id"]
    #print(county_info)
    #get pdf path
    pdf_path = [p for p in pdfpathlist if c in p][0]
    #print(pdf_path)
    #encode the content of the pdf
    with open(pdf_path, "rb") as f:
        byte_string = base64.b64encode(f.read()).decode('utf-8')
    #print(byte_string)
    
    #fill information for creating document
    fields = {'Title' : f"{sf_c} County Data Sharing REPORT TYPE {date}.pdf", 
          'PathOnClient' : pdf_path,
          'VersionData' : byte_string,
          'ContentLocation':'S'}
    contentvers = sf.ContentVersion.create(fields)
    print(contentvers)
    
    #find document id
    cvid = contentvers['id'] 
    document = sf.query(f"SELECT ContentDocumentId FROM ContentVersion WHERE Id = '{cvid}'") 
    docid = document['records'][0]['ContentDocumentId']
    print(docid)

    #use document id and account id to link the document to the account
    fields2 = {
        'ContentDocumentId':docid,
        'LinkedEntityId': accountId,  #changes with each loop
        'Visibility': 'AllUsers'}
    condoclink = sf.ContentDocumentLink.create(fields2)
    print(condoclink)
    #check box that triggers public link creation
    sf.Account.update(accountId, {'Create_Public_Links__c':'true'})
    
    
