from app import app

import sys



def main(argv):

    port = 5000
    debug = True
    if len(argv) > 1:
        port = argv[0]
        debug = argv[1]

    app.run(port=port, debug=debug)



if __name__ == '__main__':
    main(sys.argv[1:])
