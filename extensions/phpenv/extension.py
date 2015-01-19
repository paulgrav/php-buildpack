# -*- coding: utf-8 -*-
from extension_helpers import PHPExtensionHelper
import os
import glob
import logging

_log = logging.getLogger('PHPConfigChooser')


class PHPConfigChooser(PHPExtensionHelper):
    def __init__(self, ctx):
        PHPExtensionHelper.__init__(self, ctx)

    def _should_compile(self):
        if not self._ctx.get('ENV'):
            return False

        if not self._ctx.get('PHP_INI_SCAN_DIR'):
            return False

        self.env = self._ctx.get('ENV')
        self.iniscandir = self._ctx.get('PHP_INI_SCAN_DIR')
        _log.info('Found ENV: %s' % self.env)
        _log.info('Found PHP_INI_SCAN_DIR: %s' % self.iniscandir)
        # 1. get all ini files in the scan dir
        # 2. remove all env-\w+.ini that don’t match the $ENV

        return True

    def _compile(self, install):
        """Check to see if the ENV environment variable is set. If it is
        then we look for env-${ENV}.ini and try to use that for the php.ini """

        iniscanglob = os.path.join(self.iniscandir,'env-*.ini')
        envini = os.path.join(iniscanglob, 'env-%s.ini' % self.env)
        for i in glob.glob(iniscanglob):
            if i != envini:
                _log.info('Removed: %s' % i)
                os.remove(i)

# Register extension methods
PHPConfigChooser.register(__name__)