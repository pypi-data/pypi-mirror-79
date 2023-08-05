def usage():
  print('usage : python -m batch_resize path-of-target')

def main(argv):
  if len(argv) < 2:
    return usage()
  import os, sys, pathlib
  sys.path.append(str(pathlib.Path(__file__).parent.absolute()) + os.path.sep + 'libs')
  from batch import Context
  Context(*argv[1:]).run()

if __name__ == '__main__':
  import sys
  main(sys.argv)