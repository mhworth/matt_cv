# Create your views here.

import json

from django.views.generic import ListView, View, TemplateView, FormView
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q
from django.core.mail import send_mail

from matt_cv.core.models import *
from matt_cv.core.forms import *


class HomeView(TemplateView):
    template_name="core/index.djhtml"

    def get_context_data(self,**kwargs):
        context = super(HomeView,self).get_context_data(**kwargs)
        context["skill_categories"] = SkillCategory.objects.all().order_by("-importance")
        context["work_experiences"] = WorkExperience.objects.all()
        context["skills"] = Skill.objects.all().order_by("-importance")
        return context

class AboutView(TemplateView):
    template_name="core/about.djhtml"

    def get_context_data(self,**kwargs):
        context = super(AboutView,self).get_context_data(**kwargs)
        context["skill_categories"] = SkillCategory.objects.all().order_by("-importance")
        context["work_experiences"] = WorkExperience.objects.all()
        context["skills"] = Skill.objects.all().order_by("-importance")
        return context

class CVView(TemplateView):
    template_name = "core/cv.djhtml"

    def get_context_data(self,**kwargs):
        context = super(CVView,self).get_context_data(**kwargs)
        context["skill_categories"] = SkillCategory.objects.all().order_by("-importance")
        context["work_experiences"] = WorkExperience.objects.all().order_by("-importance")
        context["skills"] = Skill.objects.all().order_by("-importance")
        context["awards"] = Award.objects.all().order_by("-year_awarded")
        context["publications"] = Publication.objects.all().order_by("-date")
        return context

class PortfolioView(TemplateView):
    template_name="core/portfolio.djhtml"

    def get_context_data(self,**kwargs):
        context = super(PortfolioView,self).get_context_data(**kwargs)
        context["skill_categories"] = SkillCategory.objects.all().order_by("-importance")
        context["work_experiences"] = WorkExperience.objects.all()
        context["skills"] = Skill.objects.all().order_by("-importance")
        
        # Filter the projects if the proper query strings were passed
        skills = self.request.REQUEST.getlist("skill")
        if len(skills)>0:
            projects = Project.objects.filter(skills__slug__in=skills).order_by("-importance").distinct()
        else:
            projects = Project.objects.all().order_by("-importance")

        context["projects"] = projects
        return context

class ContactView(FormView):
    template_name="core/contact.djhtml"
    form_class = ContactForm

    def form_valid(self,form):
        data = form.cleaned_data
        name = data.get("name","")
        sender = data.get("sender","")
        subject = data.get("subject","")
        message = data.get("message","")

        full_message = """
            %(subject)s
            Got a message from the sender %(name)s with the email address %(sender)s. The message is as follows.

            %(message)s

            ===
        """%{"message":message,"subject":subject,"sender":sender,"name":name}
        send_mail("Email from Matt's CV site", full_message, 'matt@crabice.com', ['mr.hworth@gmail.com'], fail_silently=False)

        return super(ContactView,self).form_valid(form)

    def get_success_url(self):
        url = reverse("contact") + "?success=true"
        return url
class SkillsView(ListView):
    template_name="core/skills.djhtml"
    model = Skill
    context_object_name = "skills"

    def get_context_data(self,**kwargs):
        context = super(SkillsView,self).get_context_data(**kwargs)
        context["skill_categories"] = SkillCategory.objects.all().order_by("-importance")
        context["work_experiences"] = WorkExperience.objects.all()
        context["skills"] = Skill.objects.all().order_by("-importance")
        return context

class ProjectView(TemplateView):

    def get_template_names(self):
        project_slug = self.kwargs["slug"]
        return ["core/projects/%s.djhtml"%project_slug]

    def get_context_data(self,**kwargs):
        context = super(ProjectView,self).get_context_data(**kwargs)
        context["project"] = Project.objects.get(slug = kwargs["slug"])
        return context

class ServiceView(View):

    def projects(self,request,**kwargs):
        data = serializers.serialize("json", Project.objects.all(),use_natural_keys=True)
        return data
    
    def skills(self,request,**kwargs):
        target = kwargs.get("target")

        if target:
            # Single skill
            skill = Skill.objects.get(slug=target)
            retval = {}
            retval["name"] = skill.name
            retval["slug"] = skill.slug
            retval["description"] = skill.description
            retval["years_of_experience"] = skill.years_of_experience
            retval["pk"] = skill.pk

            # Stick in the projects too
            projects = []
            for project in Project.objects.filter(skills=skill).distinct():
                projects.append({
                    "name":project.name,
                    "slug":project.slug,
                    "url":project.get_absolute_url(),
                    "description":project.description,
                    "thumbnail":project.thumbnail.name if project.thumbnail else None
                })
            retval["projects"] = projects

            # Stick in the work experience which used these skills (also merge with the projects associated with the WE that used these skills)
            work_experience = []
            q = Q(skills=skill) | Q(project__skills=skill)
            for we in WorkExperience.objects.filter(q).distinct():
                work_experience.append({
                    "slug":we.slug,
                    "description":we.description,
                    "employer":we.employer,
                    "position":we.position,
                })
            retval["work_experience"] = work_experience
            data = json.dumps(retval)
        else:
            # All skills
            data = serializers.serialize("json", Skill.objects.all(),use_natural_keys=True)
        return data
    def get_data(self,request,**kwargs):
        action = kwargs.get("action","").lower()
        if action in ["projects","skills"]:
            return getattr(self,action)(request,**kwargs)


    def get(self,request,**kwargs):
        data = self.get_data(request,**kwargs)
        return HttpResponse(data)


home = HomeView.as_view()
about = AboutView.as_view()
cv = CVView.as_view()
portfolio = PortfolioView.as_view()
contact = ContactView.as_view()
skills = SkillsView.as_view()
project = ProjectView.as_view()
service = ServiceView.as_view()