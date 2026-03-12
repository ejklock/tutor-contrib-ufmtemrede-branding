from __future__ import annotations

import os.path
from glob import glob

from tutor import env, hooks

from .__about__ import __version__

env.BIN_FILE_EXTENSIONS.append('.json')
env.BIN_FILE_EXTENSIONS.append('.po')

########################################
# CONFIGURATION
########################################

config = {
    # Add here your new settings
    "defaults": {
        "VERSION": __version__,
        "WELCOME_MESSAGE": "Bem vindo ao UFMT em Rede!",
        # Footer links are dictionaries with a "title" and "url"
        # To remove all links, run:
        # tutor config save --set UFMT_EM_REDE_FOOTER_NAV_LINKS=[] --set UFMT_EM_REDE_FOOTER_LEGAL_LINKS=[]
        # {"title": "About", "url": "/about"},
        # {"title": "Contact", "url": "/contact"},
        "FOOTER_NAV_LINKS": [
         
        ],
         # {"title": "Terms of service", "url": "/tos"},
        "FOOTER_LEGAL_LINKS": [
           
        ],
        "BACKGROUND": "#ffffff",
        "BG_PRIMARY": "#ffffff",
        "BODY": "#FFFFFF",
        "PRIMARY": "#311B7B",
        "PRIMARY_LIGHT": "#F2F7F8",
        "SECONDARY":"#454545",
        "HEADER_BACKGROUND":"transparent linear-gradient(180deg, #3A1D98 0%, #1D0F4C 100%) 0% 0% no-repeat padding-box",
        "HEADER_BOX_SHADOW":" 0 6px 10px 0 rgba(0, 0, 0, 0.1)",
        "FONT_FAMILY": "",
        "BRAND": "#311B7B",
        "SUCCESS": "#178253",
        "INFO": "#006DAA",
        "DANGER": "#C32D3A",
        "WARNING": "#FFD900",
        "LIGHT": "#E1DDDB",
        "DRAK": "#111827",
        "LIGHT_DRAK": "#374151",
        "DARK": "#273F2F",
        "ACCENT_A": "#00BBF9",
        "ACCENT_B": "#FFEE88",
        "HOMEPAGE_BG_IMAGE": "",
        # EXTRAS: additional CSS for html theme
        "EXTRAS": "",
        # OVERRIDES: additional CSS for mfe branding
        "OVERRIDES": "",
        "FONTS": "" ,

        # static page templates
        "STATIC_TEMPLATE_404": None,
        "STATIC_TEMPLATE_429": None,
        "STATIC_TEMPLATE_ABOUT": None,
        "STATIC_TEMPLATE_BLOG": None,
        "STATIC_TEMPLATE_CONTACT": None,
        "STATIC_TEMPLATE_DONATE": None,
        "STATIC_TEMPLATE_EMBARGO": None,
        "STATIC_TEMPLATE_FAQ": None,
        "STATIC_TEMPLATE_HELP": None,
        "STATIC_TEMPLATE_HONOR": None,
        "STATIC_TEMPLATE_JOBS": None,
        "STATIC_TEMPLATE_MEDIA_KIT": None,
        "STATIC_TEMPLATE_NEWS": None,
        "STATIC_TEMPLATE_PRESS": None,
        "STATIC_TEMPLATE_PRIVACY": None,
        "STATIC_TEMPLATE_SERVER_DOWN": None,
        "STATIC_TEMPLATE_SERVER_ERROR": None,
        "STATIC_TEMPLATE_SERVER_OVERLOADED": None,
        "STATIC_TEMPLATE_SITEMAP": None,
        "STATIC_TEMPLATE_TOS": None,
        "EXTERNAL_MYSQL_PORT":"33306",
        "EXTERNAL_MYSQL_USER":"external_app",
        "EXTERNAL_MYSQL_PASSWORD":"qZ18z3",
    },
    "unique": {},
    "overrides": {},
}




hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"UFMT_EM_REDE_{key}", value) for key, value in config["defaults"].items()]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"UFMT_EM_REDE_{key}", value) for key, value in config["unique"].items()]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config["overrides"].items())
)


_MFE_BRAND_INSTALLS = """
RUN npm install '@edx/brand@git+https://github.com/ejklock/brand-openedx-indigo.git#inovatec/ulmo'
RUN npm install '@edx/frontend-component-header@npm:@edly-io/indigo-frontend-component-header@^5.0.0'
RUN npm install '@edx/frontend-component-footer@npm:@edly-io/indigo-frontend-component-footer@^3.0.0'
"""

_MFE_BRAND_ONLY = """
RUN npm install '@edx/brand@git+https://github.com/ejklock/brand-openedx-indigo.git#inovatec/ulmo'
"""

hooks.Filters.ENV_PATCHES.add_items(
    [
        ("mfe-dockerfile-post-npm-install-learning", _MFE_BRAND_INSTALLS),
        ("mfe-dockerfile-post-npm-install-authn", _MFE_BRAND_ONLY),
        # Tutor-Indigo v2.1 targets the styling updations in discussions and learner-dashboard MFE
        # brand-openedx is related to styling updates while others are for header and footer updates
        ("mfe-dockerfile-post-npm-install-discussions", _MFE_BRAND_INSTALLS),
        ("mfe-dockerfile-post-npm-install-learner-dashboard", _MFE_BRAND_INSTALLS),
        ("mfe-dockerfile-post-npm-install-profile", _MFE_BRAND_INSTALLS),
        ("mfe-dockerfile-post-npm-install-account", _MFE_BRAND_INSTALLS),
    ]
)
################# Initialization tasks
# To run the script from templates/panorama/tasks/myservice/init, add:
def add_init_tasks(location):
    with open(
        os.path.join(os.path.dirname(__file__), "templates", "tasks", location, "init"),
        encoding="utf8",
    ) as f:
        hooks.Filters.CLI_DO_INIT_TASKS.add_items([
            (
                location,
                f.read()
            ),
        ])

add_init_tasks("lms")
add_init_tasks("mysql")


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        os.path.join(os.path.dirname(__file__), "templates"),
    ]
)




hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``destination_path`` (relative to your Tutor environment).
    [
        ("ufmtemrede", "build/openedx/themes"),
        ("brand-openedx", "plugins/mfe/build/mfe"),
        ("local", "env/local"),
        ("openedx/locale", "build"),
        ("mfe/i18n", "plugins/mfe/build")
       
    ],
)

hooks.Filters.ENV_PATTERNS_IGNORE.add_items(
    # Ignore these patterns when rendering templates.
    [
      
    ]
)


    
# Force the rendering of scss files, even though they are included in a "partials" directory
hooks.Filters.ENV_PATTERNS_INCLUDE.add_item(r"ufmtemrede/lms/static/sass/partials/lms/theme/")
hooks.Filters.ENV_PATTERNS_INCLUDE.add_item(r"ufmtemrede/cms/static/sass/partials/cms/theme/")



########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorbranding/patches,
# apply a patch based on the file's name and contents.
for path in glob(
        os.path.join(
            os.path.dirname(__file__), "patches", "*",
        )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

