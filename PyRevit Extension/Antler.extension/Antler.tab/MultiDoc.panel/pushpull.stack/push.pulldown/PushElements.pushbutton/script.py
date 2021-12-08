# -*- coding: utf-8 -*-

from rpw import revit, DB
from pyrevit import script, EXEC_PARAMS, forms
from System.Collections.Generic import List
import antler
from collections import OrderedDict


logger = script.get_logger()
output = script.get_output()


def push_elements_to_link(elements, link, from_doc=revit.doc):
    model_path = DB.ModelPathUtils.ConvertUserVisiblePathToModelPath(
        link.PathName)

    logger.info(link.PathName)
    logger.info(model_path)

    open_options = DB.OpenOptions()

    link_as_doc = revit.app.OpenDocumentFile(model_path, open_options)

    logger.info(link)
    logger.info(link_as_doc)

    element_type_id_list = List[DB.ElementId](
        [element.Id for element in elements])

    with DB.Transaction(link_as_doc, __commandname__) as t:
        t.Start()

        DB.ElementTransformUtils.CopyElements(
            from_doc,
            element_type_id_list,
            link_as_doc,
            DB.Transform.Identity,
            DB.CopyPasteOptions()
            )

        t.Commit()


# links = antler.collectors.elements_of_class_collector(
#     DB.RevitLinkType, select_types=False).ToElements()

xrefs = DB.ExternalFileUtils.GetAllExternalFileReferences(revit.doc)

revit_links = OrderedDict()

for xref in xrefs:
    print(xref)
    print(DB.RevitLinkType.IsLoaded(revit.doc, xref))
    element = revit.doc.GetElement(xref)
    print(element)

    if isinstance(element, DB.RevitLinkType):
        pass
        # print(dir(element))
        # print(element.Name)
        # revit_links[element.Name] = element
     # print(xrefs)

instances = antler.collectors.revit_link_instances_collector().ToElements()

print(instances)

for instance in instances:
    link_doc = instance.GetLinkDocument()
    link_type = revit.doc.GetElement(instance.GetTypeId())

    revit_links[link_type] = {"type": link_type, "instance": instance}

print(revit_links)

# selected_link_name = forms.SelectFromList.show(
#     sorted(revit_links.keys()),
#     multiselect=False,
# )
#
# selected_link = revit_links[selected_link_name]

other_doc = antler.forms.select_docs(
    multiselect=False, selection_filter=lambda x: not x.IsFamilyDocument or not x.IsLinked)


# # linkedDocs.AppendLine(
# #     "FileName: " + Path.GetFileName(linkDoc.PathName))
# link_type = doc.GetElement(instance.GetTypeId())
# linkedDocs.AppendLine("Is Nested: " + type.IsNestedLink.ToString())

# TaskDialog.Show("Revit Links in Document", linkedDocs.ToString())
#
#
#     print(revit_links)
#
#     other_doc = antler.forms.select_docs(
# multiselect = False, selection_filter = lambda x: not x.IsFamilyDocument)
#     #
#     # logger.debug(other_doc.Id)

elements = antler.ui.preselect(DB.Element)

#
# class duplicate_names_handler(DB.IDuplicateTypeNamesHandler):
#     pass

# class do_nothing(DB.ISaveSharedCoordinatesCallbackForUnloadLocally):
#     def GetSaveModifiedLinksOptionForUnloadLocally(self, link):
#         return None

#
# model_path = DB.ModelPathUtils.ConvertUserVisiblePathToModelPath(
#     selected_link["doc"].PathName)
#
# logger.info(link.PathName)
# logger.info(model_path)

# print(opened_doc)

# try:
#     selected_link["type"].UnloadLocally(None)
# except:
#     selected_link["type"].Unload(None)
#
# # try:
# open_options = DB.OpenOptions()
#
# with revit.app.OpenDocumentFile(model_path, open_options) as opened_doc:
with DB.Transaction(other_doc, __commandname__) as t:
    t.Start()

    DB.ElementTransformUtils.CopyElements(
        revit.doc,
        List[DB.ElementId](
            [element.Id for element in elements]),
        other_doc,
        DB.Transform.Identity,
        DB.CopyPasteOptions()
        )

    t.Commit()
# finally:
    # result = selected_link["type"].Reload()
    # other_doc.

    #
    # push_elements_to_link(element_types, other_doc)

    # element_type_id_list = List[DB.ElementId](
    #     [element_type.Id for element_type in element_types])
