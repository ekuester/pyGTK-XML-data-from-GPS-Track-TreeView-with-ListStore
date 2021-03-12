#!/usr/bin/env python3
# see https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
#  parse xml content of a GPX file recorded with the
#  App mytracks by Dirk Stichling for Apple's iPhone or iPad
#  command line version v1.0.0
#  File: pyXMLGPX-parser.py
#  using python module 
#
# Copyright © 2016-2021 Erich Küster. All rights reserved.

import os, sys
from time import mktime, strptime

import gettext
_ = gettext.gettext

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio, GLib, GObject

from inspect import currentframe
from math import asin, cos, sin, sqrt

import xml.etree.ElementTree as ET

svg = """
<svg id="svg154" width="256" height="256" version="1.1" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg" xmlns:cc="http://creativecommons.org/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:xlink="http://www.w3.org/1999/xlink">
 <defs id="defs142">
  <linearGradient id="linearGradient868" x1="98" x2="98" y1="98" y2="195.5" gradientTransform="matrix(1.2308 0 0 1.2308 8.8767 8.7226)" gradientUnits="userSpaceOnUse">
   <stop id="stop864" stop-color="#ff0035" offset="0"/>
   <stop id="stop866" stop-color="#fd5" offset="1"/>
  </linearGradient>
  <linearGradient id="linearGradient862" x1="138.69" x2="221.78" y1="167.91" y2="167.91" gradientUnits="userSpaceOnUse" xlink:href="#linearGradient868"/>
  <linearGradient id="linearGradient887" x1="93.205" x2="128.06" y1="140.09" y2="98.375" gradientTransform="translate(-3.0196)" gradientUnits="userSpaceOnUse" xlink:href="#linearGradient868"/>
  <linearGradient id="linearGradient893" x1="105.77" x2="103.04" y1="35.507" y2="16.058" gradientTransform="matrix(.29209 0 0 3.4236 12.98 1.357)" gradientUnits="userSpaceOnUse" xlink:href="#linearGradient868"/>
  <linearGradient id="linearGradient895" x1="149.64" x2="201.03" y1="47.501" y2="108.7" gradientTransform="matrix(.82996 0 0 1.2049 12.98 1.357)" gradientUnits="userSpaceOnUse">
   <stop id="stop121" stop-color="#ffb380" offset="0"/>
   <stop id="stop123" stop-color="#ff2a2a" offset="1"/>
  </linearGradient>
  <filter id="filter854" x="-.072" y="-.072" width="1.144" height="1.144" color-interpolation-filters="sRGB">
   <feGaussianBlur id="feGaussianBlur856" stdDeviation="3.5141602"/>
  </filter>
 </defs>
 <rect id="rect1206" x="8.1453" y="8.1453" width="240" height="240" rx="32" ry="32" fill="#fff" fill-opacity=".93891" stroke="#e9e5e5" stroke-width="3.7795"/>
 <path id="path146" d="m45.862 138.9h-4.5633v-60.979h4.5633zm-2.3466-75.927c-1.9244 0-3.5158-1.5265-3.5158-3.4509 0-1.9812 1.5833-3.5158 3.5158-3.5158 1.9812 0 3.5564 1.5265 3.5564 3.5158 0 1.9244-1.5752 3.4509-3.5564 3.4509z" fill="url(#linearGradient893)" fill-rule="evenodd"/>
 <path id="path148" d="m90.185 140.09c-22.313 0-36.409-16.248-36.409-42.076 0-25.699 14.161-42.011 36.409-42.011s36.401 16.313 36.401 42.011c0 25.829-14.096 42.076-36.401 42.076zm0-79.89c-19.422 0-31.821 14.664-31.821 37.813 0 23.166 12.456 37.887 31.821 37.887 19.422 0 31.821-14.721 31.821-37.887 0-23.157-12.399-37.813-31.821-37.813z" fill="url(#linearGradient887)" fill-rule="evenodd"/>
 <path id="path150" d="m159.08 140.09c-16.751 0-28.76-9.4595-29.442-22.987h4.474c0.68206 11.092 11.1 18.854 25.309 18.854 13.868 0 23.547-7.8761 23.547-18.513 0-8.5582-5.7731-13.479-19.471-16.93l-9.6787-2.3791c-15.111-3.8569-21.972-9.971-21.972-20.21 0-12.74 11.895-21.915 26.787-21.915 15.395 0 26.892 9.0616 27.404 21.063h-4.474c-0.62522-9.7924-10.19-16.93-23.044-16.93-12.293 0-22.086 7.3646-22.086 17.668 0 8.1603 6.0005 12.854 19.13 16.134l9.1184 2.3222c15.793 3.9056 22.873 9.971 22.873 20.835 0 13.527-11.376 22.987-28.476 22.987z" fill="url(#linearGradient895)" fill-rule="evenodd"/>
 <text id="text1188" x="-110.63005" y="153.78233" fill="#000000" font-family="sans-serif" font-size="40px" style="line-height:1.25" xml:space="preserve"><tspan id="tspan1186" x="-110.63005" y="153.78233"/></text>
 <text id="text1192" x="87.968163" y="180.4267" fill="url(#linearGradient862)" font-family="sans-serif" font-size="42.667px" style="line-height:1.25;mix-blend-mode:normal" xml:space="preserve"><tspan id="tspan1190" x="87.968163" y="180.4267" fill="url(#linearGradient862)" font-family="'Noto Sans'" font-size="42.667px">Backup</tspan></text>
 <path id="path849" transform="matrix(2 0 0 2 .14531 .14531)" d="m117.14 6.8613c1.8003 2.5889 2.8613 5.7328 2.8613 9.1387v88c0 8.864-7.136 16-16 16h-88c-3.4059 0-6.5498-1.061-9.1387-2.8613 2.8851 4.1488 7.6806 6.8613 13.139 6.8613h88c8.864 0 16-7.136 16-16v-88c0-5.4581-2.7126-10.254-6.8613-13.139z" filter="url(#filter854)" opacity=".36"/>
</svg>"""

