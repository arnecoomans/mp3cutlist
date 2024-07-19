import argparse
import glob, os

class CLI:
  ''' Command Line Interface Manager Class '''
  def __init__(self):
    ''' Initialize Command Line Interface Manager Class '''
    self.parser = argparse.ArgumentParser()
    self.parser.add_argument('-c', '--cutlist', help='Cutlist File')
    self.parser.add_argument('-i', '--input', help='Source File')
    self.parser.add_argument('-o', '--output', help='Output Directory')
    self.parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Mode')
    self.parser.add_argument('--dry-run', action='store_true', help='Dry Run Mode')
    self.args = self.parser.parse_args()
    self.verbose = self.args.verbose
    self.dry_run = self.args.dry_run
    self.cutlist = None
    self.input = None
    self.output = None

  def get_cutlist(self):
    if self.cutlist:
      return self.cutlist
    ''' Get Cutlist File '''
    if self.args.cutlist:
      if self.args.verbose:
          print(f'[Info] Using cutlist file "{ self.args.cutlist }" based on --cutlist argument.')
      self.cutlist = self.args.cutlist
      return self.args.cutlist
    else:
      files = glob.glob('*.cutlist')
      if len(files) > 0:
        file = max(files, key=os.path.getmtime)
        if self.args.verbose:
          print(f'[Info] Using cutlist file "{ file }" based on last modified date.')
        self.cutlist = file
        return file
      print('[Error!] No cutlist file found.')
      print('         Please specify a cutlist file using the -i option.')
      exit(1)
  
  def get_input(self):
    if self.input:
      return self.input
    ''' Get Source File '''
    if self.args.input:
      if self.args.verbose:
        print(f'[Info] Using source file "{ self.args.input }" based on --input argument.')
      self.input = self.args.input
      return self.args.input
    else:
      files = glob.glob('*.mp3')
      if len(files) > 0:
        file = max(files, key=os.path.getmtime)
        if self.args.verbose:
          print(f'[Info] Using source file "{ file }" based on last modified date.')
        self.input = file
        return file
      print('[Error!] No source file found.')
      print('         Please specify a source file using the -i option.')
      exit(1)

  def get_output(self, fallback=None):
    if self.output:
      return self.output
    ''' Get Output Directory '''
    output = None
    if self.args.output:
      if self.args.verbose:
        print(f'[Info] Using output directory "{ self.args.output }" based on --output argument.')
      output = self.args.output
    elif fallback:
      if self.args.verbose:
        print(f'[Info] Using fallback output directory "{ fallback }".')
      output = fallback
    else:
      if self.args.verbose:
        print(f'[Info] Using current directory as output directory.')
      output = os.getcwd()  
    ''' Verify Output Directory exists '''
    print(output)
    if not os.path.exists(output):
      if self.args.verbose:
        print(f'[Info] Creating output directory "{ output }".')
      os.makedirs(output)
    if len(output) > 0 and output[-1] != '/':
      output += '/'
    self.output = output
    return output