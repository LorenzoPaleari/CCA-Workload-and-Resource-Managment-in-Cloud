import time
import psutil
from datetime import datetime
import argparse

def run(filename):
    file = open(filename, 'w')
    var = []
    for i in range(180):
        var.append(str(datetime.now().timestamp()) + " " + str(psutil.cpu_percent(interval = None, percpu = True))+ "\n")
        time.sleep(1)
    file.writelines(var)
    file.close()

def main():
    parser = argparse.ArgumentParser(prog='main', description='Command line interface for cluster operations')
    subparsers = parser.add_subparsers(dest='command')

    create_parser = subparsers.add_parser('file', help='create cluster')
    create_parser.add_argument('-f', '--file', type=str, required=True, help='YAML file for cluster configuration')

    args = parser.parse_args()
    service_not_recognized = 'Service not recognized.'
    if args.command == 'file':
        run(args.file)


if __name__ == '__main__':
    main()
