from . import *

if __name__ == '__main__':

    import pdb
    import getopt
    import os
    opts, args = getopt.getopt(sys.argv[1:], 'mh', ['help'])

    if not args:
        print(_usage)
        sys.exit(2)

    run_as_module = False
    for opt, optarg in opts:
        if opt in ['-h', '--help']:
            print(_usage)
            sys.exit()
        elif opt in ['-m']:
            run_as_module = True

    mainpyfile = args[0]  # Get script filename
    if not run_as_module and not os.path.exists(mainpyfile):
        print('Error:', mainpyfile, 'does not exist')
        sys.exit(1)

    sys.argv[:] = args  # Hide "pdb.py" and pdb options from argument list
    # Replace pdb's dir with script's dir in front of module search path.
    if not run_as_module:
        sys.path[0] = os.path.dirname(mainpyfile)
    pp = pdb.Pdb()
    pp.rcLines.extend(['continue'])
    try:
        pp._runscript(mainpyfile)
    except Exception as ex:
        from webdebug import start_server
        start_server(ex)