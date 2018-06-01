#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import sys
import qclient.utils
from qclient.http_util import send_http


class BaseAction():
    base_optional = []

    @classmethod
    def get_params(cls, args):
        params = {}
        for op in cls.base_optional:
            if hasattr(args, op) and getattr(args, op):
                params[op] = getattr(args, op)

        return params


class RunInstancesAction(BaseAction):

    name = "RunInstances"
    base_optional = ["instance_class", "count", "instance_name", "vxnets", 
                     "security_group", "login_mode", "login_passwd", "login_passwd", 
                     "hostname", "need_userdata", "userdata_type", "userdata_value",
                     "userdata_path", "target_user", "cpu_max", "mem_max"]

    @classmethod
    def get_params(cls, args):
        params = {
            "image_id": args.image_id,
        }
        if getattr(args, "instance_type"):
            params["instance_type"] = args.instance_type
        else:
            if getattr(args, "cpu") and getattr(args, "memory"):
                params["cpu"] = args.cpu
                params["memory"] = args.memory
            else:
                print("error, you should specify instance_type or specify both CPU and memory")
                sys.exit(1)

        for op in cls.base_optional:
            if hasattr(args, op) and getattr(args, op):
                params[op] = getattr(args, op)
        return params

    @classmethod
    def add_subparser(cls, subparsers):
        parser = subparsers.add_parser('run-instances', help='create instances')

        parser.add_argument('-m', '--image_id', dest='image_id',
                action='store', type=str, default='', required=True,
                help='image ID')

        parser.add_argument('-t', '--instance_type', dest='instance_type',
                action='store', type=str, default=None,
                help='instance type: small_b, small_c, medium_a, medium_b, medium_c, \
                large_a, large_b, large_c')

        parser.add_argument('-i', '--instance_class', dest='instance_class',
                action='store', type=int, default=None,
                help='instance class: 0 is performance; 1 is high performance, default 0.')

        parser.add_argument('-c', '--count', dest = 'count',
                action='store', type=int, default=1,
                help='the number of instances to launch, default 1.')

        parser.add_argument('-C', '--cpu', dest='cpu',
                action='store', type=int, default=None,
                help='cpu core: 1, 2, 4, 8, 16')

        parser.add_argument('-M', '--memory', dest='memory',
                action='store', type=int, default=None,
                help='memory size in MB: 512, 1024, 2048, 4096, 8192, 16384')

        parser.add_argument('-N', '--instance_name', dest='instance_name',
                action='store', type=str, default='',
                help='instance name')

        parser.add_argument('-n', '--vxnets', dest='vxnets',
                action='store', type=str, default=None,
                help='specifies the IDs of vxnets the instance will join.')
    
        parser.add_argument('-s', '--security_group', dest='security_group',
                action='store', type=str, default=None,
                help='the ID of security group that will be applied to instance')

        parser.add_argument('-l', '--login_mode', dest='login_mode',
                action='store', type=str, default=None, required=True,
                help='SSH login mode: keypair or passwd')

        parser.add_argument('-p', '--login_passwd', dest='login_passwd',
                action='store', type=str, default='',
                help='login_passwd, should specified when SSH login mode is "passwd".')

        parser.add_argument('-k', '--login_keypair', dest='login_keypair',
                action='store', type=str, default='',
                help='login_keypair, should specified when SSH login mode is "keypair".')

        parser.add_argument('--hostname', dest='hostname',
                action='store', type=str, default='',
                help='the hostname you want to specify for the new instance.')

        parser.add_argument('--need_userdata', dest='need_userdata',
                action='store_const', const=1,
                help='use userdata')

        parser.add_argument('--userdata_type', dest='userdata_type',
                action='store', type=str, default=None,
                help='userdata_type: plain, exec, tar')

        parser.add_argument('--userdata_value', dest='userdata_value',
                action='store', type=str, default=None,
                help='userdata_value')

        parser.add_argument('--userdata_path', dest='userdata_path',
                action='store', type=str, default=None,
                help='userdata_path')

        parser.add_argument('--target-user', dest='target_user',
                action='store', type=str, default=None,
                help='ID of user who will own this resource, should be one of your sub-account.')

        parser.add_argument("--cpu_max", dest="cpu_max",
                action="store", type=int, default=0,
                help='''The cpu core, e.g. "1, 2, 4, 8, 16".''')

        parser.add_argument("--mem_max", dest="mem_max",
                action="store", type=int, default=0,
                help='''The memory size in MB, e.g. "1024, 2048, 4096"''')


