# Django settings for gda_web project.
import sys
import matt_cv as base_settings

try:
    import matt_cv.settings as base_settings
except ImportError:
    print """
    -------------------------------------------------------------------------
    You need to create a base_settings.py file which needs to contain at least
    database connection information.

    Copy local_settings_example.py to local_settings.py and edit it.
    -------------------------------------------------------------------------
    """
    import sys
    sys.exit(1)
else:
    # Import any symbols that begin with A-Z. Append to lists any symbols that
    # begin with "EXTRA_".
    import re
    for attr in dir(base_settings):
        match = re.search('^EXTRA_(\w+)', attr)
        if match:
            name = match.group(1)
            value = getattr(base_settings, attr)
            try:
                globals()[name] += value
            except KeyError:
                globals()[name] = value
        elif re.search('^[A-Za-z]', attr):
            globals()[attr] = getattr(base_settings, attr)


DEBUG = False

STATICFILES_DIRS += (
        '/var/www',
    )
