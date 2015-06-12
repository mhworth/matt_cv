#!/usr/bin/env python
# encoding: utf-8
import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print "Using settings from",os.environ["DJANGO_SETTINGS_MODULE"]
from matt_cv.core.models import *
from django.contrib.auth.models import *
from django.core.files.base import ContentFile

# Initialize
import django
django.setup()

# Categories
SKILL_CATEGORIES=(
    ("Backend","Serverside processes/business logic","backend",10),
    ("User Interfaces","User interface design and implementation","frontend",9),
    ("Data Analysis","Analyzing data",'data-analysis',3),
    ("Scientific Instrumentation","Designing firmware, frontends, electronics, calibration routines, and data analysis algorithms for scientific instruments","instrumentation",2),
    ("Programming Languages","Programming languages in which Matt is fluent","programming-languages",11),
    ("Management","General management","management",12)
)

for name,description,slug,importance in SKILL_CATEGORIES:
    SkillCategory.objects.get_or_create(name=name,description=description,slug=slug,importance=importance)

SKILLS=(
    

    #
    # Languages
    #
    {
        "name":"C++",
        "description":"Application architecture and implementation in the C++ programming language",
        "categories":["instrumentation","programming-languages"],
        "years_of_experience":6,
        "slug":"cpp",
        "importance":9
    },
    {
        "name":"Python",
        "description":"Application architecture, application implementation, and shell scripting in the Python programming language",
        "categories":["instrumentation","programming-languages","data-analysis"],
        "years_of_experience":5,
        "slug":"python",
        "importance":12

    },
    {
        "name":"Javascript",
        "description":"Javascript, as used in modern browsers, Node.js, MongoDB Map/Reduce etc.",
        "categories":["frontend","backend","programming-languages"],
        "years_of_experience":3,
        "slug":"js",
        "importance":10
    },
    {
        "name":"SQL",
        "description":"Used in Relational Database querying",
        "categories":["backend","programming-languages"],
        "years_of_experience":4,
        "slug":"sql",
        "importance":6
    },
    {
        "name":"PHP",
        "description":"Web application design and Joomla plugin development",
        "categories":["backend","programming-languages"],
        "years_of_experience":3,
        "slug":"php",
        "importance":5
    },
    {
        "name":"Java",
        "description":"Application development in the Java programming language",
        "categories":["backend","programming-languages"],
        "years_of_experience":6,
        "slug":"java",
        "importance":10
    },
    {
        "name":"LabVIEW",
        "description":"Application development in the LabVIEW programming language",
        "categories":["programming-languages","instrumentation"],
        "years_of_experience":6,
        "slug":"labview",
        "importance":5
    },

    #
    # Databases
    #
    {
        "name":"MySQL",
        "description":"Administering/developing SQL for a MySQL database server",
        "categories":["backend"],
        "years_of_experience":4,
        "slug":"mysql",
        "importance":5
    },
    {
        "name":"SQLite",
        "description":"Developing applications using SQLite as a database backend",
        "categories":["backend"],
        "years_of_experience":2,
        "slug":"sqlite",
        "importance":5
    },
    {
        "name":"MongoDB",
        "description":"Administering and developing for a MongoDB NoSQL server",
        "categories":["backend"],
        "years_of_experience":2,
        "slug":"mongodb",
        "importance":5
    },

    #
    # API's/Libraries
    #
    {
        "name":"Django",
        "description":"Developing web applications using the Django web framework",
        "categories":["backend",'frontend'],
        "years_of_experience":2,
        "slug":"django",
        "importance":10
    },
    {
        "name":"Joomla!",
        "description":"A PHP-based content management system",
        "categories":["backend",'frontend'],
        "years_of_experience":2,
        "slug":"joomla",
        "importance":4
    },
    {
        "name":"jQuery",
        "description":"A powerful javascript toolkit",
        "categories":["backend",'frontend'],
        "years_of_experience":3,
        "slug":"jquery",
        "importance":8
    },
    {
        "name":"Spring",
        "description":"An inversion of control library for java",
        "categories":["backend"],
        "years_of_experience":3,
        "slug":"spring",
        "importance":4
    },
    {
        "name":"Servlets",
        "description":"A standard Java API for dealing with HTTP requests to a server",
        "categories":["backend"],
        "years_of_experience":4,
        "slug":"servlets",
        "importance":4
    },
    {
        "name":"CORBA",
        "description":"A standard for supplying Remote Method Invocation functionality across multiple languages",
        "categories":["backend"],
        "years_of_experience":2,
        "slug":"corba",
        "importance":2
    },
    {
        "name":"Apache Velocity",
        "description":"An open-source templating language",
        "categories":["backend"],
        "years_of_experience":2,
        "slug":"velocity",
        "importance":2
    },
    {
        "name":"Swing",
        "description":"One of the main GUI APIs in the Java standard library",
        "categories":['frontend'],
        "years_of_experience":3,
        "slug":"swing",
        "importance":2
    },

    #
    # Software tools
    #
    {
        "name":"Maven",
        "description":"An extensible build and dependency managment tool, primarily targetted at Java",
        "categories":["backend","frontend"],
        "years_of_experience":5,
        "slug":"maven",
        "importance":6
    },
    {
        "name":"Scons",
        "description":"A python-based alternative to Make--used for building primarily C++ and Java projects",
        "categories":["backend","data-analysis","instrumentation"],
        "years_of_experience":6,
        "slug":"scons",
        "importance":1
    },
    {
        "name":"Eclipse",
        "description":"An open source IDE for multiple programming languages",
        "categories":['instrumentation','data-analysis','backend','frontend'],
        "years_of_experience":6,
        "slug":"eclipse",
        "importance":5
    },
    {
        "name":"GIT",
        "description":"A distributed Source Code Management toolkit",
        "categories":['instrumentation','data-analysis','backend','frontend'],
        "years_of_experience":3,
        "slug":"git",
        "importance":5
    },
    {
        "name":"Mercurial",
        "description":"A distributed Source Code Management toolkit",
        "categories":['instrumentation','data-analysis','backend','frontend'],
        "years_of_experience":3,
        "slug":"mercurial",
        "importance":5
    },
    {
        "name":"SVN",
        "description":"A server/client Source Code Management toolkit",
        "categories":['instrumentation','data-analysis','backend','frontend'],
        "years_of_experience":5,
        "slug":"svn",
        "importance":5
    },
    {
        "name":"RabbitMQ",
        "description":"A language-agnostic message queue system",
        "categories":['backend'],
        "years_of_experience":1,
        "slug":"rabbitmq",
        "importance":6
    },
    {
        "name":"Celery",
        "description":"A distributed and asynchronous task management system, focusing on Python applications",
        "categories":['backend'],
        "years_of_experience":1,
        "slug":"celery",
        "importance":6
    },
    {
        "name":"SVN",
        "description":"A server/client Source Code Management toolkit",
        "categories":['instrumentation','data-analysis','backend','frontend'],
        "years_of_experience":5,
        "slug":"svn",
        "importance":5
    },


    #
    # Standards
    #
    {
        "name":"HTML/HTML5",
        "description":"The markup language used primarily for web applications",
        "categories":['frontend'],
        "years_of_experience":6,
        "slug":"html",
        "importance":10
    },
    {
        "name":"XML",
        "description":"The markup language used oftentimes to transmit structured data--the superset of HTML",
        "categories":['frontend','backend'],
        "years_of_experience":6,
        "slug":"xml",
        "importance":7
    },
    {
        "name":"JSON",
        "description":"A standard used for exchanging structured data based on the syntax for objects in Javascript",
        "categories":['frontend','backend'],
        "years_of_experience":4,
        "slug":"json",
        "importance":5
    },
    {
        "name":"CSS/CSS3",
        "description":"The stylesheet language used primarily for styling web pages (but also used in other applications)",
        "categories":['frontend'],
        "years_of_experience":6,
        "slug":"css",
        "importance":10
    },
    {
        "name":"LESS",
        "description":"An alternative to CSS for styling web pages--compiles to css",
        "categories":['frontend'],
        "years_of_experience":1,
        "slug":"less",
        "importance":7
    },
    {
        "name":"VME",
        "description":"A standard used for communicating with scientific instrumentation",
        "categories":['instrumentation'],
        "years_of_experience":6,
        "slug":"vme",
        "importance":4
    },
    {
        "name":"REST",
        "description":"REpresational State Transfer - An Architectural standard for developing HTTP-based APIs",
        "categories":['backend'],
        "years_of_experience":4,
        "slug":"rest",
        "importance":6
    },
    #
    # Math, Statistics, etc.
    #
    {
        "name":"Statistical Modeling",
        "description":"Using statistical theory to measure or predict the behavior of a system",
        "categories":['instrumentation','data-analysis'],
        "years_of_experience":6,
        "slug":"statistical-modeling",
        "importance":7
    },
    {
        "name":"Advanced Mathematics",
        "description":"I have an education in math equivalent to a PhD in Physics",
        "categories":['instrumentation','data-analysis'],
        "years_of_experience":6,
        "slug":"advanced-mathematics",
        "importance":7
    },
    {
        "name":"Device Physics",
        "description":"Understanding of the physics behind modern sensor technology",
        "categories":['instrumentation','data-analysis'],
        "years_of_experience":6,
        "slug":"device-physics",
        "importance":5
    },
    {
        "name":"MATLAB",
        "description":"A software toolkit for numerically analyzing data",
        "categories":['instrumentation','data-analysis'],
        "years_of_experience":2,
        "slug":"matlab",
        "importance":3
    },

    #
    # Software Development Practices
    #
    {
        "name":"SCRUM/Agile",
        "description":"A team-oriented and adaptive approach to software development",
        "categories":['instrumentation','data-analysis','backend','frontend'],
        "years_of_experience":2,
        "slug":"scrum",
        "importance":9
    },
    {
        "name":"Test-Driven Development",
        "description":"A software development methodolgy in which the developer defines the target functionality through unit tests before implementing the functionality",
        "categories":['backend','frontend'],
        "years_of_experience":2,
        "slug":"tdd",
        "importance":6
    },

    #
    # Project management
    #
    {
        "name": "Technical Project Management",
        "description": "The management of technical projects",
        "categories": ['management'],
        "years_of_experience": 6,
        "slug": "project-management",
        "importance": 10
    }

)
for skill in SKILLS:
    s,created = Skill.objects.get_or_create(
        name=skill["name"],
        description = skill["description"],
        years_of_experience = skill["years_of_experience"],
        slug = skill["slug"],
        importance = skill["importance"],
        primary_category = SkillCategory.objects.get(slug = skill["categories"][0])
    )
    for slug in skill["categories"]:
        s.categories.add(SkillCategory.objects.get(slug=slug))

