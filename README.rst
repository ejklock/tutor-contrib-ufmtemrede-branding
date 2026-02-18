ufmtemrede plugin for `Tutor <https://docs.tutor.edly.io>`__
###############################################################################

UFMT em Rede indigo based from tutor-contrib-branding theme for tutor edx


Installation
************

.. code-block:: bash

    pip install git+https://github.com/myusername/tutor-contrib-ufmtemrede-theme

Configuration
-------------

Customize colors
~~~~~~~~~~~~~~~~

Most Bootstrap variables can be set using settings. 
These are the available variables and their defaults:

* UFMT_EM_REDE_PRIMARY: #0000FF
* UFMT_EM_REDE_SECONDARY: #454545
* UFMT_EM_REDE_FONT_FAMILY: <no default>
* UFMT_EM_REDE_BRAND: #9D0054
* UFMT_EM_REDE_SUCCESS: #178253
* UFMT_EM_REDE_INFO: #006DAA
* UFMT_EM_REDE_DANGER: #C32D3A
* UFMT_EM_REDE_WARNING: #FFD900
* UFMT_EM_REDE_LIGHT: #E1DDDB
* UFMT_EM_REDE_DARK: #273F2F
* UFMT_EM_REDE_ACCENT_A: #00BBF9
* UFMT_EM_REDE_ACCENT_B: #FFEE88
* UFMT_EM_REDE_BACKGROUND: #ffffff
* UFMT_EM_REDE_BG_PRIMARY: #ffffff
* UFMT_EM_REDE_BODY: #FFFFFF
* UFMT_EM_REDE_HOMEPAGE_BG_IMAGE: ""

You can add these settings to the ``config.yml`` file or using the
``tutor config --set "<setting>=<value>"`` command.

These settings affect the Bootstrap's ``_variables.scss`` file in the
`comprehensive theme <https://github.com/openedx/edx-platform/blob/master/lms/static/sass/partials/lms/theme/_variables.scss>`__
and in the `MFE branding module <https://github.com/openedx/brand-openedx/blob/625ad32f9cf8247522541ee77dfd574b30245226/paragon/_variables.scss>`__.

You can also add CSS overrides using the ``UFMT_EM_REDE_EXTRAS`` and the ``UFMT_EM_REDE_OVERRIDES`` variables,
to impact the `comprehensive theme <https://github.com/openedx/edx-platform/blob/master/lms/static/sass/partials/lms/theme/_extras.scss>`__
and the `MFE branding module <https://github.com/openedx/brand-openedx/blob/625ad32f9cf8247522541ee77dfd574b30245226/paragon/_overrides.scss>`__
respectively.

E.g., this setting will add a CSS block to change the color of h1 texts in all MFE:

::

    UFMT_EM_REDE_OVERRIDES: >-
      h1 {
            color: red;
      }

Managing fonts
~~~~~~~~~~~~~~

Set ``UFMT_EM_REDE_FONTS_URLS`` to a list of URLS pointing to a zipped set of font files.
Then use the ``tutor branding download-fonts`` command to download an unzip the font files
to ``$(tutor config printroot)/env/build/openedx/themes/theme/lms/static/fonts`` and
``$(tutor config printroot)/env/plugins/mfe/build/mfe/brand-openedx/fonts`` if the mfe plugin is enabled.

Tip: copy the download url from the `<https://fonts.google.com>`__ site,
for instance `<https://fonts.google.com/download?family=Roboto%20Flex>`__.

E.g., to add Roboto Flex font, set:

::

    UFMT_EM_REDE_FONTS_URLS:
    - https://fonts.google.com/download?family=Roboto%20Flex

Then run

::

    tutor branding download-fonts

To add a specific font definition, use the ``UFMT_EM_REDE_FONTS`` setting, e.g.:

::

    UFMT_EM_REDE_FONTS: >-
        @font-face {
            font-family: 'Roboto Flex';
            src: url('RobotoFlex-VF.woff2') format('woff2 supports variations'),
               url('RobotoFlex-VF.woff2') format('woff2-variations');
        }

Learn more about using flex fonts `here <https://web.dev/variable-fonts/>`__.

