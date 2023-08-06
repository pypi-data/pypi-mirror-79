import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Project(Base):

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_all(self): 
		try:
			logging.info("Start function: find_all")
			return self.jira.projects()	
			logging.info("End function: find_all")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 
	
	def find_issue(self, project_key):
		try:
			logging.info("Start function: find_issue")
			return self.jira.search_issues('project='+project_key)
			logging.info("End function: find_issue")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

	def find_group(self, project_key):
		try:
			logging.info("Start function: find_issue")
			return self.jira.groups('project='+project_key)
			logging.info("End function: find_issue")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 