##############################
# use f-strings with gettext #
##############################
def  f(s):
    frame = currentframe().f_back
    return eval(f"f'{s}'", frame.f_locals, frame.f_globals)

###########
# classes #
###########

class XMLGPXParserWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gtk+: XML Application - XML TableView from GPX-Tracker")
        self.set_border_width(8)
        self.set_default_size(1024, 768);
        loader = GdkPixbuf.PixbufLoader()
        loader.write(svg.encode())
        loader.close()
        pixbuf = loader.get_pixbuf()
        self.set_icon(pixbuf)
        # vertical box to hold the widgets
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        # a toolbar created in the method create_toolbar (see below)
        toolbar = self.create_toolbar()
        # with extra horizontal space
        toolbar.set_hexpand(True)
        # show the toolbar
        toolbar.show()
        # add the toolbar to the vertical box
        self.vbox.pack_start(toolbar, False, True, 0)
        self.label = Gtk.Label()
        self.label.set_markup("<span face=\"mono\" weight=\"bold\">View XML data from GPS Track</span>")
        self.label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.label_box.pack_start(self.label, True, True, 0)
        self.vbox.pack_start(self.label_box, True, True, 0)

        # some stuff to remember
        self.first_run = True
        self.last_path = str()

        # create scrolled_window for treeview under the combobox
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_size_request(-1, 456)
        self.scrolled_window.set_border_width(0)
        # there is always the scrollbar (otherwise: ALWAYS NEVER)
        self.scrolled_window.set_policy(\
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        # model creation for the treeview
        treemodel = Gtk.ListStore( int, 'gdouble', 'gdouble', 'gdouble', 'glong', 'gdouble', 'gdouble')
        # create TreeView
        self.treeview = Gtk.TreeView(model=treemodel)
        # treeview column headers
        treeview_columns =\
            ['Id', 'latitude', 'longitude', 'elevation', 'time [sec]', 'distance', 'speed [km/h]']
        for num, name in enumerate(treeview_columns):
            rendererText = Gtk.CellRendererText()
            # center align all columns of row (0.0 left, 1.0 right)
            rendererText.props.xalign = 0.5
            column = Gtk.TreeViewColumn(name, rendererText, text=num)
            # make all the column reorderable and resizable
            column.set_reorderable(True)
            column.set_resizable(True)
            # center the column titles in first row
            column.set_alignment(0.5)
            self.treeview.append_column(column)
        # Connect signal handler
        self.treeview.connect("row_activated", self.on_row_activated)

        self.status_frame = Gtk.Frame()
        self.status_bar = Gtk.Statusbar()
        self.status_frame.add(self.status_bar)
        self.vbox.pack_end(self.status_frame, False, True, 0)
        self.context_id = self.status_bar.push(0, _("Choose a file, click Open"))
        self.add(self.vbox)
        self.show_all()

    # method to create the toolbar
    def create_toolbar(self):
        # a toolbar
        toolbar = Gtk.Toolbar()
        # which is the primary toolbar of the application
        toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        # toolbar.set_toolbar_style(Gtk.TOOLBAR_BOTH);
        # create a button for the "open" action, with a stock image
        openIcon = Gtk.Image.new_from_icon_name("document-open", Gtk.IconSize.LARGE_TOOLBAR)
        open_button = Gtk.ToolButton.new(openIcon, _("Open"))
        open_button.set_tooltip_text(_("Open GPS recording"))
        # label is shown
        open_button.set_is_important(True)
        toolbar.insert(open_button, 1)
        open_button.show()
        # set the name of the action associated with the button.
        open_button.connect("clicked", self.on_open_clicked)
        # create a button for the "quit" action, with a stock image
        quitIcon = Gtk.Image.new_from_icon_name("application-exit", Gtk.IconSize.LARGE_TOOLBAR)
        quit_button = Gtk.ToolButton.new(quitIcon, _("Quit"))
        quit_button.set_tooltip_text(_("Exit program"))
        # label is shown
        quit_button.set_is_important(True)
        toolbar.insert(quit_button, 2)
        quit_button.show()
        # set the name of the action associated with the button.
        quit_button.connect("clicked", self.on_quit_clicked)
        # create horizontal space
        toolitem_space = Gtk.SeparatorToolItem()
        toolitem_space.set_expand(True)
        toolbar.insert(toolitem_space, 3)
        # create a button for the "about" action, with a stock image
        aboutIcon = Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.LARGE_TOOLBAR)
        about_button = Gtk.ToolButton.new(aboutIcon, _("About"))
        about_button.set_tooltip_text(_("About program"))
        # label is shown
        about_button.set_is_important(True)
        toolbar.insert(about_button, 4)
        about_button.show()
        # set the name of the action associated with the button.
        about_button.connect("clicked", self.on_about_clicked)
        # return the complete toolbar
        return toolbar

    def add_filters(self, dialog):
        filter_gpx = Gtk.FileFilter()
        filter_gpx.set_name(_("GPX track files"))
        filter_gpx.add_pattern("*.gpx")
        dialog.add_filter(filter_gpx)

        filter_xml = Gtk.FileFilter()
        filter_xml.set_name(_("XML files"))
        filter_xml.add_mime_type("text/xml")
        dialog.add_filter(filter_xml)

        filter_text = Gtk.FileFilter()
        filter_text.set_name(_("Text files"))
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name(_("Any files"))
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def choose_gpx_file(self):
        dialog = Gtk.FileChooserDialog(
            title=_("Select GPS track file"), parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK)
        self.add_filters(dialog)
        dialog.set_current_folder(self.last_path)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            filename = None
        dialog.destroy()
        return filename

    def on_open_clicked(self, open_button):
        if (self.first_run is False):
            self.context_id = self.status_bar.push(self.context_id,\
                _("Go on to open a new track file"))
        gpx_url = self.choose_gpx_file()
        if (gpx_url is None):
            self.context_id = self.status_bar.push(self.context_id,\
                _("No track file chosen, try again"))
            return
        # remenber chosen path
        self.last_path = os.path.dirname(gpx_url)
        try:
            tree = ET.parse(gpx_url)
        except AttributeError as err:
            self.context_id = self.status_bar.push(self.context_id,\
                _('An error occurred while opening, good luck!'))
            return
        self.remove(self.vbox)
        if (self.first_run):
            # prepare scrolled window
            self.scrolled_window.add(self.treeview)
            self.scrolled_window.show()
            # add new widgets and reorder
            self.vbox.remove(self.label_box)
            self.vbox.pack_start(self.scrolled_window, False, True, 0)
            self.vbox.pack_start(self.label_box, True, True, 0)
            self.bottom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            self.bottom_box.set_border_width(0)
            self.total_label = Gtk.Label()
            self.total_label.set_margin_start(64)
            self.total_label.set_markup(_("<b>Total distance:</b>"))
            self.total_label.set_margin_end(24)
            self.total_entry = Gtk.Entry(text="0.0")
            self.bottom_box.pack_start(self.total_label, False, True, 0)
            self.bottom_box.pack_start(self.total_entry, False, True, 0)
            self.vbox.pack_start(self.bottom_box, False, True, 0)
            self.first_run = False
        gpx = tree.getroot()
        tag = gpx.tag
        # namespace in {}
        try:
            index = tag.index('}')
        except ValueError as err:
            index = -1
        index += 1
        ns = tag[0:index]
        # find all trackpoints
        points = 0
        # distance by great circle haversine
        total_distance = 0.0
        # distance given by mytracks app
        tracks_distance = 0.0
        trackpoints = list()
        for trk in gpx.findall(f'{ns}trk'):
            for trkseg in trk.findall(f'{ns}trkseg'):
                for trkpt in trkseg.iter(f'{ns}trkpt'):
                    trackpoint = dict()
                    lat = trkpt.get('lat')
                    lon = trkpt.get('lon')
                    ele_item = trkpt.find(f'{ns}ele')
                    ele = ele_item.text
                    trackpoint['latitude'] = float(lat)
                    trackpoint['longitude'] = float(lon)
                    trackpoint['elevation'] = float(ele)
                    time_item = trkpt.find(f'{ns}time')
                    date_string = time_item.text
                    date_time = strptime(date_string,'%Y-%m-%dT%H:%M:%SZ')
                    trackpoint['seconds'] = mktime(date_time)
                    extensions = trkpt.find(f'{ns}extensions')
                    if extensions:
                        for ext in extensions:
                            try:
                                i = ext.tag.index('}')
                            except ValueError as err:
                                i = -1
                            i += 1
                            key = ext.tag[i:]
                            trackpoint[key] = ext.text
                    points += 1
                    trackpoint['Id'] = points
                    if points == 1:
                        trackpoint['distance'] = 0.0
                        trackpoint['velocity'] = 0.0
                    else:
                        previous = trackpoints[-1]
                        self.distanceByHaversine(previous, trackpoint)
                        elapsed_time = trackpoint['seconds'] - previous['seconds']
                        trackpoint['velocity'] = trackpoint['distance'] / elapsed_time * 3600.0
                        total_distance += trackpoint['distance']
                        if extensions:
                            tracks_distance += float(trackpoint['length'])
                    trackpoints.append(trackpoint)
        model = self.treeview.get_model()
        # delete data of an earlier run
        if (len(model) > 0):
            # make place for new table rows
            model.clear()
        names = ['Id', 'latitude', 'longitude', 'elevation', 'seconds', 'distance', 'velocity']
        for trackpoint in trackpoints:
            row_iter = model.append()
            for column, name in enumerate(names):
                model.set_value(row_iter, column, trackpoint[name])
        self.total_entry.set_text(f'{total_distance: 5.4f} km')
        print(f'mytracks distance = {tracks_distance: 5.4f}')
        self.context_id = self.status_bar.push(self.context_id,\
            f(_('Track contains {points} trackpoints')))
        self.label.set_markup(f'<span face=\"mono\" weight=\"bold\">View XML data from {gpx_url}</span>')
        self.add(self.vbox)
        self.show_all()

    def on_quit_clicked(self, quit_button):
        self.destroy()

    def on_about_clicked(self, widget):
        about = Gtk.AboutDialog(transient_for=self)
        about.set_logo(GdkPixbuf.Pixbuf.new_from_file("about.xpm"))
        about.set_program_name("pyGtk: XML Application - XML Data from GPX Track")
        about.set_size_request(480, -1)
        about.set_version("Version 1.2.8")
        about.set_authors(_("Erich Küster, Krefeld/Germany\n"))
        about.set_copyright("Copyright © 2018-2021 Erich Küster. All rights reserved.")
        with open("COMMENTS","r") as f:
            comments = f.read()
        about.set_comments(comments)
        with open("LICENSE","r") as f:
            license = f.read()
        about.set_license(license)
        about.set_website("http://www.python-gtk-3-tutorial.readthedocs.io")
        about.set_website_label("https://python-gtk-3-tutorial.readthedocs.io/en/latest/")
        about.set_authors([_("Erich Küster, Krefeld/Germany")])
        response = about.run()
        if response != Gtk.ResponseType.DELETE_EVENT:
            print(_("Unknown button was clicked"))
        about.destroy()

    def on_row_activated(self, treeview, path, column):
        return

    # Formula given by http://en.wikipedia.org/wiki/Great-circle_distance
    # same given by https://movable-type.co.uk/scripts/gis-faq-5.1.html
    def distanceByHaversine(self, previous, trackpoint):
        # dRad is pi()/180 for conversion in radians
        dRad = 1.74532925199433E-02
        # mean earth radius in km
        r = 6371.0
        lat1 = previous['latitude'] * dRad
        lat2 = trackpoint['latitude'] * dRad
        lon1 = previous['longitude'] * dRad
        lon2 = trackpoint['longitude'] * dRad
        dlat = lat1 - lat2
        dlon = lon1 -lon2
        a = sin(dlat / 2) * sin(dlat / 2) + \
            cos(lat1) * cos(lat2) * sin(dlon / 2) * sin(dlon / 2)
        trackpoint['distance'] = (2.0 * asin(min(1, sqrt(a))) * r)

display = XMLGPXParserWindow()
display.connect("destroy", Gtk.main_quit)
display.show_all()
Gtk.main()

