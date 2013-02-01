from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True) 

class Project(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    #decription Not Null but may be ''
    description = models.TextField(blank=True) 
    #Ok. This is hierarchi structure now.
    parent = models.ForeignKey('self', blank=True, null=True)
    #But I want to have tags =)
    tags=models.ManyToManyField(Tag, blank=True);
    # If user use quick method he create project only wih name.
    # It is not good for next sistimatisation and analis.
    # So we can remaind him about all this projects.
    new = models.BooleanField(default=False)
    #There are may be many projects
    #Some of them only for hierarh srtucture
    #Let's filter them!
    can_has_records = models.BooleanField(default=True)
    #others...
    
    def __unicode__ (self):
        return self.name

class Record(models.Model):
    #I think, that we may dell user from this class.
    #Because project has user and we can't create record without user.
    #Then fix view index of obojects.
    #but if it we want an instrujent of team work this field is must have
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    start_time = models.DateTimeField('start Time')
    #Now we save seconds it this field
    duration = models.IntegerField()
    note = models.TextField(blank=True)
    
    def __unicode__(self):
        return '%s %s' %(self.project, self.start_time) 
    
    




