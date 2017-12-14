# -*- coding: utf-8 -*-
'''
Configure a Pacemaker cluster using crmsh
=========================================

Configure a Pacemaker cluster using the crmsh
cluster shell.

:depends: crmsh
'''
from __future__ import absolute_import
import re

from salt.ext import six
from salt.exceptions import CommandExecutionError


def property(**kwargs):
    '''
    Set a cluster property

    kwargs
        property \"key=value\" pairs

    This function will reject to run if current node is not DC.


    CLI Example:

    .. code-block:: bash

        salt '*' crmsh.property stonith-enabled=true cluster-name=test
    '''
    cmd = ['crm', 'configure', 'property']

    for k, v in kwargs.items():
        if k.startswith('__pub_'):
            continue
        cmd.append("%s=%s" % (k, v))
    if len(cmd) == 3:
        raise CommandExecutionError("Except at least one key=value pair")

    return __salt__['cmd.run_all'](cmd, output_loglevel='trace', python_shell=False)


def show(*args, **kwargs):
    '''
    Display CIB objects

    args
        list of show type, valid elements include:
        object IDs,
        object type, use the \'type:\' prefix,
        object tag, use the \'tag:\' prefix,
        constraints related to a primitive, use the \'related:\' prefix.
        (default: None)

        type :: node | primitive | group | clone | ms | rsc_template | bundle
              | location | colocation | order
              | rsc_ticket
              | property | rsc_defaults | op_defaults
              | fencing_topology
              | role | user | acl_target
              | tag
    kwargs
        options \"key=value\" pairs, include:
        xml
            show CIB objects with XML format (default: False)
        changed
            show all modified objects (default: False)


    CLI Example:

    .. code-block:: bash

        salt '*' crmsh.show
        salt '*' crmsh.show vip type:node
        salt '*' crmsh.show related:vip xml=True
        salt '*' crmsh.show changed=True
    '''
    cmd = ['crm', 'configure', 'show']

    xml = kwargs.get('xml', False)
    if xml is True:
        cmd += ["xml"]
    changed = kwargs.get('changed', False)
    if changed is True:
        cmd += ["changed"]
        return __salt__['cmd.run_all'](cmd, output_loglevel='trace', python_shell=False)
    if args:
        cmd += args

    return __salt__['cmd.run_all'](cmd, output_loglevel='trace', python_shell=False)
