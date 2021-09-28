import snowflake.connector
import pandas as pd

con = snowflake.connector.connect(
    user='SNOWFLAKE_USER',
    password='SNOWFLAKE_PASSWORD',
    account='SNOWFLAKE_ACCOUNT',
    warehouse='WAREHOUSE',
    database='DATABASE',
    schema= 'SCHEMA',
    role= 'ROLE'
)

#districts
cur = con.cursor()
sql = "select distinct DISTRICT_NAME from SOME_VIEW where SCHOOL_TYPE = 'Some Condition' and split_part(DISTRICT_NAME,' County Office',1) not in (select distinct County from SOME_VIEW) and split_part(DISTRICT_NAME,' County Department',1) not in (select distinct County from SOME_VIEW)"
cur.execute(sql)
df = cur.fetch_pandas_all()

tabcmddf = df.copy()
for i in tabcmddf.index:
    tabcmddf.loc[i,'DISTRICT_NAME'] = tabcmddf.loc[i,'DISTRICT_NAME'].replace(' ','%20')
    
tabcmddf.to_csv(r'C:\Users\Administrator\CommandLineUtility\DistrictDashboardSharing\districts.csv', header = False, index = False)
print(f"Number of some condition districts in SOME_VIEW: {len(tabcmddf)}")

#counties
cur = con.cursor()
sql = "select DISTINCT COUNTY from SOME_VIEW where SCHOOL_TYPE = 'Some Condition'"
cur.execute(sql)
snowcounties = cur.fetch_pandas_all()

countydf = snowcounties.copy()
for i in countydf.index:
    countydf.loc[i,'COUNTY'] = countydf.loc[i,'COUNTY'].replace(' ','%20')
    
countydf.to_csv(r'C:\Users\Administrator\CommandLineUtility\DistrictDashboardSharing\counties.csv', header = False, index = False)
print(f"Number of counties with some condition districts in SOME_VIEW: {len(countydf)}")
