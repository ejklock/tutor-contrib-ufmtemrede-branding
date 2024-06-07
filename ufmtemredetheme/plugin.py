import json
import os
import zipfile
from glob import glob
from pathlib import Path
from urllib.error import HTTPError

import click
import pkg_resources
import requests
from tutor import config as tutor_config
from tutor import env, fmt, hooks

from .__about__ import __version__

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
        "FOOTER_NAV_LINKS": [
            # {"title": "About", "url": "/about"},
            # {"title": "Contact", "url": "/contact"},
        ],
        "FOOTER_LEGAL_LINKS": [
            # {"title": "Terms of service", "url": "/tos"},
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

hooks.Filters.ENV_PATCHES.add_items(
    [
        (
            "mfe-dockerfile-post-npm-install-learning",
            """

RUN npm install '@edx/frontend-component-header@npm:@edly-io/indigo-frontend-component-header@^1.0.0'
RUN npm install '@edx/frontend-component-footer@npm:@edly-io/indigo-frontend-component-footer@^1.0.0'
""",
        ),
        (
            "mfe-dockerfile-post-npm-install-authn",
            """

""",
        ),
        # Tutor-Indigo v2.1 targets the styling updations in discussions and learner-dashboard MFE
        # brand-openedx is related to styling updates while others are for header and footer updates
        (
            "mfe-dockerfile-post-npm-install-discussions",
            """
RUN npm install '@edx/brand@npm:@edly-io/indigo-brand-openedx@^1.0.0'
RUN npm install '@edx/frontend-component-header@npm:@edly-io/indigo-frontend-component-header@^1.0.0'
RUN npm install '@edx/frontend-component-footer@npm:@edly-io/indigo-frontend-component-footer@^1.0.0'
""",
        ),
        (
            "mfe-dockerfile-post-npm-install-learner-dashboard",
            """

RUN npm install '@edx/frontend-component-footer@npm:@edly-io/indigo-frontend-component-footer@^1.0.0'
""",
        ),
    ]
)


################# Initialization tasks
# To run the script from templates/panorama/tasks/myservice/init, add:
with open(
        pkg_resources.resource_filename(
            "ufmtemredetheme", os.path.join("templates", "tasks", "lms", "init")
        ),
        encoding="utf8",
) as f:
    hooks.Filters.CLI_DO_INIT_TASKS.add_items([
         (
            "lms",
            f.read()
        ),
         (
            "cms",
            f.read()
        ),
         
    ]
        
    )

########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("ufmtemredetheme", "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``destination_path`` (relative to your Tutor environment).
    [
        ("ufmtemrede", "build/openedx/themes"),
        ("brand-openedx", "plugins/mfe/build/mfe"),
    ],
)

# Force the rendering of scss files, even though they are included in a "partials" directory
hooks.Filters.ENV_PATTERNS_INCLUDE.add_item(r"ufmtemrede/lms/static/sass/partials/lms/theme/")
hooks.Filters.ENV_PATTERNS_INCLUDE.add_item(r"ufmtemrede/cms/static/sass/partials/cms/theme/")


########################################
# Commands
########################################

@click.group(help="Branding tools", name='branding')
@click.pass_obj
def UFMT_EM_REDE_command(context):
    pass


def _download_file(url: str, dest_dir: str, filename: str):
    fmt.echo_info(f"Downloading {filename} from {url} to {dest_dir}")

    try:
        response = requests.get(url)
        response.raise_for_status()

        open(os.path.join(dest_dir, filename), "wb").write(response.content)

    except HTTPError as http_err:
        fmt.echo_error(f'HTTP error occurred downloading {filename}: {http_err}')
    except Exception as err:
        fmt.echo_error(f'Error downloading {filename}: {err}')


@click.command(help="Download image from url")
@click.pass_obj
def download_images(context):
    fmt.echo_info("*** Downloading images ***")
    config = tutor_config.load(context.root)

    # Download LMS images
    dest_dir = os.path.join(context.root, 'env', 'build', 'openedx', 'themes', 'theme', 'lms', 'static', 'images')

    if "UFMT_EM_REDE_LMS_IMAGES" in config:
        for image in config['UFMT_EM_REDE_LMS_IMAGES']:
            Path(dest_dir).mkdir(parents=True, exist_ok=True)
            _download_file(url=image['url'], filename=image['filename'], dest_dir=dest_dir)
    else:
        fmt.echo_alert("No UFMT_EM_REDE_LMS_IMAGES configured")

    # Download CMS images
    dest_dir = os.path.join(context.root, 'env', 'build', 'openedx', 'themes', 'theme', 'cms', 'static', 'images')

    if "UFMT_EM_REDE_CMS_IMAGES" in config:
        Path(dest_dir).mkdir(parents=True, exist_ok=True)
        for image in config['UFMT_EM_REDE_CMS_IMAGES']:
            _download_file(url=image['url'], filename=image['filename'], dest_dir=dest_dir)
    else:
        fmt.echo_alert("No UFMT_EM_REDE_CMS_IMAGES configured")


@click.command(help="Download and unzip font from url")
@click.pass_obj
def download_fonts(context):
    fmt.echo_info("*** Downloading fonts ***")
    config = tutor_config.load(context.root)

    # Download fonts
    dest_dir = os.path.join(context.root, 'env', 'build', 'openedx', 'themes', 'theme', 'lms', 'static', 'fonts')
    dest_dir_mfe = os.path.join(context.root, 'env', 'plugins', 'mfe', 'build', 'mfe', 'brand-openedx', 'fonts')

    if "UFMT_EM_REDE_FONTS_URLS" in config:
        for font_url in config['UFMT_EM_REDE_FONTS_URLS']:
            filename = 'font.zip'
            Path(dest_dir).mkdir(parents=True, exist_ok=True)
            _download_file(url=font_url, dest_dir=dest_dir, filename=filename)

            # Unzip the file
            with zipfile.ZipFile(os.path.join(dest_dir, filename), 'r') as zip:
                zip.extractall(dest_dir)
                if 'mfe' in config.get('PLUGINS'):
                    zip.extractall(dest_dir_mfe)
                zip.printdir()

                os.remove(os.path.join(dest_dir, filename))

    else:
        fmt.echo_alert("No UFMT_EM_REDE_FONTS_URLS configured")


UFMT_EM_REDE_command.add_command(download_images)
UFMT_EM_REDE_command.add_command(download_fonts)

hooks.Filters.CLI_COMMANDS.add_item(UFMT_EM_REDE_command)

########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorbranding/patches,
# apply a patch based on the file's name and contents.
for path in glob(
        os.path.join(
            pkg_resources.resource_filename("ufmtemredetheme", "patches"),
            "*",
        )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
