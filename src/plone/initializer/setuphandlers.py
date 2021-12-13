# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from zope.component.hooks import getSite
from App.config import getConfiguration
import os
from pathlib import Path
from Products.CMFCore.utils import getToolByName
from pprint import pprint
import io


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'plone.initializer:uninstall',
        ]


def _load_setup_data(context):
    context
    portal_setup = getToolByName(context, 'portal_setup')
    tar_file_path =  os.path.join(os.path.dirname(getConfiguration().clienthome),'importdata',getSite().id,'data.tar.gz')
    if Path(tar_file_path).exists():
        tar_fileobj = io.BytesIO()
        with open(tar_file_path, 'r:*') as fin:
            tar_fileobj = io.BytesIO(fin.read())
        tarball = tar_fileobj.getvalue()
        result = portal_setup.runAllImportStepsFromProfile(None, True, archive=tarball)
        steps_run = 'Steps run: %s' % ', '.join(result['steps'])
        portal_setup.manage_importSteps(manage_tabs_message=steps_run,
                                        messages=result['messages'])



def post_install(context):
    """Post install script"""
    _load_setup_data(context)

def uninstall(context):
    """Uninstall script"""
