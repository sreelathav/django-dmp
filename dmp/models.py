from django.db import models

# Create your models here.

from django.db import models

import datetime
from datetime import datetime, timedelta, date
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import PositiveIntegerField

import re

# import users 
from django.contrib.auth.models import *
#from cedainfoapp.models import *
from sizefield.models import FileSizeField

#----- 

class Person(User):
    class Meta:
        proxy = True
        ordering = ('username',)

class Project(models.Model):

    # Projects are activities under funding programmes that are examined
    # for their data management needs.

    title = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    desc = models.TextField(blank=True, null=True)
    notes = GenericRelation("Note")
    data_activities = models.TextField(blank=True, null=True, help_text="Short description of data generation activities. eg Data will be collected by FAAM aircraft/ground instruments. Are there intensive measurement campaigns?")
    startdate = models.DateField(blank=True, null=True,verbose_name="Start Date",help_text="Date format dd/mm/yyyy")
    enddate = models.DateField(blank=True, null=True,verbose_name="End Date",help_text="Date format dd/mm/yyyy")
    dmp_agreed = models.DateField(blank=True, null=True, verbose_name="DMP Agreed",help_text="Date format dd/mm/yyyy")
    initial_contact = models.DateField(blank=True, null=True, verbose_name="Initial Contact",help_text="Date format dd/mm/yyyy")
    sciSupContact = models.ForeignKey(Person, help_text="CEDA person contact for this Project", blank=True, null=True)
    PI = models.CharField(max_length=200, blank=True, null=True)
    PIemail = models.EmailField(max_length=200, blank=True, null=True)
    PIinst = models.CharField(max_length=200, blank=True, null=True)
    Contact1 = models.CharField(max_length=200, blank=True, null=True)
    Contact2 = models.CharField(max_length=200, blank=True, null=True)
    projectcost = models.IntegerField(blank=True, null=True)
    services = models.TextField(blank=True, null=True)
    primary_dataCentre = models.CharField(max_length=200,blank=True, null=True)
    other_dataCentres = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True,
            choices=(("Proposal","Proposal"),
                 ("NotFunded","Not Funded"),
                 ("NotStarted","Not Started"),
                 ("Active","Active"),
                 ("NoData","No Data"),
                 ("EndedWithDataToCome","Ended with data to come"),
                 ("Defaulted","Defaulted"),
                 ("NoDataForUs","No data for us"),
                 ("Complete","Complete")))
    modified = models.DateTimeField(auto_now=True)
    third_party_data = models.ManyToManyField('DataProduct', related_name='requirements+', 
                        blank=True, null=True)
    # vms = models.ManyToManyField(VM, blank=True, null=True)
    # groupworkspaces = models.ManyToManyField(GWS, blank=True, null=True)
    project_URL = models.URLField(blank=True, null=True)
    dmp_URL = models.URLField(blank=True, null=True, verbose_name="DMP URL")
    ODMP_URL = models.URLField(blank=True,null=True)
    moles_URL = models.URLField(blank=True,null=True)
    project_usergroup = models.CharField(max_length=200, blank=True, null=True, help_text="Group name for registration for this group")
    metadata_form = GenericRelation("MetadataForm")


    def active(self):
        if self.status in ("Active", "EndedWithDataToCome"): return True 
        elif self.status == "NotStarted" and self.startdate < date.today(): return True
        elif not self.status: return True
        else: return False
	
    def __unicode__(self):
        return "%s" % self.title

    def ndata(self):
        dps = DataProduct.objects.filter(project=self)
        return len(dps)

    def data_outputs(self):
        dps = DataProduct.objects.filter(project=self)
        return dps

    def datastatecount(self):
        dps = DataProduct.objects.filter(project=self, status='WithProjectTeam')
        nteam = len(dps)
        dps = DataProduct.objects.filter(project=self, status='Ingesting')
        ningest = len(dps)
        dps = DataProduct.objects.filter(project=self, status='Archived')
        ndone = len(dps)
        dps = DataProduct.objects.filter(project=self, status='Defaulted')
        ndone += len(dps)
        dps = DataProduct.objects.filter(project=self, status='NotArchived')
        ndone += len(dps)
        return (nteam, ningest, ndone)

    def summary_text(self):
        title = self.title
        m = re.search('\(([A-Z]{4,})', title)
        if m: acronym = m.group(1)
        else: 
            m = re.search('([A-Z]\w*[A-Z]\w*)', title)
            if m: acronym = m.group(1)
            else: 
                acronym = ''

        pi = self.PI
        m = re.search('( \w+ \()', pi)
        if m: pi = m.group(1)
        else: pi = pi
        
        return "%s %s"% (acronym, pi)

    def project_groups_links(self):
        output = ''
        for g in self.projectgroup_set.all():
            output += '<a href="/admin/dmp/projectgroup/%s">%s</a> ' % (g.id, g.name)
        return output
    project_groups_links.allow_tags = True    

    def project_groups(self):
        return ProjectGroup.objects.filter(projects=self)   

    def grants(self):
        return Grant.objects.filter(project=self)

    def grant_links(self):
        output = ''
        for g in self.grants():
            output += '<a href="/admin/dmp/grant/%s">%s</a> ' % (g.id, g.number)
        return output
    grant_links.allow_tags = True    

    def alerts(self):
        # produce alert flag (red, amber, green) and alert text to show needed actions.
        # 
        # 4 alert types, DMP agreement, contact, end of project, missing info.
        month = timedelta(days=31)
        now = date.today()
        flag = 0  # green - default
        text = '' # default alert text
        if self.status == 'NoData' and not self.initial_contact: return ('ambar', 'Marked as no data, but not contacted?')
        if not self.active(): return ('green', 'No warnings as not active.')

        # Need to set start and end dates to have alerts
        if not self.startdate: return ('red', 'Need a start date.')
        if not self.enddate: return ('red', 'Need an end date.')
        
        # check DMP status
        if self.startdate + 3*month < now and not self.dmp_agreed: 
            flag = max(flag, 2)
            text += 'DMP not agreed after 3 months from project start. '
        elif self.startdate + 2*month < now and not self.dmp_agreed:
            flag = max(flag, 1)
            text += 'DMP not agreed after 2 months from project start. '

        # check contact status
        if self.startdate + 2*month < now and not self.initial_contact: 
            flag = max(flag, 2)
            text += 'No contact in the first 2 months of the project. '
        elif self.startdate + 1*month < now and not self.initial_contact:
            flag = max(flag, 1)
            text += 'No contact in the first 1 months of the project. '

        # check contact status
        if self.startdate < now and self.status=="NotStarted": 
            flag = max(flag, 1)
            text += 'Change status to active? '

        # end of project
        if self.enddate < now: 
            flag = max(flag, 2)
            text += 'Project ended but not marked as complete. '
        elif self.enddate - 3*month < now:
            flag = max(flag, 1)
            text += '3 months before project end.  '

        # check critical fields
        if not self.title:
            flag = max(flag, 2)
            text += 'Needs a title. '
        if not self.sciSupContact:
            flag = max(flag, 1)
            text += 'Needs a science support contact. '
        if not self.PI:
            flag = max(flag, 2)
            text += 'Needs a PI name. '
        if not self.status:
            flag = max(flag, 1)
            text += 'Needs a status. '  
            
        print flag, text    
        flag = ('green', 'ambar', 'red')[flag]
        return (flag, text)              

    def is_jasmin(self):
        #look for jasmin in vm mountpoints 
        for vm in self.vms.all():
            for mount in vm.mountpoints_required:
                if mount.find("jasmin") != -1: return True
        #look for jasmin in groupworkspaces
        for gws in self.groupworkspaces.all():
            if gws.path.find("jasmin") != -1: return True
        return False

    def is_cems(self):
        #look for cems in vm mountpoints 
        for vm in self.vms.all():
            for mount in vm.mountpoints_required:
                if mount.find("cems") != -1: return True
        #look for cems in groupworkspaces
        for gws in self.groupworkspaces.all():
            if gws.path.find("cems") != -1: return True
        return False


