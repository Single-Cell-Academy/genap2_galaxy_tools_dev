import hashlib
import sys

def main(dependencies):
    #"__picard@2.18.2" "__r-base@3.4.1"
    #626e8c85236e11587c90fe300d7273816bacf20561a301d26c9ed80103b79b1a
    h = hashlib.new('sha256')
    for dependency in dependencies:
        h.update(dependency.encode('utf-8'))
    print("mulled-v1-" + h.hexdigest())


if __name__ == "__main__":
    main(sys.argv[1:])