WORK_EXPERIENCE = (
    {
        "employer":"Soar Technology",
        "position":"Sr. Artificial Intelligence Engineer",
        "start_date":datetime.date(year=2012,month=4,day=16),
        "end_date":datetime.date(year=2014,month=1,day=1),
        "description":"""
        Managed projects, wrote proposals (primarily to DoD), pitched new project ideas, and wrote software for a government contractor specializing in Artificial Intelligence.
        """,
        "skills":['java','python','mysql','sql','mongodb','html','scrum','rabbitmq','css','js','jquery','less','rest','statistical-modeling', 'project-management'],
        "slug":"soartech",
        "importance":21
    },
    {
        "employer":"Global Dressage Analytics",
        "position":"Cofounder",
        "start_date":datetime.date(year=2011,month=2,day=1),
        "end_date":datetime.date(year=2014,month=1,day=1),
        "description":"""
        Responsible for the engineering aspects of developing a web-based analytics toolkit for dressage athletes, judges, and trainers.
        """,
        "skills":['python','django','mysql','sql','mongodb','html','scrum','rabbitmq','celery','css','js','jquery','less','rest','statistical-modeling','tdd'],
        "slug":"gda",
        "importance":20
    },
    {
        "employer":"University of Tennessee",
        "position":"Software Engineer (Contractor)",
        "start_date":datetime.date(year=2011,month=12,day=1),
        "end_date":datetime.date(year=2012,month=3,day=1),
        "description":"""
        Designed software for interacting with the Pixel Luminosity Telescope, a next-generation particle tracking experiment based on monocrystalline diamond detectors.
        """,
        "skills":['django','python','cpp','java','html','css','js','vme','device-physics','xml','json','svn'],
        "slug":"ut-contractor",
        "importance":19
    },
    {
        "employer":"La Casa Del Sol",
        "position":"Lead Developer (Contractor)",
        "start_date":datetime.date(year=2010,month=4,day=1),
        "end_date":datetime.date(year=2010,month=10,day=1),
        "description":"""
        Developed web presence and web application for a real estate business based in Barcelona, Spain.
        """,
        "skills":['php','mysql','html','css','js','jquery'],
        "slug":"lacasadelsol",
        "importance":18
    },
    {
        "employer":"University of Tennessee",
        "position":"Programmer/Research Assistant",
        "start_date":datetime.date(year=2008,month=8,day=1),
        "end_date":datetime.date(year=2011,month=12,day=1),
        "description":"""
        Designed control, instrument driver, visualization, and analysis software for the Pixel Luminosity Telescope, a next-generation particle tracking experiment based on monocrystalline diamond detectors.
        """,
        "skills":["python","cpp","java","vme","device-physics","statistical-modeling","advanced-mathematics",],
        "slug":"gra",
        "importance":17
    },
    {
        "employer":"University of Tennessee",
        "position":"Research Assistant",
        "start_date":datetime.date(year=2006,month=10,day=1),
        "end_date":datetime.date(year=2008,month=8,day=1),
        "description":"""
        Developed software and implemented high performance computing infrastructure for both the University of Tennessee Physics Department and the Compact Muon Solenoid experiment at the Large Hadron Collider at CERN.
        """,
        "skills":['java','cpp','spring','servlets','xml','corba','swing','python'],
        "slug":"ura",
        "importance":12
    },
    {
        "employer":"University of Tennessee",
        "position":"Lab Assistant",
        "start_date":datetime.date(year=2005,month=12,day=1),
        "end_date":datetime.date(year=2006,month=10,day=1),
        "description":"""
        Developed software applications to run the equipment used by students in physics lab classes.
        """,
        "skills":['labview','matlab','device-physics','advanced-mathematics'],
        "slug":"ula",
        "importance":12
    },
)
for we in WORK_EXPERIENCE:
    work_experience,created = WorkExperience.objects.get_or_create(
        employer=we["employer"],
        position=we["position"],
        start_date=we["start_date"],
        end_date=we["end_date"],
        description=we["description"],
        slug=we["slug"],
        importance=we["importance"]
    )
    for skill in we["skills"]:
        work_experience.skills.add(Skill.objects.get(slug=skill))

