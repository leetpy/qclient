#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import sys
import utils

class BaseAction():
    pass


class RunInstanceAction(BaseAction):
    
    @classmethod
    def get_params(cls, args):
        return {
            "image_id": args.image_id,
        }

class QShell(object):

    def get_base_parser(self):
        parser = argparse.ArgumentParser(prog='qingcloud client')
        return parser
    
    def get_subcommand_parser(self):
        parser = self.get_base_parser()
        subparsers = parser.add_subparsers()
        ri_parser = subparsers.add_parser('run-instances', help='create instances')
        ri_parser.add_argument('-m', '--image_id', dest='image_id',
                               type=str, default='', required=True,
                               help='image ID')
        ri_parser.add_argument('-t', '--instance_type', dest='instance_type',
                               type=str, default=None, required=True,
                               help='instance type: small_b, small_c, medium_a, medium_b, medium_c, \
                               large_a, large_b, large_c')
        return parser
    
    def load_config(self):
        user_config = '~/.qingcloud/config.yaml'
        work_dir = os.path.dirname(os.path.realpath(__file__))
        if os.path.isfile(user_config):
            cf_file = user_config
        else:
            cfg_file = os.path.join(work_dir, 'config.yaml')

    try:

        conf = utils.parse_config(cfg_file)

    except Exception, e:

        print(e)
       
    def main(self, argv):
        parser = self.get_base_parser()
        parser.parse_known_args(argv)

        subcommand_parser = self.get_subcommand_parser()
        args = subcommand_parser.parse_args(argv)


def main():
    try:
        QShell().main(sys.argv[1:])
    except KeyboardInterrupt:
        print("... terminating qingcloud client")
        return 1
    except Exception as e:
        print(e)
        return 1


if __name__ == '__main__':
    sys.exit(main())
