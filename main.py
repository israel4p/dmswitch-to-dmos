#!/usr/bin/env python3


def read_mpls():
    with open('config_mpls.txt') as conf:
        configs = conf.readlines()

    list_configs = []
    dict_configs = {}

    for config in configs:
        if 'shutdown' not in config:
            if 'vpn' in config:
                dict_configs[config.split()[0]] = config.split()[1]

            if 'name' in config:
                dict_configs[config.split()[0]] = config.split()[1]

            if 'neighbor' in config:
                dict_configs[config.split()[0]] = config.split()[1]
        else:
            list_configs.append(dict_configs)
            dict_configs = {}

    return list_configs


def read_vlan(config_mpls):
    with open('config_vlan.txt') as conf:
        configs = conf.readlines()

    list_configs = []
    new_configs = []

    for config in configs:
        if '!' not in config.strip():
            list_configs.append(config)
        else:
            for mpls in config_mpls:
                if mpls['vpn'] in list_configs[0]:
                    mpls['tag'] = list_configs[-1].split()[1]
                    mpls['interface'] = list_configs[-1].split()[-1]
                    new_configs.append(mpls)

            list_configs = []

    return new_configs


def create_comands(configs):
    mpls = 'mpls l2vpn vpws-group VPWS-CONNECTX'

    for config in configs:
        print('%s vpn %s' % (mpls, config['vpn']))

        if 'name' in config:
            print('description %s' % config['name'])

        print('neighbor %s pw-id %s' % (config['neighbor'], config['vpn']))

        if config['tag'] == 'tagged':
            print('pw-type vlan')

        print('exit')
        print('access-interface gigabit-ethernet-1/%s' % config['interface'])

        if config['tag'] == 'tagged':
            print('dot1q %s' % config['vpn'])

        print('top\n')

    for config in configs:
        if 'name' in config:
            print('interface gigabit-ethernet 1/%s' % config['interface'])
            print('description %s' % config['name'])
            print('top\n')


config_mpls = read_mpls()
configs = read_vlan(config_mpls)
create_comands(configs)
