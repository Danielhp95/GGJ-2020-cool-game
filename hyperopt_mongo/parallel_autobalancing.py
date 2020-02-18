import signal
import os

import logging
from multiprocessing_logging import install_mp_handler

from multiprocessing import Process, cpu_count
from subprocess import call


# Workflow:
# Start Mongo
# Launch high level python controller script
# Launch external processes
# Wait for controller to finish optimization
# kill workers
# kill mongo
def main():
    mongo_call = lambda: call(['mongod', '--dbpath', '.', '--port', '1234', '--directoryperdb'], stdout=open(os.devnull, 'w'))
    high_level_call = lambda: call(['python', 'cool_game_regym_hyperopt.py'])
    worker_call = lambda: call(['hyperopt-mongo-worker', '--mongo=localhost:1234/foo_db', '--poll-interval=0.1'])

    mongo_p = Process(target=mongo_call)
    mongo_p.start()

    high_level_p = Process(target=high_level_call)
    high_level_p.start()

    workers_p = [Process(target=worker_call)
                 for _ in range(1)]
    for p in workers_p: p.start()

    high_level_p.join()

    for p in workers_p:
        os.kill(p.pid, signal.SIGKILL)
    # loop above doesn't seem to work
    call(['killall', 'hyperopt-mongo-worker'])

    os.kill(mongo_p.pid, signal.SIGTERM)


if __name__ == '__main__':
    logging.basicConfig()
    install_mp_handler()
    main()
