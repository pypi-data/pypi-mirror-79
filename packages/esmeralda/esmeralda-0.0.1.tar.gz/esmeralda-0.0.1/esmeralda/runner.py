#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import subprocess
from subprocess import PIPE
import json
from tempfile import NamedTemporaryFile
import uuid

import pendulum
from djali.couchdb import CloudiControl
from quasimodo.amqp import QueueWorkerSkeleton
from jinja2 import Environment, BaseLoader

from esmeralda.defaults import ESMERALDA_CONFIG

TIME_OUT_DEFAULT = pendulum.Duration(hours=1)

INVENTORY_TEMPLATE = """[{{ group_name }}]
{{ inventory_hostname }}
"""

FALLBACK_ANSIBLE_CFG_REL = 'etc/ansible.cfg'

FALLBACK_INVENTORY = 'etc/00-merged-dummy'

FALLBACK_PLAYBOOK = 'information-dumping.yml'


def setup_ansible_environment(**kwargs):
    ansible_root_path = kwargs.get(
        "ansible_root_path", ESMERALDA_CONFIG['ansible_root_path'])
    ansible_config_path = kwargs.get(
        "ansible_config_path",
        os.path.join(ansible_root_path, FALLBACK_ANSIBLE_CFG_REL))

    os.environ['ANSIBLE_CONFIG'] = ansible_config_path
    os.environ['ANSIBLE_STDOUT_CALLBACK'] = 'json'


class TimeOutController(object):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        db_url = kwargs.get("db_url", ESMERALDA_CONFIG['time_out_url'])
        self.cc = CloudiControl(db_url)

    def set_timeout(self, key, time_out=None):
        if time_out is None:
            time_out = TIME_OUT_DEFAULT

        u_now = pendulum.now(tz=pendulum.UTC)
        blocked_until = u_now + time_out
        doc = {
            'time_out': blocked_until.to_iso8601_string()
        }
        self.cc[key] = doc
        self.log.info("{key} will be in time out until {time_out}".format(
            key=key, **doc))

    def in_timeout(self, key):
        try:
            doc = self.cc[key]
        except KeyError:
            self.log.info("{key} is not in time out".format(key=key))
            return False

        blocked_until = pendulum.parse(doc['time_out'])
        u_now = pendulum.now(tz=pendulum.UTC)

        self.log.info(
            "{key} is supposed to be in time out until {time_out}".format(
                key=key, **doc))

        return u_now < blocked_until


class Dispatcher(QueueWorkerSkeleton):
    def __init__(self, *args, **kwargs):
        amqp_port = kwargs.get("amqp_port", ESMERALDA_CONFIG['amqp_port'])

        super().__init__(
            self,
            port=amqp_port,
            queue_declare_arguments=kwargs.get('queue_declare_arguments'),
            *args, **kwargs)

    def _handle_request(self, payload, **kwargs):
        """
        Message/request handling function.
        To be implemented by deriving classes.
        """
        try:
            inventory_hostname = payload['identity']['inventory_hostname']
        except KeyError:
            inventory_hostname = payload['inventory_hostname']

        identity = payload.get('identity')
        if identity is None:
            identity = dict(
                inventory_hostname=inventory_hostname,
                serial_number=uuid.uuid4().hex
            )

        toc = TimeOutController()
        in_time_out = toc.in_timeout(inventory_hostname)

        if in_time_out:
            self.log.info(
                "{inventory_hostname}/{serial_number} is in time out.".format(
                    **identity))
            return True

        toc.set_timeout(inventory_hostname)

        self.log.info("Dispatching update request ... ")
        self.add_to_queue(payload, queue=ESMERALDA_CONFIG['dispatch_queue'])

        return True


class AnsibleExecutor(QueueWorkerSkeleton):
    def __init__(self, *args, **kwargs):
        amqp_port = kwargs.get("amqp_port", ESMERALDA_CONFIG['amqp_port'])

        super().__init__(
            self,
            port=amqp_port,
            queue_declare_arguments=kwargs.get('queue_declare_arguments'),
            *args, **kwargs)

    def _handle_request(self, payload, **kwargs):
        """
        Message/request handling function.
        To be implemented by deriving classes.
        """
        wrap = AnsibleRunWrapper()

        try:
            inventory_hostname = payload['identity']['inventory_hostname']
        except KeyError:
            inventory_hostname = payload['inventory_hostname']

        rv = wrap.run(inventory_hostname=inventory_hostname)

        if rv is not False:
            return True

        return False


class AnsibleRunWrapper(object):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.ansible_root_path = kwargs.get(
            "ansible_root_path", ESMERALDA_CONFIG['ansible_root_path'])
        self.ansible_config_path = kwargs.get(
            "ansible_config_path",
            os.path.join(self.ansible_root_path, FALLBACK_ANSIBLE_CFG_REL))

        try:
            self.verbose = int(kwargs.get("verbose"))
        except Exception:
            self.verbose = 0

    def _run(self, **kwargs):
        playbook_path = kwargs.get(
            "playbook_path",
            os.path.join(self.ansible_root_path, FALLBACK_PLAYBOOK)
        )

        inventory_path = kwargs.get(
            "inventory_path",
            os.path.join(self.ansible_root_path, FALLBACK_INVENTORY)
        )

        setup_ansible_environment(ansible_root_path=self.ansible_root_path,
                                  ansible_config_path=self.ansible_config_path)
        call_args = [
            ESMERALDA_CONFIG['ansible_playbook_binary'],
            '-i',
            inventory_path,
            playbook_path
        ]

        if self.verbose:
            self.log.info("Trying to run {!r}".format(call_args))

        proc = subprocess.run(call_args, stdout=PIPE, stderr=PIPE,
                              cwd=self.ansible_root_path)
        result = json.loads(proc.stdout)
        rc = proc.returncode

        if self.verbose:
            self.log.info("RC={!r}".format(rc))

            if self.verbose >= 10:
                for line in json.dumps(result, indent=2).split("\n"):
                    self.log.info(line)

        return rc, result

    def run(self, **kwargs):
        if kwargs.get("inventory_hostname"):
            inventory_template = Environment(
                loader=BaseLoader).from_string(INVENTORY_TEMPLATE)
            rendered_inventory = inventory_template.render({
                'inventory_hostname': kwargs["inventory_hostname"],
                'group_name': 'victims'
            })

            # Create a temporary file and write the template string to it
            hosts = NamedTemporaryFile(delete=False)
            hosts.write(rendered_inventory)
            hosts.close()
            kwargs['inventory_path'] = hosts.name
        else:
            self.log.warning(
                "No inventory_hostname! Using default inventory path!")

        try:
            return self._run(**kwargs)
        except Exception as exc:
            self.log.error("Failed to run: {!s}".format(exc))
            return False


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # logging.basicConfig(loglevel=logging.DEBUG)
    db_url = 'http://donny:Dimpfelmoser89Lima@localhost:55984/time_out'
    toc = TimeOutController(db_url=db_url)
    toc.in_timeout('hatsnet')
    toc.set_timeout("bla")
    toc.in_timeout('bla')