CONTRIBUTIONS = (
    #
    # GDA
    #
    {"description":"Designed the architecture for the web application from the ground up","experience":"gda","importance":15},
    {"description":"Developed the analysis algorithms to reduce large score data sets (several million scores) into performance parameters that can be easily understood by the user","experience":"gda","importance":12},
    {"description":"Made new visualizations (based on Javascript) to quickly communicate the results of the analysis to the user","experience":"gda","importance":13},
    {"description":"Implemented a predictive analysis to allow users to project their performance to some time in the future","experience":"gda","importance":10},
    {"description":"Helped create the frontend for the web application (html/javascript/css)","experience":"gda","importance":9},
    {"description":"Designed and implemented an asynchronous precalculation and caching mechanism to increase performance in the case where an analysis that a user may wish to view takes more than a few seconds","experience":"gda","importance":8},

    #
    # UT - Contractor
    #
    {"description":"Created a web-based user interface (based on Django) to provide operators with a simple-to-use tool to run the powerup routines, calibrations, and data runs","experience":"ut-contractor","importance":12},
    {"description":"Made python bindings for the existing C++ infrastructure (which I also built)","experience":"ut-contractor","importance":10},
    {"description":"Trained a new graduate student on how to run and develop the web-based user interface that I made","experience":"ut-contractor","importance":9},

    #
    # La Casa Del Sol
    #
    {"description":"Developed a Joomla! plugin which allowed La Casa del Sol's employees to maintain and display a list of apartments which they represented","experience":"lacasadelsol","importance":14},
    {"description":"Implemented the internationalization infrastructure, which supported English, Spanish, and Russian","experience":"lacasadelsol","importance":12},
    {"description":"Created a pure javascript slideshow plugin which integrated layers of static navigation","experience":"lacasadelsol","importance":8},


     #
     # GRA
     # 
     {"description":"Designed and implemented calibration algorithms for intelligently tuning instrument operational parameters","experience":"gra","importance":14},
     {"description":"Created and implemented the data acquisition framework","experience":"gra","importance":12},
     {"description":"Managed system tests (~15 people present) in particle beams to measure fundamental parameters of diamond detectors, such as resolution, charge collection depth, efficiency, and sensor lifetime","experience":"gra","importance":11},
     {"description":"Designed the web-based detector monitoring framework for the CMS Beam and Radiation Monitoring (BRM) group, which was the first place where beam was seen in CMS","experience":"gra","importance":10},
     {"description":"Analyzed the data taken by a diamond-based monitoring device called the Beam Conditions Monitor 1L (BCM1L) to measure important parameters such as the minimum sensitivity, which were in turn used to set beam abort conditions for CMS","experience":"gra","importance":9},

     #
     # URA
     #
     {"description":"Implemented a distributed file system (Lustre) on a Beowulf cluster used for physics analyses","experience":"ura","importance":14},
     {"description":"Created the real-time instrument monitoring framework for the CMS BRM group","experience":"ura","importance":12},
     {"description":" Developed a software package for transferring data from instruments to displays over the network in real-time","experience":"ura","importance":11},
     {"description":"Developed a scalable mechanism for monitoring errors in the 66 million pixel channels in the CMS Pixel detector","experience":"ura","importance":10},

     #
     # ULA
     #
     {"description":"Created a hardware/software solution for measuring and visualizing electric fields on conducting paper","experience":"ula","importance":14},
     {"description":"Implemented control software for controlling an X-ray machine for use in a Bragg diffraction experiment","experience":"ula","importance":12},
     {"description":"Developed control software to control a Cesium heatpipe experiment","experience":"ula","importance":11},
     {"description":"Made an application for measuring Compton scattering by controlling a stepper motor, radiation detector, and a gamma source","experience":"ula","importance":10},
     {"description":"Helped to setup laboratory experiments","experience":"ula","importance":9},
)

