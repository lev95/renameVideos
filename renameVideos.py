import sys
import os
import re
import datetime
from pymediainfo import MediaInfo


def transcodeDate(date):

    # # Extract time
    # dateRegex = re.compile(r'(\d\d)-(\d\d)-(\d\d)')
    # mo = re.search(dateRegex, date)

    # # Adapt time to timezone
    # dateT = datetime.time(
    #     int(mo.group(1)),
    #     int(mo.group(2)),
    #     int(mo.group(3)))
    # dateT.replace(hour=dateT.hour + 2)
    # print(dateT)

    # Remove characters which do now work on Windows
    date = date.replace(":", "-")
    return date


def renameFile(root, file):
    filepath = os.path.join(root, file)

    # Gather information
    meta = MediaInfo.parse(filepath)
    encoded_date = None
    for track in meta.tracks:
        if track.track_type == 'Video':
            encoded_date = track.encoded_date
        if track.track_type == 'General':
            file_extension = track.file_extension

    # Rename files
    if encoded_date != None:
        encoded_date = transcodeDate(encoded_date)
        newfilepath = os.path.join(root, encoded_date + "." + file_extension)
        if filepath != newfilepath:
            os.rename(filepath, newfilepath)
            print("Renamed from: " + filepath + " to: " + newfilepath)
        else:
            print("File has the same filename: " + filepath)
    else:
        print("File has no encoded date or is not compatible: " + filepath)


# Stop if no input files
if len(sys.argv) == 1:
    print("Script needs one or more paths.")
    sys.exit()

# Walk through files in directory
for i in sys.argv[1:]:
    for root, dirs, files in os.walk(i):
        for file in files:
            renameFile(root, file)
