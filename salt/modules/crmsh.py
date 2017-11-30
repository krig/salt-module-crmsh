# -*- coding: utf-8 -*-
'''
Configure a Pacemaker cluster using crmsh
=========================================

Configure a Pacemaker cluster using the crmsh
cluster shell.

:depends: crmsh
'''
from __future__ import absolute_import
from salt.ext import six
import re


def configure_show(xml=False, changed=False, show_type=None):
    '''
    Display CIB objects

    xml
        show CIB objects with XML format (default: False)
    changed
        show all modified objects (default: False)
    show_type
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

    CLI Example:

    .. code-block:: bash

        salt '*' crmsh.configure_show 
        salt '*' crmsh.configure_show show_type="vip, type:node"
        salt '*' crmsh.configure_show xml=True show_type='related:vip'
        salt '*' crmsh.configure_show changed=True
    '''
    cmd = ['crm', 'configure', 'show']

    if xml is True:
        cmd += ["xml"]
    if changed is True:
        cmd += ["changed"]
        return __salt__['cmd.run_all'](cmd, output_loglevel='trace', python_shell=False)
    if isinstance(show_type, six.string_types):
        cmd += re.split(',\s*|\s', show_type)
    if isinstance(show_type, (list, tuple)):
        cmd += show_type

    return __salt__['cmd.run_all'](cmd, output_loglevel='trace', python_shell=False)
