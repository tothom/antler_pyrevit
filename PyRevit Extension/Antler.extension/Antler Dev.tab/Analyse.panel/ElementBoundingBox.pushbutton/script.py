from rpw import revit, DB
from pyrevit import forms, script

import json

import antler

from antler import LOGGER


elements = antler.ui.preselect(DB.FamilyInstance)

element = elements[0]



vector = DB.XYZ(0.5,0.5,0.5)
plane = antler.geometry.z_oriented_plane_from_vector(vector)
transform = antler.geometry.transform.from_plane(plane)


geometry_element = element.get_Geometry(DB.Options())


LOGGER.info(geometry_element)
LOGGER.info([a for a in geometry_element])

instance_geometry_elements = []

for geometry_instance in geometry_element:
    instance_geometry = geometry_instance.GetInstanceGeometry(transform)
    instance_geometry_elements.append(instance_geometry)

LOGGER.info(instance_geometry_elements)


geometry = instance_geometry_elements[0]

# geometry = [a.GetInstanceGeometry() for a in geometry_element]

# instance_geometry = geometry.GetInstanceGeometry()

element_bbox = element.get_BoundingBox(None)

LOGGER.info(element_bbox)
[LOGGER.info(a) for a in antler.geometry.bounding_box.query(element_bbox).items()]
#bbox = geometry.GetBoundingBox()



geometry_bbox = antler.geometry.bounding_box.get_filtered_bounding_box(geometry)

LOGGER.info(geometry_bbox)
[LOGGER.info(a) for a in antler.geometry.bounding_box.query(geometry_bbox).items()]


# #
# # for bbox in bboxes:
# #     LOGGER.info(antler.geometry.bounding_box.query(bbox))
#
#
# oriented_bbox = antler.geometry.bounding_box.from_vector(geometry, DB.XYZ(0.5,0.5,0))
#
# LOGGER.info(oriented_bbox)
# LOGGER.info(antler.geometry.bounding_box.query(oriented_bbox))
