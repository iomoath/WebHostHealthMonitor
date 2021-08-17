import argparse
import core
import sys
import config

arg_parser = None


def generate_argparser():
    ascii_logo = """
    Web Site Monitor Agent
    Moath Maharmeh - Moath@vegalayer.com
    
    github.com/iomoath/WebHostHealthMonitor
    """

    ap = argparse.ArgumentParser(ascii_logo)

    ap.add_argument("-c","--check", action='store_true',
                    help="Check web hosts reachability")

    ap.add_argument("-v", "--verbose", action='store_true',
                    help="Show more information while processing.")

    ap.add_argument("--version", action="version", version='Web Site Monitor Agent. Version 1.1')
    return ap


def run(args):
    if args["verbose"]:
        config.VERBOSE_ENABLED = True

    if args['check']:
        core.check_hosts_reachability()
    else:
        arg_parser.print_help()
        sys.exit()



def main():
    global arg_parser
    arg_parser = generate_argparser()
    args = vars(arg_parser.parse_args())
    run(args)



if __name__ == "__main__":
    main()