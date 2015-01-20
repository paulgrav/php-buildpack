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

        self.env = self._ctx.get('ENV')
        _log.info('Found ENV: %s' % self.env)

        return True

    def _clearout_ini(self, path, env):
        """Looks at the specified path of ini files matching env-(dev|stage|prod)
        and deletes the environment specific ini files that do not match the
        specified environment.
        """
        if not os.path.exists(path):
            _log.info('Path not found: %s' % path)
            return

        iniscanglob = os.path.join(path,'env-*.ini')
        envini = os.path.join(path, 'env-%s.ini' % env)
        _log.info('Searching: %s' % path)
        for i in glob.glob(iniscanglob):
            _log.info('Found: %s' % i)
            if i != envini:
                os.remove(i)
                _log.info('Removed: %s' % i)

    def _compile(self, install):

        phpini_confd_path = os.path.join(self._ctx.get('HOME'),'app','php','etc','conf.d')
        phpini_scan_dir = self._ctx.get('PHP_INI_SCAN_DIR')

        self._clearout_ini(phpini_confd_path, self.env)
        self._clearout_ini(phpini_scan_dir, self.env)


# Register extension methods
PHPConfigChooser.register(__name__)