# noinspection PyUnresolvedReferences
from Autodesk.Revit.UI import IExternalEventHandler, ExternalEvent
# noinspection PyUnresolvedReferences
from Autodesk.Revit.DB import Transaction
# noinspection PyUnresolvedReferences
from Autodesk.Revit.Exceptions import InvalidOperationException

from pyrevit.forms import WPFWindow

__doc__ = "A simple modeless form sample"
__title__ = "Modeless Form"
__author__ = "Cyril Waechter"

from rpw import revit, DB, UI

#uidoc = revit.uidoc
#doc = revit.doc

# Simple function we want to run
def delete_elements():
    t = Transaction(revit.doc, "Failing script")
    t.Start()
    for elid in revit.uidoc.Selection.GetElementIds():
        print(str(elid))
        #revit.doc.Delete(elid)
    t.Commit()


# Create a subclass of IExternalEventHandler
class SimpleEventHandler(IExternalEventHandler):
    """
    Simple IExternalEventHandler sample
    """

    # __init__ is used to make function from outside of the class to be executed by the handler. \
    # Instructions could be simply written under Execute method only
    def __init__(self, do_this):
        self.do_this = do_this

    # Execute method run in Revit API environment.
    def Execute(self, uiapp):
        try:
            self.do_this()
        except InvalidOperationException:
            # If you don't catch this exeption Revit may crash.
            print "InvalidOperationException catched"

    def GetName(self):
        return "simple function executed by an IExternalEventHandler in a Form"


# Now we need to make an instance of this handler. Moreover, it shows that the same class could be used to for
# different functions using different handler class instances
simple_event_handler = SimpleEventHandler(delete_elements)
# We now need to create the ExternalEvent
ext_event = ExternalEvent.Create(simple_event_handler)


# A simple WPF form used to call the ExternalEvent
class ModelessForm(WPFWindow):
    """
    Simple modeless form sample
    """

    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)
        self.simple_text.Text = "Hello World"
        self.Show()

    def delete_click(self, sender, e):
        # This Raise() method launch a signal to Revit to tell him you want to do something in the API context
        ext_event.Raise()

# Let's launch our beautiful and useful form !
modeless_form = ModelessForm("ModelessForm.xaml")