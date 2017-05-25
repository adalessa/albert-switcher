#!/usr/bin/env python

import os
import sys
import json
import subprocess
import copy
import re
import gtk

albert_op = os.environ.get("ALBERT_OP")

if albert_op == "METADATA":
    metadata="""{
      "iid":"org.albert.extension.external/v2.0",
      "name":"Switcher",
      "version":"1.0",
      "author":"Ariel DAlessandro",
      "dependencies":["wmctrl"],
      "trigger":"$"
    }"""
    print(metadata)
    sys.exit(0)

elif albert_op == "NAME":
    sys.exit(0)

elif albert_op == "INITIALIZE":
    sys.exit(0)

elif albert_op == "FINALIZE":
    sys.exit(0)

elif albert_op == "SETUPSESSION":
    sys.exit(0)

elif albert_op == "SETUPSESSION":
    sys.exit(0)

elif albert_op == "TEARDOWNSESSION":
    sys.exit(0)

elif albert_op == "QUERY":

    albert_query = os.environ.get("ALBERT_QUERY")
    query = albert_query[1:]
    class Object(object):
        pass

    items = []
    windows = subprocess.check_output(['/bin/sh', '-c', 'wmctrl -l'])
    windows = windows.split("\n")
    a=0
    for window in windows:
        parts = re.compile("([^\s]+) ([ ,-][0-1]) ([^\s]+) (.*$)").split(window)
        if len(parts) != 6:
            continue
        if parts[2] == '-1':
            continue


        #search the icon
        icon = ''
        ic=''
        rawClass=subprocess.check_output(['/bin/sh', '-c', 'xprop -id {0} | grep WM_CLASS'.format(parts[1])])
        wmClass=re.compile('WM_CLASS\(STRING\) = "([^\s]+)"').split(rawClass)
        if len(wmClass) == 3:
            ic=wmClass[1]
            icon_theme = gtk.icon_theme_get_default()
            icon_info = icon_theme.lookup_icon(ic, 48, 0)
            if icon_info:
                icon=icon_info.get_filename()

        #
        title='{}-{}'.format(ic, parts[4])
        if len(query) > 1 and title.lower().find(query.lower()) == -1:
              continue

        item = Object()
        item.id = parts[1]
        item.name = parts[4]
        item.description = ic
        item.icon = icon
        item.actions = []

        action = Object()
        action.command = "sh"
        action.name = "Open {}".format(ic)
        action.arguments = ["-c", 'wmctrl -iR {0}'.format(parts[1])]
        item.actions.append(action)

        action = Object()
        action.command = "sh"
        action.name = "Close {}".format(parts[4])
        action.arguments = ["-c", 'wmctrl -ic {0}'.format(parts[1])]
        item.actions.append(action)

        items.append(item)



    results = []
    for it in items:
        results += [json.dumps(it, default=lambda o: o.__dict__)]

    print('{"items": [' + ", ".join(results) + "]}")
    sys.exit(0)

elif albert_op == "COPYTOCLIPBOARD":
    clipboard.copy(sys.argv[1])
    sys.exit(0)
