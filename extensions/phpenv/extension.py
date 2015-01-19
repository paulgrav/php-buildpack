from extension_helpers import PHPExtensionHelper
import os
import os
import logging

_log = logging.getLogger('PHPConfigChooser')


class PHPConfigChooser(PHPExtensionHelper):
    def __init__(self, ctx):
        PHPExtensionHelper.__init__(self, ctx)

    def _should_compile(self):
        if not self._ctx.get('ENV'):
            return False

        env = self._ctx.get('ENV')
        _log.info('Found ENV: %s' % env)

        self.env_specific_ini = os.path.join(self._ctx['BUILD_DIR'],
                                      'php','etc','php-%s.ini' % env )
        _log.info('Looking for: %s' % self.env_specific_ini)
        if os.path.exists(self.env_specific_ini):
            return True

        return False

    def _compile(self, install):
        """Check to see if the ENV environment variable is set. If it is
        then we look for php-${ENV}.ini and try to use that for the php.ini """

        original_ini = os.path.join(self._ctx['BUILD_DIR'],
                                         'php', 'etc', 'php.ini')
        os.rename(self.env_specific_ini, original_ini)
        _log.info('Renamed %s to %s' % (self.env_specific_ini, original_ini))
        install.package('PHPENV')

# Register extension methods
PHPConfigChooser.register(__name__)