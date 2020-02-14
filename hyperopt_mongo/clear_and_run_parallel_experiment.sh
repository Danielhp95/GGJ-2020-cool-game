#!/bin/bash

# The number of available CPUS in a viking job will be stored in
# $SLURM_CPUS_ON_NODE


function clear_mongodb_files() {
rm -rf sizeStorer.wt WiredTiger WiredTigerLAS.wt WiredTiger.lock WiredTiger.turtle WiredTiger.wt storage.bson _mdb_catalog.wt local logfile.txt journal admin config diagnostic.data foo_db mongod.lock
}


###########
## START ##
###########

# Start Mongo
mongod --dbpath . --port 1234 --directoryperdb --journal &
MONGODB_PID=$!

##################################
# Launch top-level python script #
##################################
python cool_game_regym_hyperopt.py &
HIGH_LEVEL_PYTHON_PID=$!

##################
# Launch workers #
##################
WORKER_IDS=()
NUMBER_WORKERS=1  
for i in `seq 0 $NUMBER_WORKERS`; do
    # Launch external process (that's what `&`) does
    hyperopt-mongo-worker --mongo=localhost:1234/foo_db --poll-interval=0.1 &
    PID=$!
    echo "Spawning process: " $PID
    # Append process id
    WORKER_IDS+=($PID) 
done

# Wait for optimization to finish
wait $HIGH_LEVEL_PYTHON_PID
echo "Optimization finished, proceeding to shutdown workers"

#############################
# Kill all workers and MONGO#
#############################
for pid in "${WORKER_IDS[@]}"; do
    echo "Killing worker process: " $pid
    kill -9 $pid
done

kill -2 $MONGODB_PID
