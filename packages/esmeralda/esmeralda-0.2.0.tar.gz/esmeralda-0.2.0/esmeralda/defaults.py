#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

ESMERALDA_CONFIG = dict(
    time_out_url='http://time:out@localhost:5984/time_out',
    run_reports_url='http://time:out@localhost:5984/run_reports',
    ansible_root_path=os.path.join(
        os.environ.get("HOME", ''), "ansible-playbooks"),
    ansible_playbook_binary="/usr/bin/ansible-playbook",
    amqp_port = 5672,
    dispatch_queue="esmeralda_request",
    inventory='etc/00-merged-dummy',
    playbook='information-dumping.yml',
    ansible_config='etc/ansible.cfg'
)

PREFIX = 'ESMERALDA_'

for key in ESMERALDA_CONFIG:
    env_key = PREFIX + key.upper()

    try:
        ESMERALDA_CONFIG[key] = os.environ[env_key]
    except KeyError:
        pass
