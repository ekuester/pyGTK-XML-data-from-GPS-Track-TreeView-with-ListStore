#!/usr/bin/env python3

import os, sys
import datetime

import gettext
_ = gettext.gettext

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio, GLib, GObject
from inspect import currentframe
from math import asin, cos, sin, sqrt

import xml.etree.ElementTree as ET

svg = """
<svg id="svg15" width="256" height="256" enable-background="new 0 0 32 32" version="1.1" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg" xmlns:cc="http://creativecommons.org/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
 <metadata id="metadata19">
  <rdf:RDF>
   <cc:Work rdf:about="">
    <dc:format>image/svg+xml</dc:format>
    <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage"/>
    <dc:title/>
   </cc:Work>
  </rdf:RDF>
 </metadata>
 <defs id="defs7">
  <linearGradient id="grad" x1="2.6788" x2="2.6788" y1=".46663" y2="29.398" gradientTransform="matrix(6.5328 0 0 7.5006 16 16)" gradientUnits="userSpaceOnUse">
   <stop id="stop2" stop-color="#eee" offset="0"/>
   <stop id="stop4" stop-color="#bbb" offset="1"/>
  </linearGradient>
 </defs>
 <rect id="rect9" x="37" y="23" width="182" height="210" ry="28" fill="url(#grad)" stroke="#000" stroke-width="7"/>
 <rect id="rect11" x="16" y="65" width="224" height="126" ry="28"/>
 <text id="text13" x="121" y="163" fill="#ffffff" font-family="Arial, sans-serif" font-size="94.5px" font-weight="bold" stroke-width="7" text-anchor="middle">GPX</text>
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
class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        super(Window, self).__init__(title=_("Gtk+: XML Application - XML TableView from GPX-Tracker"),\
    application=app)
        self.set_border_width(8)
        self.set_default_size(1024, 768);
        loader = GdkPixbuf.PixbufLoader()
        loader.write(svg.encode())
        loader.close()
        pixbuf = loader.get_pixbuf()
        self.set_icon(pixbuf)
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
        self.label.set_markup(_("<span face=\"mono\" weight=\"bold\">View XML data from GPS Track</span>"))
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
        treemodel = Gtk.ListStore( int, 'gdouble', 'gdouble', 'gdouble', str, 'gdouble', 'gdouble')
        # create TreeView
        self.treeview = Gtk.TreeView(model=treemodel)
        # treeview column headers
        treeview_columns =\
    ['Id', _('latitude'), _('longitude'), _('elevation'), _('UTC'), _('distance [km]'), _('velocity [km/h]')]
        formats = ['{0:d} ', '{0:.4f}  ', '{0:.4f}  ', '{0:.1f}  ', '{0:>s}  ', '{0:0.3f}  ', '{0:0.3f}   ']
        for col_num, name in enumerate(treeview_columns):
            # align text in column cells of row (0.0 left, 0.5 center, 1.0 right)
            rendererText = Gtk.CellRendererText(xalign=1.0, editable=False)
            column = Gtk.TreeViewColumn(name, rendererText, text=col_num)
            # set formatting for column
            col_format = formats[col_num]
            column.set_cell_data_func(rendererText, self.celldatafunction, func_data=[col_num, col_format])
            # center the column titles in first row
            column.set_alignment(0.5)
            # make all the column reorderable, resizable and sortable
            column.set_sort_column_id(col_num)
            column.set_reorderable(True)
            column.set_resizable(True)
            self.treeview.append_column(column)
        # Connect signal handler
        self.treeview.connect("row_activated", self.on_row_activated)
        # status frame for messages
        self.status_frame = Gtk.Frame()
        self.status_bar = Gtk.Statusbar()
        self.status_frame.add(self.status_bar)
        self.vbox.pack_end(self.status_frame, False, True, 0)
        self.context_id = self.status_bar.push(0, _("Choose a file, click Open"))
        self.add(self.vbox)

    # method for column cell formatting
    def celldatafunction(self, column, cell, model, iter, func_data):
        # we don't use column, but it is provided by the function
        col_num, col_format = func_data
        cell.set_property('text', col_format.format(model.get(iter, col_num)[0]))
        path = model.get_path(iter)
        row = path[0]
        colors = ['lightgoldenrodyellow', 'white']
        cell.set_property('cell-background', colors[row % 2])

    # method to create the toolbar
    def create_toolbar(self):
        # a toolbar
        toolbar = Gtk.Toolbar()
        # which is the primary toolbar of the application
        toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        # toolbar.set_toolbar_style(Gtk.TOOLBAR_BOTH);
        # create a button for "open"
        openIcon = Gtk.Image.new_from_icon_name("document-open", Gtk.IconSize.LARGE_TOOLBAR)
        open_button = Gtk.ToolButton.new(openIcon, _("Open"))
        open_button.set_tooltip_text(_("Open GPS recording"))
        # label is shown
        open_button.set_is_important(True)
        toolbar.insert(open_button, 1)
        open_button.show()
        # set the name of the action associated with the button
        open_button.set_action_name("app.open")
        # create a button "quit" action
        quitIcon = Gtk.Image.new_from_icon_name("application-exit", Gtk.IconSize.LARGE_TOOLBAR)
        quit_button = Gtk.ToolButton.new(quitIcon, _("Quit"))
        quit_button.set_tooltip_text(_("Exit program"))
        # label is shown
        quit_button.set_is_important(True)
        toolbar.insert(quit_button, 2)
        quit_button.show()
        # set the name of the action associated with the button
        quit_button.set_action_name("app.quit")
        # create horizontal space
        toolitem_space = Gtk.SeparatorToolItem()
        toolitem_space.set_expand(True)
        toolbar.insert(toolitem_space, 3)
        # create a button for "about"
        aboutIcon = Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.LARGE_TOOLBAR)
        about_button = Gtk.ToolButton.new(aboutIcon, _("About"))
        about_button.set_tooltip_text(_("About program"))
        # label is shown
        about_button.set_is_important(True)
        toolbar.insert(about_button, 4)
        about_button.show()
        # set the name of the action associated with the button
        about_button.set_action_name("app.about")
        # return the complete toolbar
        return toolbar

    def on_row_activated(self, treeview, path, column):
        print('treeview row activated')
        return

class Application(Gtk.Application):
    def __init__(self):
        super(Application, self).__init__()

    def do_activate(self):
        self.window = Window(self)
        self.window.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("open", None)
        action.connect("activate", self.on_open)
        self.add_action(action)
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

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
            title=_("Select GPS track file"), parent=self.window, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK)
        self.add_filters(dialog)
        dialog.set_current_folder(self.window.last_path)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            filename = None
        dialog.destroy()
        return filename

    def on_open(self, action, parameter):
        if (self.window.first_run is False):
            self.window.context_id = self.window.status_bar.push(self.window.context_id,\
                _("Go on to open a new track file"))
        gpx_url = self.choose_gpx_file()
        if (gpx_url is None):
            self.window.context_id = self.window.status_bar.push(self.window.context_id,\
                _("No track file chosen, try again"))
            return
        # remenber chosen path
        self.window.last_path = os.path.dirname(gpx_url)
        try:
            tree = ET.parse(gpx_url)
        except AttributeError as err:
            self.window.context_id = self.window.status_bar.push(self.window.context_id,\
                _('An error occurred while xml parsing, good luck!'))
            return
        print(f(_('file chosen: {gpx_url}')))
        self.window.remove(self.window.vbox)
        if (self.window.first_run):
            # prepare scrolled window
            self.window.scrolled_window.add(self.window.treeview)
            self.window.scrolled_window.show()
            # add new widgets and reorder
            self.window.vbox.remove(self.window.label_box)
            self.window.vbox.pack_start(self.window.scrolled_window, False, True, 0)
            self.window.vbox.pack_start(self.window.label_box, True, True, 0)
            self.window.bottom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            self.window.bottom_box.set_border_width(0)
            distance_label = Gtk.Label()
            distance_label.set_margin_start(64)
            distance_label.set_markup(_("<b>Total distance:</b>"))
            distance_label.set_margin_end(24)
            self.window.distance_entry = Gtk.Entry(text="0.0")
            self.window.bottom_box.pack_start(distance_label, False, True, 0)
            self.window.bottom_box.pack_start(self.window.distance_entry, False, True, 0)
            space_label = Gtk.Label(label=' ')
            self.window.bottom_box.pack_start(space_label, False, False, 0)
            duration_label = Gtk.Label()
            duration_label.set_margin_end(24)
            duration_label.set_markup(_("<b>Total duration:</b>"))
            self.window.duration_entry = Gtk.Entry(text="0.0")
            self.window.duration_entry.set_margin_end(64)
            self.window.bottom_box.pack_end(self.window.duration_entry, False, True, 0)
            self.window.bottom_box.pack_end(duration_label, False, True, 0)
            self.window.vbox.pack_start(self.window.bottom_box, False, True, 0)
            self.window.first_run = False
        gpx = tree.getroot()
        tag = gpx.tag
        # namespace in {}
        try:
            index = tag.index('}')
        except ValueError:
            index = -1
        index += 1
        ns = tag[0:index]
        # find all trackpoints
        points = 0
        total_duration = 0.0
        # distance by great circle haversine
        total_distance = 0.0
        # distance given by mytracks app
        tracks_distance = 0.0
        trackpoints = list()
        for trk in gpx.findall(f'{ns}trk'):
            for trkseg in trk.findall(f'{ns}trkseg'):
                for trkpt in trkseg.iter(f'{ns}trkpt'):
                    trackpoint = dict(points=0, latitude=0.0, longitude=0.0, elevation=0.0,\
                        time='', seconds=0.0, distance=0.0, velocity=0.0, length=0.0, speed=0.0)
                    lat = trkpt.get('lat')
                    lon = trkpt.get('lon')
                    ele_item = trkpt.find(f'{ns}ele')
                    ele = ele_item.text
                    trackpoint['latitude'] = float(lat)
                    trackpoint['longitude'] = float(lon)
                    trackpoint['elevation'] = float(ele)
                    time_item = trkpt.find(f'{ns}time')
                    date_string = time_item.text
                    z = date_string.index('Z')
                    parse_format = '%Y-%m-%dT%H:%M:%S'
                    # do we have milliseconds
                    try:
                        p = date_string.index('.')
                    except ValueError:
                        p = z
                        date_time = datetime.datetime.strptime(date_string, f'{parse_format}Z')
                    if p < z:
                        # add format with milliseconds
                        date_time = datetime.datetime.strptime(date_string, f'{parse_format}.%fZ')
                    # generate timedelta object to calculate the seconds
                    epoch_delta = date_time - datetime.datetime.utcfromtimestamp(0.0)
                    trackpoint['seconds'] = epoch_delta.total_seconds()
                    trackpoint['time'] = date_time.strftime('%a %b %d, %Y %H:%M:%S')
                    extensions = trkpt.find(f'{ns}extensions')
                    if extensions:
                        for ext in extensions:
                            try:
                                i = ext.tag.index('}')
                            except ValueError:
                                i = -1
                            i += 1
                            key = ext.tag[i:]
                            trackpoint[key] = ext.text
                    points += 1
                    trackpoint['Id'] = points
                    if points > 1:
                        # fetch last element
                        previous = trackpoints.pop()
                        elapsed_time = trackpoint['seconds'] - previous['seconds']
                        trackpoints.append(previous)
                        self.distanceByHaversine(previous, trackpoint)
                        total_distance += trackpoint['distance']
                        # very rarely elapsed_time is zero
                        try:
                            trackpoint['velocity'] = trackpoint['distance'] / elapsed_time * 3600.0
                        except ZeroDivisionError:
                            trackpoint['velocity'] = 0.0
                        total_duration += elapsed_time
                        if extensions:
                            tracks_distance += float(trackpoint['length'])
                    trackpoints.append(trackpoint)
        model = self.window.treeview.get_model()
        # delete data of an earlier run
        if (len(model) > 0):
            # make place for new table rows
            model.clear()
        names = ['Id', 'latitude', 'longitude', 'elevation', 'time', 'distance', 'velocity']
        for trackpoint in trackpoints:
            row_iter = model.append()
            for column, name in enumerate(names):
                model.set_value(row_iter, column, trackpoint[name])
        self.window.distance_entry.set_text(f(_('{total_distance: 5.3f} km')))
        # convert seconds to hh:mm:ss.f
        total_duration += 0.05
        hh, mm60 = divmod(total_duration, 3600)
        mm, ss = divmod(mm60, 60)
        self.window.duration_entry.set_text(f(_('{hh:2.0f}h {mm:2.0f}m {ss:2.1f}s')))
        print(f(_('total duration = {total_duration: 5.1f} seconds')))
        print(f(_('mytracks distance = {tracks_distance: 5.3f} km')))
        self.window.context_id = self.window.status_bar.push(self.window.context_id,\
            f(_('Track contains {points} trackpoints')))
        self.window.label.set_markup(f(_('<span face=\"mono\" weight=\"bold\">View XML data from {gpx_url}</span>')))
        self.window.add(self.window.vbox)
        self.window.show_all()

    def on_quit(self, action, parameter):
        self.window.destroy()

    def on_about(self, action, parameter):
        about = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about.set_logo(GdkPixbuf.Pixbuf.new_from_file("about.xpm"))
        about.set_program_name(_("pyGtk: XML Application - XML Data from GPX Track"))
        about.set_size_request(480, -1)
        about.set_version("Version 1.2.10")
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

# available translations
de = gettext.translation('pyXMLGPX-parser', localedir='locale', languages=['de'])
de.install()
# define _ shortcut for translations
_ = de.gettext # German
app = Application()
exit = app.run(sys.argv)
sys.exit(exit)