for con in CONTRIBUTIONS:
    contribution, created = Contribution.objects.get_or_create(
        description = con["description"],
        experience = WorkExperience.objects.get(slug=con["experience"]),
        importance = con["importance"]
    )

PROJECTS = (
    {
        "name":"Generalized Unilateral Transfer Server (GUTS)",
        "start_date":datetime.date(month=1,year=2007,day=1),
        "end_date":datetime.date(month=6,year=2007,day=1),
        "description":"""
            GUTS is a library, used by CERN's Compact Muon Solenoid Experiment, which serializes arbitrary java objects and transfers them to a list of connected clients for processing.
            The primary use of this library is to transfer data between two distinct networks: CERN's Large Hadron Collider Machine Network, and the Compact Muon Solenoid network.
            This library works only one way--i.e., the protocol accepts no direct feedback from the clients--in order to satisfy the strict security standards required by CERN management
            for software which bridges the two networks.  
        """,
        "work_experience":"ura",
        "skills":["java","python","cpp",'corba','spring','maven','eclipse','svn'],
        "slug":"guts",
        "importance":3,
        "thumbnail":"images/guts/guts-architecture.png"
    },
    {
        "name":"Beam and Radiation Monitoring Realtime Display Framework",
        "start_date":datetime.date(month=6,year=2007,day=1),
        "end_date":datetime.date(month=7,year=2008,day=1),
        "description":"""
            The Beam and Radition Monitoring (BRM) realtime display framework takes the highly important radiation monitoring data which comes from the BRM subsystems and displays
            it in such a way that shifters can monitor it 24/7 to make machine-safety decisions based upon the displayed data.  
        """,
        "work_experience":"ura",
        "skills":["java","python","cpp",'velocity','spring','maven','eclipse','svn','swing','css','xml','js'],
        "slug":'brm-display',
        "importance":5,
        "thumbnail":"images/brm-display/brm-sample-display.png"
    },
    {
        "name":"DIP-Cache: A realtime online cache for instrument monitoring data",
        "start_date":datetime.date(month=9,year=2007,day=1),
        "end_date":datetime.date(month=12,year=2007,day=1),
        "description":"""
            DIP-Cache is a realtime data caching server which accepts data coming from any source that publishes its data through the Data Interchange Protocol (a CERN standard communication protocol).
            In addition to simply caching data as it comes in, it responds to queries which allow the user to limit the data length, select the most recent time stamp, choose a specific instrument ID, etc.  
        """,
        "work_experience":"ura",
        "skills":["java","python","cpp",'spring','maven','eclipse','svn','xml','servlets','rest'],
        "slug":'dipcache',
        "importance":5,
        "thumbnail":"images/dipcache/dipcache-architecture.png"
    },
    {
        "name":"Beam and Radiation Monitoring Data Logging and Analysis Framework",
        "start_date":datetime.date(month=4,year=2008,day=1),
        "end_date":datetime.date(month=10,year=2008,day=1),
        "description":"""
            The BRM Data Logging and Analysis Framework takes data from a number of sources--my GUTS framework, a CORBA-based CERN standard protocol called CMW, and another CERN-standard protocol called DIP--and
            logs the data to files, which are nightly archived to deep storage through CERN's heirarchial storage solution called CASTOR.  After the data is archived, it is analyzed using a 
            ROOT-based data analysis package which can extract various instrument performance parameters.  
        """,
        "work_experience":"gra",
        "skills":["java","python","cpp",'spring','maven','eclipse','svn','xml'],
        "slug":'brm-data',
        "importance":4,
        "thumbnail":"images/brm-data-framework/brm-data-architecture.png"
    },
    {
        "name":"Introduction to Modern Data Analysis with LabVIEW and MATLAB",
        "start_date":datetime.date(month=2,year=2006,day=1),
        "end_date":datetime.date(month=4,year=2006,day=1),
        "description":"""
            I was commissioned to write a laboratory exercise for use in the University of Tennessee Modern Physics Laboratory which could teach
            students how to use LabVIEW and MATLAB together to interact with and analyze lab instrumentation.  
        """,
        "work_experience":"ula",
        "skills":['labview','matlab','device-physics'],
        "slug":'intro-modern',
        "importance":3,
        "thumbnail":"images/intro-modern-daq/v-vs-y-vs-x.png"
    },
    {
        "name":"Data Acquisition and Calibration Framework for the Pixel Luminosity Telescope",
        "start_date":datetime.date(month=10,year=2008,day=1),
        "end_date":datetime.date(month=8,year=2011,day=1),
        "description":"""
            The Pixel Luminosity Telescope (PLT) is a next-generation diamond detector which uses the same complex and highly advanced readout electronics as the
            Compact Muon Solenoid's (CMS) Pixel Detector System.  Calibrating and operating the system is a complex exercise, and I was commissioned to help design 
            the software and firmware to deal with it.  
        """,
        "work_experience":"gra",
        "skills":["python","cpp",'svn','xml','scons','vme','statistical-modeling','device-physics'],
        "slug":'plt-daq',
        "importance":6,
        "thumbnail":"images/plt-daq/plt-teststand.jpg"
    },
    {
        "name":"Web-based Control System for the Pixel Luminosity Telescope",
        "start_date":datetime.date(month=6,year=2011,day=1),
        "end_date":None,
        "description":"""
            The Pixel Luminosity Telescope (PLT) is a next-generation diamond detector which uses the same complex and highly advanced readout electronics as the
            Compact Muon Solenoid's (CMS) Pixel Detector System.  Operating the control software by hand is difficult for someone who has less than a few years
            of experience with the detector.  Therefore, it was necessary to create a user interface which is easy enough for anyone to use to operate the system, log its state at any given time,
            and do quality assurance on the data that comes out of the detector.  I was commissioned to design and implement this UI using web-based tools.
        """,
        "work_experience":"ut-contractor",#
        "skills":["python","cpp",'svn','xml','django','scons','html','css','js','jquery','sqlite','mysql','json'],
        "slug":'plt-ui',
        "importance":10,
        "thumbnail":"images/plt-ui/header.png"
    },
    {
        "name":"Drivers, Data Acquisition System, and User Interface for the Zurich Microstrip Telescope",
        "start_date":datetime.date(month=2,year=2010,day=1),
        "end_date":datetime.date(month=6,year=2011,day=1),
        "description":"""
            The Zurich Beam Telescope is a silicon micostrip tracker capable of delivering 1 micrometer resolution for 
            localizing charged particles which pass through it.  This high resolution is useful for studing the characteristics
            of many other particle detectors, which may be inserted inside of the assembly to provide detailed studies of
            the spatial behavior of the instrument.
        """,
        "work_experience":"gra",
        "skills":["python","cpp",'vme'],
        "slug":'zurich-beam-telescope',
        "importance":8,
        "thumbnail":"images/zurich-beam-telescope/matt_zbt.png"
    },
    {
        "name":"Performance Testing and Analysis for Next-Generation Diamond-Based Particle Detectors",
        "start_date":datetime.date(month=1,year=2008,day=1),
        "end_date":datetime.date(month=8,year=2011,day=1),
        "description":"""
            Diamond is a radiation-hard and heat-tolerant material, which makes it useful as sensor material in harsh environments such as
            those found in modern particle accelerator interaction regions.  I have helped to quantify properties such as spatial resolution, 
            charge collection depth, and the Lorentz Angle in lab-grown
            diamonds to establish their suitability for different applications.
        """,
        "work_experience":"gra",
        "skills":["python","cpp",'advanced-mathematics','svn','xml','scons','vme','statistical-modeling','device-physics'],
        "slug":'diamond',
        "importance":10,
        "thumbnail":"images/diamond/sipix.jpg"
    },
    {
        "name":"Web Presence for La Casa del Sol (lacasadesol.com)",
        "start_date":datetime.date(year=2010,month=4,day=1),
        "end_date":datetime.date(year=2010,month=10,day=1),
        "description":"""
            La Casa del Sol (unfortunately now out of business due to the owner having to leave Barcelona) was a real estate business which
            helped connect prospective buyers/renters to condos/apartments located in Barcelona, Spain.  They relied on a web application
            which I designed that allowed them to make a searchable list of apartments which they represented.
        """,
        "work_experience":"lacasadelsol",
        "skills":["php",'joomla','html','css','js','jquery','mysql','json','sql','mysql'],
        "slug":'lacasadelsol',
        "importance":12,
        "thumbnail":"images/lacasadelsol/whole-site.png"
    },
    {
        "name":"Global Dressage Analytics (dressageanalytics.com)",
        "start_date":datetime.date(month=2,year=2011,day=1),
        "end_date":None,
        "description":"""
            dressageanalytics.com is a web application which allows atheletes who participate in the equestrian sport of dressage
            to track their progress, predict their future performance, get training suggestions, and compare their performance with that
            of their peers.
        """,
        "work_experience":"gda",
        "skills":["python",'git','mercurial','xml','js','django','scons','html','css','jquery','sqlite','mysql','json','celery','rabbitmq','sql','mysql','sqlite','mongodb','jquery','statistical-modeling','scrum','rest','tdd'],
        "slug":'gda',
        "importance":20,
        "thumbnail":"images/gda/gda-front-page.png"
    },
)

