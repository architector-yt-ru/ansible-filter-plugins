
# server {{ backend | host_short }} {{ backend }}:80 check inter 10s rise 2 fall 2 weight 1 {{ ' backup' if dc != backend | host_dc else '' }}

def get_short_hostname(data):

  return data.split('.')[0]

def get_dc_name(data):

  return data.split('.')[0].split('-')[-1]

def get_hostlist_mixed(data, groups={}):

  hostlist = []

  for v in data:
    hosts = []
    if type(v) is dict:
      for k in v.keys():
        if groups.get(k):
          hosts += groups.get(k)
        else: 
          hosts.append(k)
    else:
      if groups.get(v):
        hosts += groups.get(v)
      else:
        hosts.append(v)

    hostlist += hosts

  return hostlist

#     - instance: test
#       defaults: { mysql_port: 3200, mysql_rsync_port: 4313, mysql_master_port: 1513 }
#       hosts: 
#         - mysql-02-sas.dev.test.local
#         - mysql-03-sas.dev.test.local: { mysql_port: 3200 }
#         - group_name: { mysql_port: 3199 }


def get_host_defaults(data, host, groups={}, extra={}):

  defaults = data.get('defaults', {})
  defaults.update(extra)

  if not data.get('hosts'):
    return defaults

  for v in data['hosts']:
    hosts = []
    #  - host_w_params: { mysql_port: 3199 }
    #  - group_name_w_params: { mysql_port: 3199 }
    if type(v) is dict:
      for k in v.keys():
        if groups.get(k):
          hosts = groups.get(k)
        else: 
          hosts.append(k)
        # merge params
        if host in hosts:
          defaults.update(v[k])
          return defaults

  return defaults


class FilterModule(object):
    ''' custom jinja2 filters for working with collections '''

    def filters(self):
        return {
            'host_short': get_short_hostname,
            'host_dc': get_dc_name,
            'host_list': get_hostlist_mixed,
            'host_defaults': get_host_defaults,
        }

