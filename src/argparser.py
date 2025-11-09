import sys

class ArgParser:
    def __init__(self):
        self.noArg = True

        self.all = False
        self.help = False
        self.interfaces = False
        self.ports = False
        self.protocol = None
        self.version = False
        self.verbose = False

        self.virtual = False
        self.physical = False

    def parse(self, args):
        if not args:
            return

        self.noArg = False

        index = 0

        while index < len(args):
            arg = args[index]

            if arg.startswith('--'):
                if arg == '--all':
                    self.all = True

                elif arg == '--help':
                    self.help = True

                elif arg == '--interfaces':
                    self.interfaces = True

                elif arg == '--ports':
                    self.ports = True

                    nextIndex = index + 1
                    if nextIndex < len(args):
                        arg = args[nextIndex]

                        if arg.lower() not in ('tcp', 'udp'):
                            print(f'Error: `{arg}` is not a valid protocol')
                            sys.exit(1)

                        self.protocol = arg
                        index += 1

                elif arg == '--version':
                    self.version = True

                elif arg == '--verbose':
                    self.verbose = True

                else:
                    print(f'Error: unrecognized argument `{arg}`')
                    sys.exit(1)

            elif arg.startswith('-'):
                if arg == '-a':
                    self.all = True

                elif arg == '-h':
                    self.help = True

                elif arg == '-i':
                    self.interfaces = True

                elif arg == '-p':
                    self.ports = True

                    nextIndex = index + 1
                    if nextIndex < len(args):
                        arg = args[nextIndex]

                        if arg.lower() not in ('tcp', 'udp'):
                            print(f'Error: `{arg}` is not a valid protocol')
                            sys.exit(1)

                        self.protocol = arg
                        index += 1

                elif arg == '-V':
                    self.version = True

                elif arg == '-phy':
                    self.physical = True

                elif arg == '-virt':
                    self.virtual = True

                elif arg == '-v':
                    self.verbose = True

                else:
                    print(f'Error: unrecognized argument `{arg}`')
                    sys.exit(1)

            else:
                print(f'Error: unrecognized argument `{arg}`')
                sys.exit(1)

            index += 1