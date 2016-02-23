from helpers.myHelpers import list_to_string

class Issue(object):
	def __init__(self,response,attribs):
		self.issue=[]
		self.update_issue_list(response,attribs)

	def update_issue_list(self,resp,atrbs):
		size = len(atrbs)
		for i in range(size):
			if(atrbs[i]=="labels"):
				all_label = list_to_string(resp["labels"])
				self.issue.append(all_label)
			else:	
				self.issue.append(resp[atrbs[i]])

