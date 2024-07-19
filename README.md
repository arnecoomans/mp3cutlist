# Cutlister

Splits a large MP3 file into chunks.

Requires a .cutlist file that holds metadata (@album, @artist)
and for each track a line with 
- tracknumber (optional)
- start-timestamp (format hh:mm:ss)
- end-timestamp (optional, format hh:mm:ss)
- track title

If end-timestamp is not known, it will fetch the start timestamp of the following track

Requires ffmpeg on host system

## Example:
$ python cutlister.py --cutlist example.cutlist --input example_large_file.mp3 --output example_output_directory --verbose --dry-run