# How to use it

## Environment variables
Source the variables with `source env.sh`

## Python script
```
./main.py <command>
```
### Commands:
- `create`: creates the cluster and install `mcperf` to the three clients. It requires the path to the yaml configuration file (`-f <filename>`).
- `start memcached`: starts the `memcached` pod. It requires the path to the yaml configuration file (`-f <filename>`).
- `status`: get the current status of the cluster.
- `ssh <node-name>`: open a ssh connection to the specified node. It requires the key `cloud-computing-24` to be stored in `~/.ssh/`.
- `test -s <scheduler-name> -p <parsec-directory>`: executes the scheduler specified. `<scheduler-name>` must be the name of the file in the `schedulers/` directory without the `.py` extension. `<parsec-directory>` must be the path to the directory containing the yaml configuration files of the parsec jobs.
- `destroy`: deletes all the resources allocated for the cluster.
- `time`: executes the `get_time` function to analyze the results.

For more info run `--help`.

### Static scheduler
```
./main.py -s static -p yaml/parsec_static
```
