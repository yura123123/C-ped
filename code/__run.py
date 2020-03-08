from sys import exc_info
from traceback import print_exception

from server import main as run_server

from config import CFG, CFG_Exception

from global_vars import init_vars

def run():
    if CFG == "Error":
        raise CFG_Exception("Internal error setting up config.")
    init_vars(CFG)
    # see server.py for more detail, all server-related stuff is handled there.
    run_server(CFG)


if __name__ == "__main__":
    # Semi-automatic backend restarting in case it dropped for any reason.
    while True:
        try:
            run()

        # Anything in run() called for a forced.
        except SystemExit:
            break

        # Exceptions displaying.
        except Exception as err:
            try:
                exc_info = exc_info()
            finally:
                # Display the *original* exception
                print(err)
                print_exception(*exc_info)
                del exc_info

        stopper = input().lower()
        if stopper == "q" or stopper == "quit":
            break

    print("Stopping server...")