for project in PROJECTS:
    p,created = Project.objects.get_or_create(
        name=project["name"],
        start_date=project["start_date"],
        end_date=project["end_date"],
        description=project["description"],
        work_experience=WorkExperience.objects.get(slug=project["work_experience"]),
        slug=project["slug"],
        importance=project['importance']
    )
    if project.has_key("thumbnail"):
        filename = project.get("thumbnail")
        with open(filename) as img:
            p.thumbnail.save(os.path.split(filename)[1], ContentFile(img.read()))

    for skill in project["skills"]:
        p.skills.add(Skill.objects.get(slug=skill))

AWARDS = (
    {"name":"Chancellor's Citation: Professional Promise","year_awarded":2011,"awarded_by":"University of Tennessee - Knoxville","description":""},
    {"name":"Sigma Pi Sigma Honors Society","year_awarded":2008,"awarded_by":"University of Tennessee - Knoxville","description":""},
    {"name":"Outstanding Undergraduate in Physics: Academic Achievement","year_awarded":2008,"awarded_by":"University of Tennessee - Knoxville","description":""},
    {"name":"Douglass V. Roseberry Award","year_awarded":2008,"awarded_by":"University of Tennessee - Knoxville","description":""},
    {"name":"Chancellor's Citation: Academic Achievement","year_awarded":2008,"awarded_by":"University of Tennessee - Knoxville","description":""},
    {"name":"Top Collegiate Scholar","year_awarded":2008,"awarded_by":"University of Tennessee - Knoxville","description":""},
)

