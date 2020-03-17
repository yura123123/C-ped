DELIMETERS = [".", ",", ":", "?", "!", ";"]

client_count = 0
max_client_count = 0

clients_by_sid = {}
client_infos_by_ip = {}
client_infos_by_user_id = {}


def disconnect_message(request, reason=None):
    print(
        "Disconnected("
        + str(client_count)
        + "/"
        + str(max_client_count)
        + ") user("
        + str(request.remote_addr)
        + ")."
        + (" Reason: " + reason)
        if reason
        else ""
    )


def redirect_error(error_message, error_code=None):
    page = "<hr>"
    page += "<b><center>"
    if error_code is not None:
        page += "<i>" + str(error_code) + "</i>: "

    page += error_message
    page += "<b></center>"
    page += "<hr>"
    page += '<a class="button" href="/">Main page.</a>'
    return page


def init_vars(CFG):
    global max_client_count
    global max_clients_per_ip

    max_client_count = CFG["Server"].getint("max_client_count", -1)
    max_clients_per_ip = CFG["Server"].getint("max_clients_per_ip", 1)
