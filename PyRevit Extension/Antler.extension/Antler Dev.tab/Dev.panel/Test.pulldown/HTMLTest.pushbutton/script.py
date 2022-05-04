from System.Collections.Generic import *
from rpw import revit, DB, UI

from pyrevit import forms
from collections import OrderedDict

import re
import os

import sys
if sys.platform != 'cli':
    import pythoncom
    pythoncom.CoInitialize()

import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Form, DockStyle, WebBrowser, TextBox, Keys
clr.AddReference('System.Security')
from System.Security import SecurityCriticalAttribute


__doc__ = "HTML Test"
__title__ = "HTML Test"
__author__ = "Thomas Holth"

uidoc = revit.uidoc
doc = revit.doc


html_path = os.path.join(__commandpath__, 'vis.html')
# html_path = r'https://visjs.github.io/vis-timeline/examples/timeline/basicUsage.html'
# print(html_path)


f = Form()
f.Text = 'WebBrowser Example'
f.Width = 800
f.Height = 600

wb = WebBrowser()
# wb.ScriptErrorsSuppressed = True
wb.AllowNavigation = True

# wb.OnVisibleChanged += wb.update
wb.Navigate(html_path, None, None,"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0")

wb.Dock = DockStyle.Fill
f.Controls.Add(wb)



# with open(os.path.join(__commandpath__, 'basic_network.js')) as js_file:
#     javascript = js_file.read()
#     # print(javascript)
#     wb.Document.InvokeScript(javascript, None)
# htmldoc = wb.Document

# head = htmldoc.GetElementsByTagName("head")
#
# for h in head:
#     print(h)
# print((head))
#
# s = htmldoc.CreateElement("script")
# s.SetAttribute("text","function sayHello() { alert('hello'); }")
# head.AppendChild(s)
    # browser.Document.InvokeScript("sayHello")

# Event handling
# def OnKeyPress(sender, args):
#     if args.KeyChar == u'\r':
#         wb.Navigate(tb.Text.strip())
# tb.KeyPress += OnKeyPress


f.ShowDialog()
