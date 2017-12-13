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


def _dc():
    '''
    check whether we are DC node
    '''
    import socket

    try:
        res = __salt__['cmd.run_all']("crmadmin -D")
    except:
        return False
    if 'stdout' in res.keys():
        dc = res['stdout'].split()[-1]
        if dc != socket.gethostname():
            return False

    return True

default_attr={"output_loglevel"="trace", "python_shell"=False}

configure_table = {
    {"cmd" : "show",
        "doc" :
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
                salt '*' crmsh.configure_show
                salt '*' crmsh.configure_show vip type:node
                salt '*' crmsh.configure_show related:vip xml=True
                salt '*' crmsh.configure_show changed=True
            ''',
        "check" : None,
        "exception" : None,
        "onlyDC" : False,
        "attrs" : {"xml":False,
                 "changed":False}
    },
    {"cmd" : "property",
        "doc" :
            '''
            Set a cluster property

            kwargs
                property \"key=value\" pairs
            This function will reject to run if current node is not DC.

            CLI Example:
            .. code-block:: bash
                salt '*' crmsh.configure_property stonith-enabled=true cluster-name=test
            ''',
        "check" : (None, 1),
        "onlyDC" : True,
        "exception" : exception_property,
        "attrs" : {}
    }
}

def exception_property(args, kwargs):
    remove_keys = []

    for k in kwargs.keys():
        if k.startswith('__pub_'):
            remove_keys += k

    for k in remove_keys:
        kwargs.pop(k)

def show_support_cmd():
    cmd_list = []
    for ele in configure_table:
        cmd_list += ele["cmd"]
    raise CommandExecutionError(", ".join(cmd_list))

def show_cmd_usage(cmd_dict):
    raise CommandExecutionError(cmd_dict["doc"])

def show_cmd_attr(cmd_dict):
    raise CommandExecutionError(", ".join(cmd_dict["attr"].keys()))

def configure(*args, **kwargs):
    '''
    CLI Example:

    .. code-block:: bash
       salt '*' crmsh.configure cmd=show
       salt '*' crmsh.configure cmd=property
    '''
    crm = ["crm", "configure"]

    for ele in configure_table:
        if kwargs.get("cmd", "") == ele.get("cmd"):
            cmd_dict = ele
            break
    else:
        return show_support_cmd()

    kwargs.pop("cmd")
    crm += cmd_dict["cmd"]

    # Run an exception workflow for the if necessary
    if cmd_dict["check"] is not None:
        if (cmd_dict["check"][0] is not None and len(args) < cmd_dict["check"][0]) or
           (cmd_dict["check"][1] is not None and len(kwargs) < cmd_dict["check"][1]):
            return show_cmd_usage(cmd_dict)

    # Run an exception workflow for the if necessary
    # May exit after exception workflow
    if cmd_dict["exception"] is not None:
        cmd_dict["exception"](args, kwargs)

    cmd_dict["attr"].update(default_attr)

    for key in kwargs:
        if key in cmd_dict["attr"]:
            cmd_dict["attr"][key] = kwargs[key]
        else:
            return show_cmd_attr(cmd_dict)

    if cmd_dict["onlyDC"] and not _dc():
        raise CommandExecutionError("This function can only run at DC node")

    crm += args

    return __salt__['cmd.run_all'](crm, **cmd_dict["attr"])
