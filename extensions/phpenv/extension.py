from extension_helpers import PHPExtensionHelper
import os
import os
import logging

_log = logging.getLogger('PHPConfigChooser')


class PHPConfigChooser(PHPExtensionHelper):
    def __init__(self, ctx):
        PHPExtensionHelper.__init__(self, ctx)

    def _configure(self):

        if not os.environ.get('ENV'):
            return

        env = os.environ.get('ENV')
        php_ini_path = os.path.join(self._ctx['BUILD_DIR'],
                                         'php', 'etc', 'php.ini')
        new_ini_path = os.path.join(self._ctx['BUILD_DIR'],
                                        'php','etc','php-%s.ini' % env )
        os.rename(new_ini_path, php_ini_path)


# Register extension methods
PHPConfigChooser.register(__name__)