Finally, set the font family using the ``UFMT_EM_REDE_FONT_FAMILY`` variable:

::

    UFMT_EM_REDE_FONT_FAMILY: Roboto Flex


Downloading images
~~~~~~~~~~~~~~~~~~

CMS and LMS images can be included as long as they can be accessed through a HTTP(S) request.
Most important images are:

LMS:

- favicon.ico
- logo.png

CMS:

- studio-logo.png

A banner can also be added to the homepage.

E.g., to add custom logos and banner set the following:

::

    UFMT_EM_REDE_LMS_IMAGES:
    - filename: banner.png
      url: https://url/to/banner.png
    - filename: favicon.ico
      url: https://url/to/favicon.ico
    - filename: logo.png
      url: https://url/to/logo.png
    UFMT_EM_REDE_CMS_IMAGES:
    - filename: studio-logo.png
      url: https://url/to/studio-logo.png
    UFMT_EM_REDE_HOMEPAGE_BG_IMAGE: banner.png

Then run

::

    tutor branding download-images

Custom HTML block in home page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can add a custom HTML code to be rendered in the home page after the banner
and before the list of courses by setting ``UFMT_EM_REDE_INDEX_ADDITIONAL_HTML``.

Customize HTML certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~

By setting ``UFMT_EM_REDE_CERTIFICATE_HTML`` you can override the standard certificate with
your own HTML code.

Tip: Create a file with the HTML code (e.g., ``UFMT_EM_REDE_certificate_html.html``)
and then update the configuration from the file.

::

    tutor config save --set UFMT_EM_REDE_CERTIFICATE_HTML="$(cat UFMT_EM_REDE_certificate_html.html)"


Customizing static pages
~~~~~~~~~~~~~~~~~~~~~~~~

You can set your own HTML content to the typical static pages by setting the corresponding
variable:

- UFMT_EM_REDE_STATIC_TEMPLATE_404
- UFMT_EM_REDE_STATIC_TEMPLATE_429
- UFMT_EM_REDE_STATIC_TEMPLATE_ABOUT
- UFMT_EM_REDE_STATIC_TEMPLATE_BLOG
- UFMT_EM_REDE_STATIC_TEMPLATE_CONTACT
- UFMT_EM_REDE_STATIC_TEMPLATE_DONATE
- UFMT_EM_REDE_STATIC_TEMPLATE_EMBARGO
- UFMT_EM_REDE_STATIC_TEMPLATE_FAQ
- UFMT_EM_REDE_STATIC_TEMPLATE_HELP
- UFMT_EM_REDE_STATIC_TEMPLATE_HONOR
- UFMT_EM_REDE_STATIC_TEMPLATE_JOBS
- UFMT_EM_REDE_STATIC_TEMPLATE_MEDIA_KIT
- UFMT_EM_REDE_STATIC_TEMPLATE_NEWS
- UFMT_EM_REDE_STATIC_TEMPLATE_PRESS
- UFMT_EM_REDE_STATIC_TEMPLATE_PRIVACY
- UFMT_EM_REDE_STATIC_TEMPLATE_SERVER_DOWN
- UFMT_EM_REDE_STATIC_TEMPLATE_SERVER_ERROR
- UFMT_EM_REDE_STATIC_TEMPLATE_SERVER_OVERLOADED
- UFMT_EM_REDE_STATIC_TEMPLATE_SITEMAP
- UFMT_EM_REDE_STATIC_TEMPLATE_TOS

Customizing MFE header and footer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use a custom header or footer, clone `frontend-component-header <https://github.com/openedx/frontend-component-header>`_
and/or `frontend-component-footer <https://github.com/openedx/frontend-component-footer>`_,
push to your custom repository and set the repository URL in the variables:

- UFMT_EM_REDE_FRONTEND_COMPONENT_HEADER_REPO
- UFMT_EM_REDE_FRONTEND_COMPONENT_FOOTER_REPO

Usage
-----

::

    tutor plugins enable branding
    tutor branding download-images
    tutor branding download-fonts
    tutor images build openedx
    tutor images build mfe
    tutor local settheme theme

In K8s deployments, you will need to push the docker images and restart Tutor.

License
-------

This software is licensed under the terms of the AGPLv3.
