try:
    from django.conf.urls.defaults import patterns, include, url
except ImportError:
    from django.conf.urls import patterns, url, include
from django.conf import settings

urlpatterns = patterns('',

    url(r'^$',"matt_cv.core.views.home",name="home"),
    url(r'portfolio/$',"matt_cv.core.views.portfolio",name="portfolio"),
    url(r'contact/$',"matt_cv.core.views.contact",name="contact"),
    url(r'skills/$',"matt_cv.core.views.skills",name="skills"),
    url(r'cv/$',"matt_cv.core.views.cv",name="cv"),
    url(r'resume/$',"matt_cv.core.views.cv",name="resume"),
    url(r'about/$',"matt_cv.core.views.about",name="about"),
    url(r'project/(?P<slug>.+)/','matt_cv.core.views.project',name='project'),
    url(r'service/(?P<action>.+)/(?P<target>.+)?','matt_cv.core.views.service',name='service'),
)

