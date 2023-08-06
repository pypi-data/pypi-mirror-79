# -*- python -*-
####################
# in order to configure for your site without interfering with
# settings.py as shipped in the git repo, you can use this file
# as a template for a file that you have to name sitesettings.py
# in the same directory as settings.py
####################

# filename extensions that are expected to possibly hold notebooks
# since using jupytext, this is no longer limited to '.ipynb'
notebook_extensions = ['ipynb', 'py', 'md']

# as of 0.18.0 only 'https' is supported for server_mode
# this means the system will accept ONLY https requests
# i.e. http incoming requests are redirected to https
# note that official sites like fun-mooc.fr can themselves
# be reached only over https, and will thus refuse
# to fetch a nbhosting iframe over http
server_mode = "https"

# for the nginx config
server_name = "nbhosting.inria.fr"
ssl_certificate = "/root/ssl-certificate/bundle.crt"
ssl_certificate_key = "/root/ssl-certificate/nbhosting.inria.fr.key"


# the location used by the application
# typically where you have a big fat btrfs filesystem
# our main deployment at Inria uses /nbhosting/current that is
# a symlink to either /nbhosting/prod or /nbhosting/dev
nbhroot = '/Users/tparment/git/nbhosting/django/fake-root/'

# the location where the application is installed
# i.e. the place where you have git clone'd it before
# running ./install.sh
srcroot = '/Users/tparment/git/nbhosting'

# the location where podman is told to store its images and all other files
# it should point into a btrfs partition
# if you upgrade from 0.24 or earlier you should keep this default value
# that was previously hard-wired
podmanroot = '/nbhosting/containers'

### upstream portals
#
# trusting an upstream portal needs both next settings
# first is for django, second for jupyter
#
# the domains that we accept being a sub iframe of, typically
# 'self' (with the single quotes)
#    that allows nbhosting to work in classroom mode
#    where local pages include notebooks
# *.fun-mooc.fr
#    would allow to run as a companion to FUN
# see jupyter/jupyter_notebook_config.py.in
frame_ancestors = [
    "https://*.fun-mooc.fr",
    # if you plan on using nbhosting in classroom mode, this is required
    "'self'",
]

# the domains that are trusted
# typically the edx platform, as well as your own
# SSL-exposed domain name
allowed_referer_domains = [
    # add yourself here so the 'revert_to_original' and
    # 'share_static_version' feature can work properly
    'localhost',
    server_name,
    'fun-mooc.fr',
]

# the IPs of devel boxes
# these will be allowed to send /notebookLazyCopy/ (formerly known as /ipythonExercice/) urls directly
# this is useful for debugging / troubleshooting
allowed_devel_ips = [
    # localhost
    ( 'match', r'127.[\.0-9]+'),
    # home
    ( 'exact', r'82.226.190.44'),
    # work
    ( 'match', r'138\.96\.[0-9]+\.[0-9]+'),
]

######################################## monitor policy
# in minutes
# monitor will run cyclically - every <period> minutes - 
# and kill containers that have been idle for more than <idle> minutes
# depends on your available resources and traffic of course
monitor_idle = 30
monitor_period = 10

######################################## django settings
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# describes how to log stderr from (shell) sub processes
# depending on its returncode
# can be either:
# None : never logs
# True : always log
# False : log when return code != 0

DEBUG_log_subprocess_stderr = False


# see e.g. https://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = 'your-actual-production-key-here'


# this is a native django setting
# see https://docs.djangoproject.com/en/1.11/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    '138.96.112.37',                    # thermals
    'nbhosting-dev.inria.fr',           #
    'thermals.pl.sophia.inria.fr',      #
    '138.96.19.2',                      # nbhosting
    'nbhosting.inria.fr',               #
    'nbhosting.pl.sophia.inria.fr',     #
    'localhost',                        # for devel
]
