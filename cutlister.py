''' Import Command Line Manager Class to Process Command Line Arguments '''
from app.cli import CLI
''' Import Cutlist Class to Process Cutlist File '''
from app.cutlist import Cutlist
import os, time


''' Initialize Command Line Interface Manager Class '''
cli = CLI()
#print(cli.arguments)

class Album:
  def __init__(self) -> None:
    self.source = cli.get_input()
    self.cutlist_file = cli.get_cutlist()
    self.cutlist = Cutlist(source=self.cutlist_file)
    self.metadata = self.cutlist.metadata
    self.tracklist = self.cutlist.tracklist

  def export_track(self, track_number, start_cue, end_cue, track_title, track_filename, metadata=[], dry_run=False):
    print(f"Preparing to export track { album.cutlist.get_tracknumber(track) }: { album.cutlist.get_start_cue(track).rjust(8) } - { str(album.cutlist.get_end_cue(track)).rjust(8)} - { album.cutlist.get_track_title(track).ljust(album.cutlist.get_longest_title())} -> { track_filename}")
    ''' Build command to export track '''
    # ffmpeg -i source_audio_file.mp3 -ss 0 -t 120 segment_1.mp3
    command = f"ffmpeg -i \"{ self.source }\" -ss { start_cue }"
    if end_cue:
      command += f" -t { end_cue - start_cue }"
    ''' Add track Metadata '''
    command += f" -metadata title=\"{ track_title }\""
    command += f" -metadata track=\"{ track_number }\""
    for meta in metadata:
      command += f" -metadata { meta }=\"{ metadata[meta] }\""
    command += f" \"{ track_filename }\""
    
    

    ''' Execute command '''
    if dry_run:
      print(f"Dry run: skipping command \"{ command }\"")
    else:
      stream = os.popen(command)
      stream.close()
    
    print(f"Finished { track_title }")

    
album = Album()

if cli.verbose:
  print(f"Reading and parsing Cutlist: { album.cutlist_file }")
  print(f"Metadata:")
  for meta in album.metadata:
    print(f"  { meta.capitalize() }: { album.metadata[meta] }")
  print(f"Tracklist: ")
  for track in album.tracklist:
    print(f"  { album.cutlist.get_tracknumber(track) }: { album.cutlist.get_start_cue(track).rjust(8) } - { str(album.cutlist.get_end_cue(track)).rjust(8)} - { album.cutlist.get_track_title(track).ljust(album.cutlist.get_longest_title())} [ { album.cutlist.get_track_filename(track)} ]")


''' Initialize Cutlist Class '''
for track in album.tracklist:
  album.export_track(track_number=track, 
                     start_cue=album.cutlist.get_start_cue_sec(track), 
                     end_cue=album.cutlist.get_end_cue_sec(track), 
                     track_title=album.cutlist.get_track_title(track), 
                     track_filename=cli.get_output(fallback=album.cutlist.get_album_title()) + album.cutlist.get_track_filename(track), 
                     metadata=album.metadata, 
                     dry_run=cli.dry_run)