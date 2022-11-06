# Introduction
This code fixes the GPS rollover problem for log files produced by the Sony GPS-CS1 tracker

The [Sony GPS-CS1](https://www.sony.com/electronics/support/product/gps-cs1) is a GPS tracker designed for photographers, who can use the logs to add geocoordinates to the EXIF data of their photos. When you turn it on it starts logging GPS coordinates to the internal storage.

Unfortunately this device suffers from the [GPS week rollover](https://en.wikipedia.org/wiki/GPS_week_number_rollover) bug, which causes the recorded dates to be off by exactly 1024 weeks, or 7168 days, after a certain date.

I don't use the device that much, so I don't know exactly when it started, but somewhere in the second half of 2022. Tracks that I recorded on the 1st of November 2022, showed up as being recorded on the 18th of March 2003.

By fixing the files the device produces, I can keep using it forever!


# How to use it

```
usage: fix_rollover.py [-h] [--folder FOLDER] [--file FILE]

options:
  -h, --help       show this help message and exit
  --folder FOLDER  Folder that contains log files you want to update
  --file FILE      Log file you want to update
```

You can either have it process a single file, or an entire folder.

Single file:
```
python fix_rollover.py --file WG20030318121127.log
```

Entire folder:
```
python fix_rollover.py --folder ~/tracks
```

It will write an updated file to the same folder as the original file, with an updated name to reflecting the correct date. The original file(s) will remain untouched.

Some assumptions:
 * Files follow the pattern as produced by the GPS-CS1, which is `WGYYYYMMDDhhmmss.log` (i.e. `WG20030318121127.log`)
 * When scanning an entire folder, any files not ending in `.log` will be skipped, as well as files that start with anything less than `WG2021`
 * If you try to run this on a file that doesn't match the pattern, it will likely crash

# More information
* Explanation of the GPS sentences: http://aprs.gids.nl/nmea/
