#!/usr/bin/python
from __future__ import print_function
import argparse
import sys
import utils
from v1_1 import shell as shell_v1_1
VERSION='1.1'
class IllegalArgumentException(Exception):
        def __init__(self, msg):
                self.msg = msg
        def __str__(self):
                return repr(msg)
class BlogShellParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(BlogShellParser, self).__init__(*args, **kwargs)
    def error(self, message):
        """error(message: string)

        Prints a usage message incorporating the message to stderr and
        exits.
        """
        self.print_usage(sys.stderr)
        choose_from = ' (choose from'
        progparts = self.prog.partition(' ')
        self.exit(2, ("error: %(errmsg)s\nTry '%(mainp)s help %(subp)s'"
                "for more information.\n") %
                {'errmsg': message.split(choose_from)[0],
                    'mainp': progparts[0],
                    'subp': progparts[2]})
class BlogShell(object):
    """
    A shell to manager blog
    """
    def get_base_parser(self):
        parser = BlogShellParser(prog = 'blog',
                description=self.__doc__.strip(),
                epilog='See "blog help COMMAND" '
                       'for help on a specific command.',
                add_help = False
        )
        parser.add_argument('-h', '--help',
                action='store_true',
                help=argparse.SUPPRESS,
        )
        parser.add_argument('--version',
                action='version',
                version=VERSION,
        )
        parser.add_argument('--debug',
                action='store_true',
                default=False,
                help = 'Print debugging output',
        )
        return parser
    def get_subcommand_parser(self, version = VERSION):
        parser = self.get_base_parser()
        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>')
        try:
            actions_module = {
                    '1.1': shell_v1_1,
                    }[version]
        except KeyError:
            actions_module = shell_v1_1
        self._find_actions(subparsers, actions_module)
        self._find_actions(subparsers, self)
        return parser
    def _find_actions(self, subparsers,actions_module):
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            command = attr[3:].replace('_', '-')
            callback = getattr(actions_module, attr)
            desc = callback.__doc__ or ''
            action_help = desc.strip()
            arguments = getattr(callback, 'arguments', [])
            subparser = subparsers.add_parser(command,
                    help=action_help,
                    description=desc,
                    add_help=False,
            )
            subparser.add_argument('-h', '--help',
                    action='help',
                    help=argparse.SUPPRESS,
            )
            self.subcommands[command] = subparser
            for (args, kwargs) in arguments:
                subparser.add_argument(*args, **kwargs)
            subparser.set_defaults(func=callback)
    def setup_debugging(self, debug):
        pass

    @utils.arg('command', metavar='<subcommand>', nargs='?',
            help='Display help for <subcommand>')
    def do_help(self, args):
        """
        Display help about this program or one of its subcomands.
        """
        if args.command:
            if args.command in self.subcommands:
                self.subcommands[args.command].print_help()
            else:
                raise IllegalArgumentException("'%s' is not a valid subcommand" % args.command)
        else:
            self.parser.print_help()
    def do_bash_completion(self, args):
        commands = set()
        options = set()
        for sc_str, sc in self.subcommands.items():
            commands.add(sc_str)
            for option in sc._optionals._option_string_actions.keys():
                options.add(option)
        commands.remove('bash-completion')
        commands.remove('bash_completion')
        print(' '.join(commands | options))
    def main(self, argv):
        parser = self.get_base_parser()
        (options, args) = parser.parse_known_args(argv)
        self.setup_debugging(options.debug)
        subcommand_parser = self.get_subcommand_parser(VERSION)
        self.parser = subcommand_parser
        if options.help or not argv:
            subcommand_parser.print_help()
            return 0
        args = subcommand_parser.parse_args(argv)
        if args.func == self.do_help:
                self.do_help(args)
                return 0
        elif args.func == self.do_bash_completion:
            self.do_bash_completion(args)
            return 0
        args.func(args)
def main():
    BlogShell().main(sys.argv[1:])
    #try:
    #    BlogShell().main(sys.argv[1:])
    #except Exception as e:
    #    print("ERROR: {0}".format(e), file=sys.stderr)
    #except KeyboardInterrupt as e:
    #    print("Shutting down blogclient", file=sys.stderr)
    #    sys.exit(1)
if __name__ == "__main__":
    main()
