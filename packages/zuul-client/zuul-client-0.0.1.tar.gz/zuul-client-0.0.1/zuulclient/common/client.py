# Copyright 2020 Red Hat, inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


# TODO This is taken straight from zuul.cmd - Refactor so the boilerplate Code
# lives in one place only.

import argparse
import configparser
import logging
import os
import prettytable
import sys
import textwrap
import time


class App(object):
    app_name = None  # type: str
    app_description = None  # type: str

    def __init__(self):
        self.args = None
        self.config = None

    def _get_version(self):
        from zuulclient.version import version_info
        return "Zuul-client version: %s" % version_info.release_string()

    def createParser(self):
        parser = argparse.ArgumentParser(
            description=self.app_description,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('-c', dest='config',
                            help='specify the config file')
        parser.add_argument('--version', dest='version', action='version',
                            version=self._get_version(),
                            help='show zuul version')
        return parser

    def parseArguments(self, args=None):
        parser = self.createParser()
        self.args = parser.parse_args(args)
        return parser

    def readConfig(self):
        safe_env = {
            k: v for k, v in os.environ.items()
            if k.startswith('ZUUL_')
        }
        self.config = configparser.ConfigParser(safe_env)
        if self.args.config:
            locations = [self.args.config]
        else:
            locations = ['~/.zuul.conf']
        for fp in locations:
            if os.path.exists(os.path.expanduser(fp)):
                self.config.read(os.path.expanduser(fp))
                return
        raise Exception("Unable to locate config file in %s" % locations)


class CLI(App):
    """Common code used by the admin CLI and zuul-client."""

    def createParser(self):
        parser = super(CLI, self).createParser()
        parser.add_argument('-v', dest='verbose', action='store_true',
                            help='verbose output')
        self.createCommandParsers(parser)
        return parser

    def createCommandParsers(self, parser):
        subparsers = parser.add_subparsers(title='commands',
                                           description='valid commands',
                                           help='additional help')
        # Add parsers that are common to RPC and REST clients
        self.add_autohold_subparser(subparsers)
        self.add_autohold_delete_subparser(subparsers)
        self.add_autohold_info_subparser(subparsers)
        self.add_autohold_list_subparser(subparsers)
        self.add_enqueue_subparser(subparsers)
        self.add_enqueue_ref_subparser(subparsers)
        self.add_dequeue_subparser(subparsers)
        self.add_promote_subparser(subparsers)

        return subparsers

    def parseArguments(self, args=None):
        parser = super(CLI, self).parseArguments(args)
        if not getattr(self.args, 'func', None):
            parser.print_help()
            sys.exit(1)
        if self.args.func == self.enqueue_ref:
            # if oldrev or newrev is set, ensure they're not the same
            if (self.args.oldrev is not None) or \
               (self.args.newrev is not None):
                if self.args.oldrev == self.args.newrev:
                    raise Exception(
                        "The old and new revisions must not be the same.")
            # if they're not set, we pad them out to zero
            if self.args.oldrev is None:
                self.args.oldrev = '0000000000000000000000000000000000000000'
            if self.args.newrev is None:
                self.args.newrev = '0000000000000000000000000000000000000000'
        if self.args.func == self.dequeue:
            if self.args.change is None and self.args.ref is None:
                raise Exception("Change or ref needed.")
            if self.args.change is not None and self.args.ref is not None:
                raise Exception(
                    "The 'change' and 'ref' arguments are mutually exclusive.")

    def setup_logging(self):
        """Client logging does not rely on conf file"""
        if self.args.verbose:
            logging.basicConfig(level=logging.DEBUG)

    def _main(self, args=None):
        self.parseArguments(args)
        self.readConfig()
        self.setup_logging()

        if self.args.func():
            return 0
        else:
            return 1

    def main(self):
        try:
            sys.exit(self._main())
        except Exception as e:
            self.log.error(e)
            sys.exit(1)

    def get_client(self):
        raise NotImplementedError('No client defined')

    def add_autohold_subparser(self, subparsers):
        cmd_autohold = subparsers.add_parser(
            'autohold', help='hold nodes for failed job')
        cmd_autohold.add_argument('--tenant', help='tenant name',
                                  required=True)
        cmd_autohold.add_argument('--project', help='project name',
                                  required=True)
        cmd_autohold.add_argument('--job', help='job name',
                                  required=True)
        cmd_autohold.add_argument('--change',
                                  help='specific change to hold nodes for',
                                  required=False, default='')
        cmd_autohold.add_argument('--ref', help='git ref to hold nodes for',
                                  required=False, default='')
        cmd_autohold.add_argument('--reason', help='reason for the hold',
                                  required=True)
        cmd_autohold.add_argument('--count',
                                  help='number of job runs (default: 1)',
                                  required=False, type=int, default=1)
        cmd_autohold.add_argument(
            '--node-hold-expiration',
            help=('how long in seconds should the node set be in HOLD status '
                  '(default: scheduler\'s default_hold_expiration value)'),
            required=False, type=int)
        cmd_autohold.set_defaults(func=self.autohold)

    def autohold(self):
        if self.args.change and self.args.ref:
            raise Exception(
                "Change and ref can't be both used for the same request")
        if "," in self.args.change:
            raise Exception("Error: change argument can not contain any ','")

        node_hold_expiration = self.args.node_hold_expiration
        client = self.get_client()
        r = client.autohold(
            tenant=self.args.tenant,
            project=self.args.project,
            job=self.args.job,
            change=self.args.change,
            ref=self.args.ref,
            reason=self.args.reason,
            count=self.args.count,
            node_hold_expiration=node_hold_expiration)
        return r

    def add_autohold_delete_subparser(self, subparsers):
        cmd_autohold_delete = subparsers.add_parser(
            'autohold-delete', help='delete autohold request')
        cmd_autohold_delete.set_defaults(func=self.autohold_delete)
        cmd_autohold_delete.add_argument('--tenant', help='tenant name',
                                         required=True, default=None)
        cmd_autohold_delete.add_argument('id', metavar='REQUEST_ID',
                                         help='the hold request ID')

    def autohold_delete(self):
        client = self.get_client()
        return client.autohold_delete(self.args.id, self.args.tenant)

    def add_autohold_info_subparser(self, subparsers):
        cmd_autohold_info = subparsers.add_parser(
            'autohold-info', help='retrieve autohold request detailed info')
        cmd_autohold_info.set_defaults(func=self.autohold_info)
        cmd_autohold_info.add_argument('--tenant', help='tenant name',
                                       required=True, default=None)
        cmd_autohold_info.add_argument('id', metavar='REQUEST_ID',
                                       help='the hold request ID')

    def autohold_info(self):
        client = self.get_client()
        request = client.autohold_info(self.args.id, self.args.tenant)

        if not request:
            print("Autohold request not found")
            return False

        print("ID: %s" % request['id'])
        print("Tenant: %s" % request['tenant'])
        print("Project: %s" % request['project'])
        print("Job: %s" % request['job'])
        print("Ref Filter: %s" % request['ref_filter'])
        print("Max Count: %s" % request['max_count'])
        print("Current Count: %s" % request['current_count'])
        print("Node Expiration: %s" % request['node_expiration'])
        print("Request Expiration: %s" % time.ctime(request['expired']))
        print("Reason: %s" % request['reason'])
        print("Held Nodes: %s" % request['nodes'])

        return True

    def add_autohold_list_subparser(self, subparsers):
        cmd_autohold_list = subparsers.add_parser(
            'autohold-list', help='list autohold requests')
        cmd_autohold_list.add_argument('--tenant', help='tenant name',
                                       required=True)
        cmd_autohold_list.set_defaults(func=self.autohold_list)

    def autohold_list(self):
        client = self.get_client()
        autohold_requests = client.autohold_list(tenant=self.args.tenant)

        if not autohold_requests:
            print("No autohold requests found")
            return True

        table = prettytable.PrettyTable(
            field_names=[
                'ID', 'Tenant', 'Project', 'Job', 'Ref Filter',
                'Max Count', 'Reason'
            ])

        for request in autohold_requests:
            table.add_row([
                request['id'],
                request['tenant'],
                request['project'],
                request['job'],
                request['ref_filter'],
                request['max_count'],
                request['reason'],
            ])

        print(table)
        return True

    def add_enqueue_subparser(self, subparsers):
        cmd_enqueue = subparsers.add_parser('enqueue', help='enqueue a change')
        cmd_enqueue.add_argument('--tenant', help='tenant name',
                                 required=True)
        cmd_enqueue.add_argument('--pipeline', help='pipeline name',
                                 required=True)
        cmd_enqueue.add_argument('--project', help='project name',
                                 required=True)
        cmd_enqueue.add_argument('--change', help='change id',
                                 required=True)
        cmd_enqueue.set_defaults(func=self.enqueue)

    def enqueue(self):
        client = self.get_client()
        r = client.enqueue(
            tenant=self.args.tenant,
            pipeline=self.args.pipeline,
            project=self.args.project,
            change=self.args.change)
        return r

    def add_enqueue_ref_subparser(self, subparsers):
        cmd_enqueue = subparsers.add_parser(
            'enqueue-ref', help='enqueue a ref',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent('''\
            Submit a trigger event

            Directly enqueue a trigger event.  This is usually used
            to manually "replay" a trigger received from an external
            source such as gerrit.'''))
        cmd_enqueue.add_argument('--tenant', help='tenant name',
                                 required=True)
        cmd_enqueue.add_argument('--pipeline', help='pipeline name',
                                 required=True)
        cmd_enqueue.add_argument('--project', help='project name',
                                 required=True)
        cmd_enqueue.add_argument('--ref', help='ref name',
                                 required=True)
        cmd_enqueue.add_argument(
            '--oldrev', help='old revision', default=None)
        cmd_enqueue.add_argument(
            '--newrev', help='new revision', default=None)
        cmd_enqueue.set_defaults(func=self.enqueue_ref)

    def enqueue_ref(self):
        client = self.get_client()
        r = client.enqueue_ref(
            tenant=self.args.tenant,
            pipeline=self.args.pipeline,
            project=self.args.project,
            ref=self.args.ref,
            oldrev=self.args.oldrev,
            newrev=self.args.newrev)
        return r

    def add_dequeue_subparser(self, subparsers):
        cmd_dequeue = subparsers.add_parser('dequeue',
                                            help='dequeue a buildset by its '
                                                 'change or ref')
        cmd_dequeue.add_argument('--tenant', help='tenant name',
                                 required=True)
        cmd_dequeue.add_argument('--pipeline', help='pipeline name',
                                 required=True)
        cmd_dequeue.add_argument('--project', help='project name',
                                 required=True)
        cmd_dequeue.add_argument('--change', help='change id',
                                 default=None)
        cmd_dequeue.add_argument('--ref', help='ref name',
                                 default=None)
        cmd_dequeue.set_defaults(func=self.dequeue)

    def dequeue(self):
        client = self.get_client()
        r = client.dequeue(
            tenant=self.args.tenant,
            pipeline=self.args.pipeline,
            project=self.args.project,
            change=self.args.change,
            ref=self.args.ref)
        return r

    def add_promote_subparser(self, subparsers):
        cmd_promote = subparsers.add_parser('promote',
                                            help='promote one or more changes')
        cmd_promote.add_argument('--tenant', help='tenant name',
                                 required=True)
        cmd_promote.add_argument('--pipeline', help='pipeline name',
                                 required=True)
        cmd_promote.add_argument('--changes', help='change ids',
                                 required=True, nargs='+')
        cmd_promote.set_defaults(func=self.promote)

    def promote(self):
        client = self.get_client()
        r = client.promote(
            tenant=self.args.tenant,
            pipeline=self.args.pipeline,
            change_ids=self.args.changes)
        return r
