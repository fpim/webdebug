

def run(mainpyfile,port,pin,host):
    try:
        import __main__
        main_dic = {"__name__": "__main__",
                                  "__file__": mainpyfile,
                                  "__builtins__": __builtins__,
                                  }
        __main__.__dict__.clear()
        __main__.__dict__.update(main_dic)

        import os

        canonic = os.path.abspath(mainpyfile)
        canonic = os.path.normcase(canonic)

        with open(canonic, "rb") as fp:
            statement = "exec(compile(%r, %r, 'exec'))" % \
                        (fp.read(), canonic)
        cmd = compile(statement, "<string>", "exec")
        exec(cmd, __main__.__dict__, __main__.__dict__)
    except Exception as ex:
        from webdebug import start_server
        start_server(ex,host,pin,port,[])

if __name__ == '__main__':
    import getopt
    import os
    import sys
    from webdebug.core import _DEFAULT_PORT, _DEFAULT_PIN, _DEFAULT_HOST,_usage
    opts, args = getopt.getopt(sys.argv[1:], 'mh', ['help','host=', 'pin=', 'port='])
    if not args:
        print(_usage)
        sys.exit(2)

    run_as_module = False
    port,pin,host = _DEFAULT_PORT, _DEFAULT_PIN, _DEFAULT_HOST

    for opt, optarg in opts:
        if opt in ['-h', '--help']:
            print(_usage)
            sys.exit()
        elif opt in ['-m']:
            run_as_module = True
        elif opt == '--host':
            host = optarg
        elif opt == '--pin':
            pin = optarg
        elif opt == '--port':
            port = int(optarg)



    mainpyfile = args[0]
    sys.argv[:] = args
    run(mainpyfile,port,pin,host)



