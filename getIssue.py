import urllib2
import sys
import json
import xlsxwriter

from utils.issues import Issue



token  = raw_input("please enter your private token and> ")
private_token = "?private_token="+token

if not token:
	print "please supply valid token"
	sys.exit()


base_url="https://gitlab.com/api/v3"

project_api="/projects"
issues_api="/issues"


#project_id="414874"
project_id =raw_input("please enter project id to fetch issues> ")

if not project_id:
	print "please supply valid project id"
	sys.exit()



delim="?"

per_page_key="&per_page="
page_num_key="&page="

curr_page=1
per_page=100

attribs=["iid","title","description","state","created_at","updated_at","labels"]



req_url=base_url+project_api+"/"+project_id+issues_api+private_token

req_url_paginated=req_url+page_num_key+str(curr_page)+per_page_key+str(per_page)

print "---------------------------------------------"
print "fetching issues, please wait ...."

try:
   
	response=urllib2.urlopen(req_url_paginated).read()
   	
except urllib2.HTTPError, err:
   	if err.code == 404:
       		print "Page not found"
   	elif err.code == 401:
		print "unauthorised access, please check your private token"
       	else:
		print "unable to fetch result"
		
	sys.exit()


issues_list=[]


parsed_data = json.loads(response)
response_len=len(parsed_data)

def update_issue_list():
	for i in range(len(parsed_data)):
		issue=Issue(parsed_data[i],attribs)
		issues_list.append(issue)


update_issue_list()

while(response_len==per_page):
	curr_page = curr_page + 1  
	req_url_paginated=req_url+page_num_key+str(curr_page)+per_page_key+str(per_page)
	response=urllib2.urlopen(req_url_paginated).read()
	parsed_data=json.loads(response)
	response_len=len(parsed_data)
    	update_issue_list()
	
	

issue_size = len(issues_list)
print "fetching issue completed successfully"
print "total issues fetched :- %d" % issue_size

print "---------------------------------------------"
print "generating MS EXCEL report file"
issues_list.reverse()


atribs_len=len(attribs)

workbook = xlsxwriter.Workbook('gitlab_issue_report.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0


for i in range(atribs_len):
	worksheet.write(row,col,attribs[col])
	col += 1

row += 1
col = 0

for i in range(issue_size):
	for j in range(atribs_len):
		worksheet.write(row+i,col+j,issues_list[i].issue[col+j])



workbook.close()

print "report file generation successfull"
print "report file is saved in same directory as of this script\nplease look for the name gitlab_issue_report.xlsx"

print "---------------------------------------------"
#for i in range(issue_size):
#	print issues_list[i].desc


#issues= namedtuple('issue','id,iid,project_id,title,description,state,created_at,updated_at,labels,milestone,assignee,author')


#issue_list=[issues(**k) for k in parsed_data]

#print issue_list[0]['iid']
#print issue_list[0]['title']

#print response

 
