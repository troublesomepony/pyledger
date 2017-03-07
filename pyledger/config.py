import sys
import argparse
from collections import namedtuple


if len(sys.argv) > 2 and 'test' in sys.argv[2]:
    argstype = namedtuple('Arguments', ['db', 'debug', 'sync'])
    args = argstype(db='sqlite://', debug=False, sync=True)

else:
    parser = argparse.ArgumentParser(description='Run the PyLedger server')
    parser.add_argument('--db', help="SQLAlchemy database address",
                        type=str, default="sqlite://")
    parser.add_argument('--sync', action='store_true')
    parser.add_argument('--debug', action='store_true', default=False)
    args = parser.parse_args()
