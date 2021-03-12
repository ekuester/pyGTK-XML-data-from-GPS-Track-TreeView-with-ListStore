# pyGTK-XML-data-from-GPS-Track-TreeView-with-ListStore
Read XML data from a GPX file und display the GPS trackpoints in a meaningful table.</br>
Calculates the total distance of the track by the Haversine formula for the great circle.</br>
(python / Linux / Gnome / pyGTK / XML data / GPS track)

### Discussion
This program is written in python with use of pyGtk for the Gnome GTK3 environment of Linux.

In those days when I switched from macOS to Fedora Linux (for what reasons ever), I had to change my programming language. For "simplicity" I choose first C++ and to my pleasure found its "way to think" very similar to Swift and Objective-C. Then I "meet" python and decided to switch the evaluated design from gtkmm to pyGtk which BTW is no problem.

Since Python is an interpretative language you can simply start the program in command line.

```
# make it executable once
chmod +x ./pyXMLGPX-parser.py
./pyXMLGPX-parser.py
```
In the moment exists no localization or package preparation (on the TO-DO-list).

I wrote this program to become familiar with the GTK-API and to get a feeling how to display different widgets on the screen. For reading of XML files the python module <b>xml.etree.ElementTree</b> is used, which integrates itself trouble-free. Take the whole as example for handling treeviews on liststore base and reading of xml files under python GTK+.

### Background
During trips by foot, bicycle or car I record the covered distance on my Apple iPhone or iPad with the excellent App <b>myTracks</b> by Dirk Stichling. Find more informations at [1] or [2].

The obtained GPX files are extracted from the backup files made by iTunes under macOS or Windows [3] and then transferred to my personal computer for dealing with further. To read in the file correctly into the program, you can do some changes:

```
# delete the namespace prefix inside the data file and make a backup
sed -e 's/mytracks://g' -i.backup gpxtrack-0.gpx
# delete the attributes of the gpx node (complex regular expression code for sed)
sed -e ':a;N;$!ba;s|\(.*<gpx\).*\(<trk>.*\)|\1>\2|' -i gpxtrack-0.gpx
# the prefix `:a;N;$!ba;` is for adding of eventually existing linefeeds to the pattern space
```
With the newest version of the programm this is NOT necessary anymore ...

### Usage:
The program is mostly self explaining. On the toolbar at top of the window you will find buttons for opening a xml file, leaving the program and getting info about. After opening a xml file the contained track points are displayed in a table together with the calculated speed between two points. The total covered distance is shown at the bottom of the window. Erasing and/or inserting additional points should not be difficult to implant just as storing of the modified file (but I leave that as your own task).

Simplified example of a xml file with GPS track data:

```
<?xml version="1.0" encoding="UTF-8"?>
<gpx>
  <trk>
    <name>2012-11-14 09:57:20</name>
    <extensions>
      <area showArea="no" areaDistance="0.000000"/>
      <directionArrows showDirectionArrows="yes"/>
      <sync syncPhotosOniPhone="no"/>
      <timezone offset="60"/>
    </extensions>
    <trkseg>
      <trkpt lat="51.30887235519598" lon="6.595192467799964">
        <ele>29.93182373046875</ele>
        <time>2012-11-14T09:17:41Z</time>
        <extensions>
          <speed>15.88389816914975</speed>
          <length>0.008501878652107393</length>
        </extensions>
      </trkpt>
      <trkpt lat="51.30883484617929" lon="6.59517176449913">
        <ele>30.09716796875</ele>
        <time>2012-11-14T09:17:42Z</time>
        <extensions>
          <speed>15.86182185803758</speed>
          <length>0.00441219393587493</length>
        </extensions>
      </trkpt>
   </trkseg>
  </trk>
</gpx>
```
### Acknowledgements:
- Special thanks go to the people in the developer community at StackOverflow. Without their help and answered questions at <https://stackoverflow.com/> and affiliate sites this work would not be possible.

### Literature
[1] <https://www.mytracks4mac.info/index.php/en/> (english)</br>
[2] <https://www.mytracks4mac.info/index.php/de/> (german)</br>
[3] <https://github.com/ekuester/pyGTK-List-ManifestDB-From-iOSBackup.git>

### Disclaimer
Use the program for what purpose you like, but hold in mind, that I will not be responsible for any harm it will cause to your hard- or software. It was your decision to use this piece of software.

