# -*- coding: utf-8 -*-
'''
Smoothtest
Copyright (c) 2015 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import rel_imp; rel_imp.init()
from .Logger import Logger
from .simple_xpath_browser import SimpleXpathBrowser

logger = Logger()

def embed():
    """Call this to embed IPython at the current point in your program.
    """
    iptyhon_msg = ('Could not embed Ipython, falling back to ipdb'
                   ' shell. Exception: %r')
    ipdb_msg = ('Could not embed ipdb, falling back to pdb'
                ' shell. Exception: %r')
    b = browser = SimpleXpathBrowser()
    display_banner = "XpathBrowser in 'b' or 'browser' variables"
    try:
        from IPython.terminal.embed import InteractiveShellEmbed
        # Now create the IPython shell instance. Put ipshell() anywhere in your code
        # where you want it to open.
        ipshell = InteractiveShellEmbed(banner2=display_banner)
        ipshell()
    except Exception as e:
        logger.w(iptyhon_msg % e)
        try:
            import ipdb
            ipdb.set_trace()
        except Exception as e:
            logger.e(ipdb_msg % e)
            import pdb
            pdb.set_trace()


if __name__ == "__main__":
    embed()