class DescribeInstancesAction(BaseAction):
    name = "DescribeInstances"

    base_optional = ["status", "search_word", "verbose"]

    @classmethod
    def add_subparser(cls, subparsers):
        parser = subparsers.add_parser('describe-instances', help='describe instances')
        parser.add_argument('-i', '--instances', dest='instances',
                            type=str, default='',
                            help='the comma separated IDs of instances you want to describe.')

        parser.add_argument('-s', '--status', dest='status',
                action='store', type=str, default='',
                help='instance status: pending, running, stopped, terminated, ceased')

        parser.add_argument('-m', '--image_id', dest='image_id',
                            action='store', type=str, default='',
                            help='the image id of instances.')

        parser.add_argument('-t', '--instance_type', dest='instance_type',
                            type=str, default=None,
                            help='instance type: small_b, small_c, medium_a, medium_b, medium_c, \
                            large_a, large_b, large_c')

        parser.add_argument('-W', '--search_word', dest='search_word',
                action='store', type=str, default='',
                help='the combined search column')

        parser.add_argument('-V', '--verbose', dest='verbose',
                action='store', type=int, default=0,
                help='the number to specify the verbose level, larger the number, the more detailed information will be returned.')

    @classmethod
    def get_params(cls, args):
        params = {}

        for op in cls.base_optional:
            if hasattr(args, op) and getattr(args, op):
                params[op] = getattr(args, op)

        # add instances
        if args.instances:
            instances = args.instances.split(',')
            for i in range(len(instances)):
                key = "instances.%d" % (i+1)
                params[key] = instances[i]

        # add image_id 
        if args.image_id:
            image_id = args.image_id.split(',')
            for i in range(len(image_id)):
                key = "image_id.%d" % (i+1)
                params[key] = image_id[i]

        # add instance_type
        if args.instance_type:
            instance_type = args.instance_type.split(',')
            for i in range(len(instance_type)):
                key = "instance_type.%d" % (i+1)
                params[key] = instance_type[i]
        return params


class TerminateInstancesAction(BaseAction):
    
    name = "TerminateInstances"
    base_optional = []

    @classmethod
    def add_subparser(cls, subparsers):
        parser = subparsers.add_parser('terminate-instances', help='terminate instances')
        parser.add_argument('-i', '--instances', dest='instances',
                action='store', type=str, default='', required=True,
                help='the comma separated IDs of instances you want to terminate.')

    @classmethod
    def get_params(cls, args):
        params = {}
        instances = args.instances.split(',')
        for i in range(len(instances)):
            key = "instances.%d" % (i+1)
            params[key] = instances[i]
        return params

class QShell(object):
    action_map = {
        "run-instances": RunInstancesAction,
        "describe-instances": DescribeInstancesAction,
        "terminate-instances": TerminateInstancesAction,
    }
    
    url = "https://api.qingcloud.com/iaas/"
    
    def get_base_parser(self):
        parser = argparse.ArgumentParser(prog='qingcloud client')
        return parser
    
    def get_subcommand_parser(self):
        parser = self.get_base_parser()
        subparsers = parser.add_subparsers()
        
        for sub in self.action_map.values():
            sub.add_subparser(subparsers)
        return parser
    
    def load_config(self):
        try:
            home = os.environ['HOME']
            user_config = os.path.join(home, '.qingcloud/config.yaml')
        except KeyError:
            pass

        if os.path.isfile(user_config):
            cfg_file = user_config
        else:
            work_dir = os.path.dirname(os.path.realpath(__file__))
            cfg_file = os.path.join(work_dir, 'config.yaml')

        try:
            conf = qclient.utils.parse_config(cfg_file)
            return conf
        except Exception, e:
            print(e)
            sys.exit(1)
       
    def main(self, argv):
        subcommand_parser = self.get_subcommand_parser()
        args = subcommand_parser.parse_args(argv)
        action = self.action_map[argv[0]]
        params = action.get_params(args)
        params['action'] = action.name
        print params
        conf = self.load_config()
        send_http(self.url, params, conf)


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
