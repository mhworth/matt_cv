import os

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib import files, console
from fabric import utils
from fabric.decorators import hosts
from fabric.contrib.files import exists
from fabric.context_managers import *
from contextlib import contextmanager
import glob
import fabric.contrib.files as files
from subprocess import Popen


RSYNC_EXCLUDE = (
    '.DS_Store',
    '.hg',
    '.git',
    '*.example',
    '*.db',
    'media/admin',
    'media/attachments',
    'local_settings.py',
    'fabfile.py',
    'bootstrap.py',
    'local_backup',
    'media',
    'gda_web/media',
    '.*'
)

DIST_PACKAGES = ['python2.7-dev',
 'python-virtualenv',
 'libmysqlclient-dev',
 'build-essential',
 'graphviz',
 'memcached',
 'libmemcached-dev',
 'libjpeg8-dev',
 'libz-dev',
 'libfreetype6-dev',
 'vim',
 'memcached',
 'mysql-server',
 'apache2',
 'libapache2-mod-wsgi',
 'rdiff-backup',
 'denyhosts',
 'rsync',
]  

#
# Environments
#
def staging():
    """ 
    Use staging environment on remote host.  Sets host up to run a staged version on an empty linode.
    """
    #env.user = 'gda'
    env.home = '/opt/local'
    env.run_user = 'www-data'
    env.project_root = '/opt/local'
    env.project_home = '%(project_root)s/matt_cv'%env
    env.environment = 'staging'
    env.hosts = ['192.168.1.11']
    env.virtualenv_root = os.path.join(env.project_root, 'BASELINE')
    env.activate = 'source %(virtualenv_root)s/bin/activate' % env
    env.settings = 'matt_cv.settings_production'
    env.backup_root = '/local/backup'

def production():
    """ 
    Use production environment on remote host
    """
    env.home = '/opt/local'
    env.run_user = 'www-data'
    env.project_root = '/opt/local'
    env.project_home = '%(project_root)s/matt_cv'%env
    env.environment = 'production'
    env.hosts = ['ec2-184-73-40-133.compute-1.amazonaws.com']
    env.virtualenv_root = os.path.join(env.project_root, 'BASELINE')
    env.activate = 'source %(virtualenv_root)s/bin/activate' % env
    env.settings = 'matt_cv.settings_production'
    env.backup_root = '/local/backup'

#
# Service management
#
def stop_services():
    for v in [apache2,memcached]:
        v("stop")

def apache2(action):
    sudo("/etc/init.d/apache2 %s"%action)

def memcached(action):
    sudo("/etc/init.d/memcached %s"%action)

def mysql(action):
    sudo("/etc/init.d/mysql %s"%action)

def start_services():
    for v in [apache2,memcached,mysql]:
        v("start")
#
# File management
#
def upload_code():
    ""
    if not hasattr(env,"environment"):
        print "Must specify an environment, exiting."
        return

    sudo("chown -R %(user)s %(project_root)s"%env)
    extra_opts = '--omit-dir-times --prune-empty-dirs'
    rsync_project(
        env.project_root,
        exclude=RSYNC_EXCLUDE,
        delete=True,
        extra_opts=extra_opts,
    )

def collectstatic():
    require('activate', provided_by=('staging','production'))
    require('run_user', provided_by=('staging','production'))
    require('project_home', provided_by=('staging','production'))

    DROPBOX = os.environ["DROPBOX"]
    dest = '/var/www/'
    extra_opts = '--omit-dir-times --prune-empty-dirs'
    sudo("chown -R %(user)s /var/www"%env)
    rsync_project(dest,delete=True,exclude=RSYNC_EXCLUDE, local_dir=os.path.join(DROPBOX,"Documents","applications","cv","projects"),extra_opts=extra_opts)

    with prefix(env.activate):
        sudo("DJANGO_SETTINGS_MODULE=%(settings)s PYTHONPATH=%(project_root)s django-admin.py collectstatic --noinput"%env,user=env.run_user)

 

#   
# Configuration management
#
def configure():
    configure_apache()

def configure_apache():

    put("conf/matt_cv","/etc/apache2/sites-available/matt_cv",use_sudo=True)

    # Make sure port 8001 is enabled
    files.comment("/etc/apache2/ports.conf","NameVirtualHost *:8001",use_sudo=True)
    files.comment("/etc/apache2/ports.conf","Listen 8001",use_sudo=True)

def enable_production():
    with cd("/etc/apache2/sites-available"):
        sudo("a2dissite *")

    sudo("a2ensite matt_cv")
    apache2("reload")

def set_permissions():

    # if not exists("/var/log/gda"):
    #     sudo("mkdir /var/log/gda")
    # if not exists("/var/log/celery"):
    #     sudo("mkdir /var/log/celery")
    # sudo("chown -R www-data /var/log/gda")
    # sudo("chown -R www-data /opt/local/gda")
    # sudo("chgrp -R gda /var/log/gda")
    # sudo("chgrp -R gda /var/log/celery")
    # sudo("chgrp -R gda /opt/local/gda")
    # sudo("chmod -R ug+rwX /var/log/gda")
    # sudo("chmod -R ug+rX /opt/local/gda")
    with settings(warn_only=True):
        sudo("mkdir -p /opt/local/matt_cv/static")
        sudo ("chown -R www-data /opt/local/matt_cv/static")

#
# Database Management
#
def create_db():
    ''
    require('project_home', provided_by=('staging','production'))
    with cd("%(project_home)s"%env):
        run("mysql -u root -p < sql/create-db.sql")
