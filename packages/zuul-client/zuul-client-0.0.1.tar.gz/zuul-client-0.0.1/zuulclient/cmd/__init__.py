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

import logging

from zuulclient.api import ZuulRESTClient
# from zuulclient.api import ZuulRESTException
from zuulclient.common.client import CLI
from zuulclient.common import get_default


class ZuulClient(CLI):
    app_name = 'zuul-client'
    app_description = 'Zuul User CLI'
    log = logging.getLogger("zuul-client")

    def createParser(self):
        parser = super(ZuulClient, self).createParser()
        parser.add_argument('--auth-token', dest='auth_token',
                            required=False,
                            default=None,
                            help='Authentication Token, required by '
                                 'admin commands')
        parser.add_argument('--zuul-url', dest='zuul_url',
                            required=False,
                            default=None,
                            help='Zuul base URL, needed if using the '
                                 'client without a configuration file')
        parser.add_argument('--use-config', dest='zuul_config',
                            required=False,
                            default=None,
                            help='A predefined configuration in .zuul.conf')
        parser.add_argument('--insecure', dest='verify_ssl',
                            required=False,
                            action='store_false',
                            help='Do not verify SSL connection to Zuul '
                                 '(Defaults to False)')
        return parser

    def createCommandParsers(self, parser):
        subparsers = super(ZuulClient, self).createCommandParsers(parser)
        # Add any specific zuul-client command subparser here
        return subparsers

    def _main(self, args=None):
        self.parseArguments(args)
        if not self.args.zuul_url:
            self.readConfig()
        self.setup_logging()
        # TODO make func return specific return codes
        if self.args.func():
            return 0
        else:
            return 1

    def get_client(self):
        if self.args.zuul_url and self.args.zuul_config:
            raise Exception('Either specify --zuul-url or use a config file')
        if self.args.zuul_url:
            self.log.debug(
                'Using Zuul URL provided as argument to instantiate client')
            client = ZuulRESTClient(self.args.zuul_url,
                                    self.args.verify_ssl,
                                    self.args.auth_token)
            return client
        conf_sections = self.config.sections()
        if len(conf_sections) == 1 and self.args.zuul_config is None:
            zuul_conf = conf_sections[0]
            self.log.debug(
                'Using section "%s" found in '
                'config to instantiate client' % zuul_conf)
        elif self.args.zuul_config and self.args.zuul_config in conf_sections:
            zuul_conf = self.args.zuul_config
        else:
            raise Exception('Unable to find a way to connect to Zuul, '
                            'provide the "--zuul-url" argument or set up a '
                            '.zuul.conf file.')
        server = get_default(self.config,
                             zuul_conf, 'url', None)
        verify = get_default(self.config, zuul_conf,
                             'verify_ssl',
                             self.args.verify_ssl)
        # Allow token override by CLI argument
        auth_token = self.args.auth_token or get_default(self.config,
                                                         zuul_conf,
                                                         'auth_token',
                                                         None)
        if server is None:
            raise Exception('Missing "url" configuration value')
        client = ZuulRESTClient(server, verify, auth_token)
        return client


def main():
    ZuulClient().main()