for award in AWARDS:
    Award.objects.get_or_create(
        name=award["name"],
        year_awarded=award["year_awarded"],
        awarded_by=award["awarded_by"],
        description=award["description"]
    )

PUBLICATIONS = (
    {
        "citation":"""“Results from a beam test of a prototype PLT diamond pixel telescope,” R. Hall-Wilton et al., Nuclear Instruments and Methods in Physics Research Section A, doi:10.1016/j.nima.2010.04.097""",
        "date":datetime.date(year=2010,month=4,day=1),
        "primary_author":False
    },
    {
        "citation":"""“Commissioning and Performance of the CMS Pixel Tracker with Cosmic Ray Muons,” Serguei Chatrchyan et al. (CMS Collaboration), JINST 5:T03007,2010.""",
        "date":datetime.date(year=2010,month=1,day=1),
        "primary_author":False,
    },
    {
        "citation":"""“Studies of mono-crystalline CVD diamond pixel detectors”, W. Bugg et. al, Nuclear Instruments and Methods in Physics Research Section A: Accelerators, Spectrometers, Detectors and Associated Equipment, In Press, Corrected Proof, Available online 24 December 2010, ISSN 0168-9002, DOI: 10.1016/j.nima.2010.12.161.""",
        "date":datetime.date(year=2010,month=12,day=4),
        "primary_author":True
    },
    {
        "citation":"""“Performance of a single-crystal diamond-pixel telescope,” R. Hall-Wilton et al., PoS RD09:027,2009.""",
        "date":datetime.date(year=2010,month=12,day=4),
        "primary_author":True,
    },
    {
        "citation":"""“Diamond detectors for radiation and luminosity measurements in CMS,” R. Hall-Wilton et al., Nuclear Science Symposium Conference Record (NSS/MIC), 2009 IEEE""",
        "date":datetime.date(year=2009,month=11,day=4),
        "primary_author":True,
    },
    {
        "citation":"""“The CMS experiment at the CERN LHC”, CMS Collaboration (R. Adolphi et al.), JINST 0803:S08004, 2008, JINST 3:S08004, 2008.""",
        "date":datetime.date(year=2008,month=8,day=1),
        "primary_author":False,
    },
    {
        "citation":"""“Display Framework Documentation for Beam and Radiation Monitoring Group.” CMS Detector Note.""",
        "date":datetime.date(year=2009,month=9,day=1),
        "primary_author":True,
    },
    {
        "citation":"""“GUTS (Generalized Unilateral Transfer Server).” CMS Internal Note.""",
        "date":datetime.date(year=2007,month=4,day=1),
        "primary_author":True,
    },
)

for publication in PUBLICATIONS:
    Publication.objects.get_or_create(
        citation = publication["citation"],
        date = publication["date"],
        primary_author = publication["primary_author"]
    )