def init_db():
    require('project_home', provided_by=('staging','production'))
    with cd("%(project_home)s"%env):
        django_admin("syncdb --noinput")
        cmd = env.activate + " && " + "bash scripts/create.sh"
        sudo(cmd)
def drop_db():
    require('project_home', provided_by=('staging','production'))
    require('activate', provided_by=('staging','production'))
    require('run_user', provided_by=('staging','production'))
    with cd("%(project_home)s"%env):
        try:
            run("mysql -u root -p < sql/drop-db.sql")
        except:
            pass

def install_dist_packages():

    cmd = ['apt-get install','-y'] + DIST_PACKAGES
    sudo(' '.join(cmd))

def create_virtualenv():
    require('virtualenv_root', provided_by=('staging','production'))

    if not exists(env.virtualenv_root):
        sudo("virtualenv --python=python2.7 %(virtualenv_root)s"%env)

def update_virtualenv():
    require('activate', provided_by=('staging','production'))
    require('virtualenv_root', provided_by=('staging','production'))
    require('project_root', provided_by=('staging','production'))
    cmd = env.activate + " && " + ' '.join(["pip", "install", "--requirement",
        os.path.join(env.project_root,'matt_cv', 'requirements.txt')]) 
    sudo(cmd)

def deploy():
    if env.environment == 'production':
        if not console.confirm('Are you sure you want to deploy production?',
                               default=False):
            utils.abort('Production deployment aborted.')
        else:
            deploy_production()
    elif env.environment == 'staging':
        deploy_staging()
    elif env.environment == 'integration':
        deploy_integration()

def deploy_integration():
    deploy_staging()

def deploy_staging():
    """ 
    Rsync code to remote host 
    """
    require('run_user', provided_by=('staging','production'))
    require('environment', provided_by=('staging','production'))
    do_create_db = console.confirm('Would you like to drop/recreate the DB?', default=False)
    create_users()
    create_groups() 
    install_dist_packages()
    create_directory_structure()
    stop_services()
    apache2("start")
    upload_code()
    configure()
    create_virtualenv()
    update_virtualenv()
    set_permissions()
    if do_create_db:
        drop_db()
        create_db()
    collectstatic()
    enable_production()# Make sure the site is enabled
    start_services()
    set_permissions()
    if do_create_db:
        init_db()
            
    
def deploy_production():
    ""

    # At the moment, do the same thing as the staging env, maybe do something different later
    deploy_staging()

def create_directory_structure():
    require('project_root', provided_by=('staging', 'production'))
    require('backup_root', provided_by=('staging', 'production'))

    if not exists(env.project_root):
        sudo("mkdir -p %(project_root)s"%env)
    
    if not exists(env.backup_root):
        sudo("mkdir -p %(backup_root)s"%env)
    
    if not exists(os.path.join(env.project_home,"static")):
        sudo("mkdir -p %(project_home)s/static"%env)
#
# Various admin tasks
#
def update_requirements():
    """ update external dependencies on remote host """
    require('run_user', provided_by=('run_user','production'))
    requirements = os.path.join(env.project_root,"matt_cv", 'requirements.txt')
    with cd(requirements):
        cmd = ['pip install']
        cmd += ['-E %(virtualenv_root)s' % env]
        cmd += ['--requirement %s' % requirements]
        sudo(' '.join(cmd),user=env.run_user)


def runserver():
    """
    Runs a django dev server on the remote
    """
    require('code_root',provided_by=('staging','production'))
    require('activate',provided_by=('staging','production'))
    require('environment',provided_by=('staging','production'))
    
    SETTINGS = "gda_web.settings_%s "% env.environment
    with cd(env.code_root):
        sudo( env.activate + " && " + " python manage.py runserver --settings=%s dressageanalytics.com:8001"%SETTINGS,user=env.run_user)
        
def django_admin(args):
    require('activate',provided_by=('staging','production'))
    require('environment',provided_by=('staging','production'))
    with cd(env.project_home):
        sudo(env.activate + " && DJANGO_SETTINGS_MODULE=%s PYTHONPATH=%s django-admin.py %s"%(env.settings, env.project_root,args))

def syncdb():
    django_admin("syncdb")

def shell():
    django_admin("shell")

def createsuperuser():
    """
    Runs a django dev server on the remote
    """
    django_admin("createsuperuser")

@contextmanager  
def mkdtemp(user="root"):
    tempdir = sudo('python -c "import tempfile; print tempfile.mkdtemp();"',user=user)
    tempdir = tempdir.strip()
    yield tempdir
    sudo("rm -rf %s"%tempdir)

    # with cd("/tmp"):
    #     now = datetime.datetime.now()
    #     ts = now.strftime("%Y-%m-%d_%H-%M-%S")
    #     filename = os.path.join("/","tmp","gda_file_upload"+ts)
    #     sudo("mkdir -p")

def user_exists(username):
    with settings(warn_only=True):
        retval = run("id %s"%username)
        return retval.return_code==0

def create_groups():
    groups = []
    for g in groups:
        with settings(warn_only=True):
            sudo("groupadd %s"%g)

def create_users():
    users = ['matt_cv']
    for user in users:
        if not user_exists(user):
            create_user(user)

def create_user(username,is_system=True):
    if is_system:
        return sudo("useradd -r %s"%username)
    else:
        return sudo("useradd %s"%username)


