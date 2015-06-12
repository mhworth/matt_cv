from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
class Base(models.Model):
    class Meta:
        abstract = True

    importance = models.IntegerField(default=0)
    slug = models.CharField(max_length=50,unique=True)

    def natural_key(self):
        return self.slug

class SkillCategory(Base):
    name = models.CharField(max_length=50,unique=True,blank=False,null=False)
    description = models.TextField(blank=False)

class SkillManager(models.Manager):
    def get_by_natural_key(self,slug):
        return self.get(slug=slug)

class Skill(Base):
    objects = SkillManager()
    class Meta:
        ordering = ['-importance', 'years_of_experience','name']
    name = models.CharField(max_length=50,unique=True,blank=False,null=False)
    description = models.TextField(blank=False)
    years_of_experience = models.IntegerField()
    categories = models.ManyToManyField('SkillCategory')
    primary_category = models.ForeignKey('SkillCategory',related_name="skill_category_primary")

    def get_absolute_url(self):
        return reverse("skills") + "?skill="+self.slug

class WorkExperience(Base):
    class Meta:
        ordering = ('-start_date','-importance')
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    employer = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    skills = models.ManyToManyField('Skill')
    description = models.TextField(blank=False)

    def get_absolute_url(self):
        return reverse("cv") + "#"+self.slug

class Contribution(models.Model):
    class Meta:
        ordering = ('-importance','-start_date')
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    description = models.TextField(blank=False)
    experience = models.ForeignKey('WorkExperience')
    importance = models.IntegerField(default=0)

class Award(models.Model):
    year_awarded = models.IntegerField()
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    awarded_by = models.CharField(max_length=150)
    importance = models.IntegerField(default=0)

class Publication(models.Model):
    citation = models.TextField()
    date = models.DateField()
    primary_author = models.BooleanField()
    class Meta:
        ordering = ('-date',)

class Project(Base):
    class Meta:
        ordering = ('-importance','-start_date')
    name = models.CharField(max_length=150)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    description = models.TextField(blank=True)
    work_experience = models.ForeignKey('WorkExperience')
    skills = models.ManyToManyField('Skill')
    thumbnail = models.ImageField(upload_to="project-thumbnails")

    def get_absolute_url(self):
        return reverse("project",args=[self.slug])
