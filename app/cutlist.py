''' Cutlist class
    Reads a .cutlist file and processes this into a tracklist
'''
class Cutlist:
  def __init__(self, source) -> None:
    print(f'Processing cutlist file { source }...')
    self.pointer = 0
    self.source = open(source, 'r')
    self.metadata = {}
    self.tracklist = {}

    self.read_cutlist()

  def __del__(self):
    self.source.close()

  def read_cutlist(self):
    for line in self.source.readlines():
      ''' Remove leading and trailing whitespace since readlines always includes the newline character '''
      line = line.strip()
      if line[:1] == '@':
        ''' Fetch Metadata lines 
            Metadata lines start with @ and are followed by a metadata name '''
        self.set_metadata(line)
      elif line[:1] != '#' and len(line) > 1:
        ''' Once comments and empty lines are ignored, proceed '''
        self.set_trackline(line)


  def set_metadata(self, line):
    ''' Store Metadata in metadata dictionary
        Identify metadata name and value
    '''
    name = line[1:line.find(' ')].strip()
    value = line[line.find(' '):].strip()
    value = ''.join(e for e in value if e.isalnum() or e in [' ', '-'])
    self.metadata[name] = value

  def set_trackline(self, line):
    ''' Find delimiter between track number and start cue '''
    delimiter = None
    delimiters = [';', '  ', "\t"]
    for d in delimiters:
      if d in line:
        delimiter = d
        break
    ''' Split tracklist line into snippets '''
    split_line = line.split(delimiter)
    ''' Snippet cleanup '''
    line = []
    for snippet in split_line:
      snippet = snippet.strip()
      ''' Clean up empty snippets '''
      if len(snippet) > 0:
        line.append(snippet)
    ''' Find track number '''
    track_number = None
    if line[0].isdigit():
      track_number = int(line[0])
    ''' Store track data '''
    track = {
      'track_number': track_number,
      'start_cue': None,
      'end_cue': None,
      'track_title': None
    }
    i = 0
    while i < len(line):
      snippet = line[i]
      ''' Find start cue '''
      if snippet.count(':') == 2:
        track['start_cue'] = snippet
        ''' Find track title '''
        if len(line) >= i+1:
          track['track_title'] = line[i+1]
      i += 1
    ''' Store tracklist in tracklist dictionary 
        If track numbers are supplied, use track numbers, else use list length + 1
    '''
    track['source'] = line
    if track_number:
      self.tracklist[track_number] = track
    else:
      self.tracklist[len(self.tracklist)+1] = track

  ''' Helpers '''      
  def get_sec(self, time_str):
    if time_str == None:
      return 0
    """Get seconds from time."""
    h, m, s, = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)
  
  ''' Getters '''
  def get_tracknumber(self, pointer):
    desired_width = len(str(len(self.tracklist)))
    if pointer in self.tracklist:
      if self.tracklist[pointer]['track_number']:
        return f"{ self.tracklist[pointer]['track_number']:0>{desired_width}}"
    return f"{ pointer:0>{desired_width}}"
  
  def get_start_cue(self, pointer):
    if pointer in self.tracklist:
      return self.tracklist[pointer]['start_cue']
    return None
  def get_start_cue_sec(self, pointer):
    if pointer in self.tracklist:
      return self.get_sec(self.tracklist[pointer]['start_cue'])
    return None

  def get_end_cue(self, pointer):
    if pointer in self.tracklist:
      if self.tracklist[pointer]['end_cue']:
        return self.tracklist[pointer]['end_cue']
      elif pointer+1 in self.tracklist:
        return self.tracklist[pointer+1]['start_cue']
    return None
  def get_end_cue_sec(self, pointer):
    if pointer in self.tracklist:
      return self.get_sec(self.get_end_cue(pointer))
    return None
  

  def get_track_title(self, pointer):
    if pointer in self.tracklist:
      return self.tracklist[pointer]['track_title']
    return None
  
  def get_track_filename(self, pointer):
    if pointer in self.tracklist:
      filename = f"{ self.get_tracknumber(pointer) } - { self.get_track_title(pointer) }"
      if self.get_album_artist():
        filename += f" - { self.get_album_artist() }"
      if self.get_album_title():
        filename += f" - { self.get_album_title() }"
      filename += ".mp3"
      return filename
    return None
  
  def get_longest_title(self):
    length = 0
    for track in self.tracklist:
      if len(self.tracklist[track]['track_title']) > length:
        length = len(self.tracklist[track]['track_title'])
    return length
  
  def get_album_artist(self):
    return self.metadata['artist'] if 'artist' in self.metadata else None
  
  def get_album_title(self):
    return self.metadata['album'] if 'album' in self.metadata else None