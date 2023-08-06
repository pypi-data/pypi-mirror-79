from jiraX.project import Project
from jiraX.issue import Issue
from jiraX.comment import Comment
import factory

class ProjectFactory(factory.Factory):
    class Meta:
        model = Project

    user = None
    apikey = None
    server = None

class IssueFactory(factory.Factory):
    class Meta:
        model = Issue

    user = None
    apikey = None
    server = None

class CommentFactory(factory.Factory):
    class Meta:
        model = Comment

    user = None
    apikey = None
    server = None