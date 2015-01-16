from extension_helpers import PHPExtensionHelper
import os
import os
import logging

_log = logging.getLogger('PHPConfigChooser')


class PHPConfigChooser(PHPExtensionHelper):
    def __init__(self, ctx):
        PHPExtensionHelper.__init__(self, ctx)

    def _configure(self):
        """Check to see if the ENV environment variable is set. If it is
        then we look for php-${ENV}.ini and try to use that for the php.ini """

        if not os.environ.get('ENV'):
            return

        env = os.environ.get('ENV')
        _log.info('Found ENV: %s' % env)
        original_ini = os.path.join(self._ctx['BUILD_DIR'],
                                         'php', 'etc', 'php.ini')
        env_specific_ini = os.path.join(self._ctx['BUILD_DIR'],
                                        'php','etc','php-%s.ini' % env )
        if os.path.exists(env_specific_ini):
            os.rename(env_specific_ini, original_ini)
            _log.info('Renamed %s to %s' % (env_specific_ini, original_ini))
        else:
            _log.info('%s not found' % env_specific_ini)

# Register extension methods
PHPConfigChooser.register(__name__)