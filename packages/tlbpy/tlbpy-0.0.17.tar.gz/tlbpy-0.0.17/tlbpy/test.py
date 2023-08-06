import sys
import argparse
import importlib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", "-n", help="name's test")
    parser.add_argument("--args", help="potential useful arg to add", nargs='+')
    args = parser.parse_args()
    test_name = args.name
    test = importlib.import_module('rl_algos.tests.'+str(test_name)).test
    test(args.args)
    
if __name__ == "__main__":
    main()