#-----

class DataProduct(models.Model):

    # Data products are data streams produced by projects

    title = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    notes = GenericRelation("Note")
    datavol = FileSizeField(default=0)
    project = models.ForeignKey(Project, help_text="Project producing this data", blank=True, null=True)
    sciSupContact = models.ForeignKey(User, help_text="CEDA person contact for this data", blank=True, null=True)
    contact1 = models.CharField(max_length=200, blank=True, null=True)
    contact2 = models.CharField(max_length=200, blank=True, null=True)
    deliverydate = models.DateField(blank=True, null=True)
    preservation_plan = models.CharField(max_length=200, blank=True, 
              null=True, choices=( ("KeepIndefinitely","Keep Indefinitely"),
                 ("KeepAsIs","Keep as is - Even if obsolete"),
                 ("Dispose5years ","Review for disposal 5 years after project completes"),
                 ("ManageInProject","Don't Archive - manage the data within the project"),
                 ("Subset","Plan to keep a subset of the data indefinitely"),
                 ("TBD","TBD")))
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    review_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=200, blank=True, null=True,
            choices=( ("WithProjectTeam","With Project Team"),
                 ("Ingesting","Ingesting"),
                 ("Archived","Archived and complete"),
                 ("Defaulted","Defaulted - not archived due to project not supplying data"),
                 ("NotArchived","Not going to archive - planned")))
    data_URL = models.URLField(blank=True, null=True)


    
    def __unicode__(self):
        return "%s" % self.title

    def projects_where_thirdparty(self): 
        return Projects.objects.filter(third_party_data=self)

