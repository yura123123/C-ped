DELIMETERS = [".", ",", ":", "?", "!", ";"]

client_count = 0
max_client_count = 0

clients_by_sid = {}
client_infos_by_ip = {}
client_infos_by_user_id = {}


def init_vars(CFG):
    global max_client_count
    global max_clients_per_ip

    max_client_count = CFG["Server"].getint("max_client_count", -1)
    max_clients_per_ip = CFG["Server"].getint("max_clients_per_ip", 1)
