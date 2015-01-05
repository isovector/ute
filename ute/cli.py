import socket
from optparse import OptionParser, OptionGroup
from ute import Message
from ute.utils import *

parser = OptionParser("usage: %prog [options] action")
parser.add_option("-i", "--id",    help="the interval to close", type="int", default=-1)
parser.add_option("-t", "--type",  help="the type of the new interval", default="")
parser.add_option("-d", "--desc",  help="the desc of the new interval", default="")
parser.add_option("-e", "--event", help="is the interval an event?",
                    action="store_true", default=False)

(options, args) = parser.parse_args()

print repr(options)

def main():
    if len(args) < 1:
        parser.print_help()
        return

    msg = Message(args[0])
    if args[0] == 'new':
        msg.type  = options.type
        msg.desc  = options.desc

        when = now()
        msg.open = when
        if options.event:
            msg.close = when

    elif args[0] == "close":
        msg.id = options.id

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print msg.toJson()
    s.sendto(msg.toJson(), ("localhost", 6112))