class Grant(models.Model):
    project = models.ForeignKey('Project', blank=True, null=True)
    number = models.CharField(max_length=200)
    title = models.CharField(max_length=800, blank=True, null=True)
    pi = models.CharField(max_length=200, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    # if grant is a child grant, enter email. This is used as a CC  when emails are sent.
    data_email = models.EmailField(blank=True, null=True)

    def __unicode__(self):
        if not self.title: return "%s" % self.number
        elif len(self.title) > 100: return "%s: %s..." % (self.number, self.title[0:100])
        else: return "%s: %s" % (self.number, self.title)

    def gotw(self):
        if self.number: 
            return '<a style="color:red; background-color:lightblue; border:2px blue dashed" href="http://gotw.nerc.ac.uk/list_full.asp?pcode=%s">%s</a>' %(self.number, self.number)
        else:
            return '-'
    gotw.allow_tags = True    

    def scrape_project(self):
        if not self.project:
            return '<a style="color:green; background-color:red; border:2px blue" href="/dmp/grant/%s/scrape">Scrape Project</a>' % self.pk
        else:
            return '-'
    scrape_project.allow_tags = True



class ProjectGroup(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    projects = models.ManyToManyField('Project', blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.name


class Note(models.Model):
    class Meta:
        verbose_name_plural = "Notes"
        ordering = ["added"]

    added = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(Person, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = PositiveIntegerField(null=True)
    location = GenericForeignKey('content_type', 'object_id')

class MetadataForm(models.Model):
    modified = models.DateTimeField(auto_now_add=True,verbose_name="last modified")
    form_type = models.CharField(max_length=200, blank=True, null=True,
            choices=( ("projectForm","Project Form"),
                      ("instrumentForm","Instrument Form"),
                      ("datasetForm","Dataset Form"),
                      ("platformForm","Platform Form"),
                      ))
    form_link = models.URLField(blank=True,null=True)

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = PositiveIntegerField(null=True)
    location = GenericForeignKey('content_type', 'object_id')

    def save(self,*args,**kwargs):
        'On save update modified'
        self.modified = timezone.now()
        return super(MetadataForm, self).save(*args,**kwargs)

class EmailTemplate(models.Model):
    template_name = models.CharField(max_length=200)
    template_ref = models.CharField(max_length=200, null=True)
    last_edited = models.DateField(auto_now_add=True)
    edited_by = models.ForeignKey(User,null=True)
    content = models.TextField(blank=True)


class DOGstats(models.Model):
    '''table of statistics for monthly DOG snapshots'''
    date = models.DateTimeField()
    stat_type = models.CharField(max_length=200)
    active_grants = models.IntegerField(null=True)
    contacted_grants = models.IntegerField(null=True)
    dmps_accepted = models.IntegerField(null=True)
    no_data = models.IntegerField(null=True)
    complete_grants = models.IntegerField(null=True)
    ended_with_outstanding_data = models.IntegerField(null=True)
    total_grants = models.IntegerField(null=True)

