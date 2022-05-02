from rpw import DB

from antler import LOGGER

import antler.geometry
# import transform

def query(bbox):
    return {
        'BoundEnabled': [[bbox.BoundEnabled[i, j] for i in range(2)] for j in range(3)], #Indexed access for loops.
        'Bounds': [bbox.Bounds[i] for i in range(2)], #Indexed access for loops. Use 0 for Min and 1 for Max.
        'Enabled': bbox.Enabled, #Defines whether the entire bounding box is enabled.
        'Max': bbox.Max, #Maximum coordinates (upper-right-front corner of the box).
        'MaxEnabled': [bbox.MaxEnabled[i] for i in range(3)], #Defines whether the maximum bound is active for given dimension.
        'Min': bbox.Min, #Minimum coordinates (lower-left-rear corner of the box).
        'MinEnabled': [bbox.MinEnabled[i] for i in range(3)], #Defines whether the minimum bound is active for given dimension.
        'Transform': antler.geometry.transform.query(bbox.Transform), #The transform from the coordinate space of the box to the model coordinate space.
        'Dimensions': [
            bbox.Max.X - bbox.Min.X,
            bbox.Max.Y - bbox.Min.Y,
            bbox.Max.Z - bbox.Min.Z
        ],
        'Center Point': DB.XYZ(
            (bbox.Max.X + bbox.Min.X)/2,
            (bbox.Max.Y + bbox.Min.Y)/2,
            (bbox.Max.Z + bbox.Min.Z)/2
        )
    }

def union_bounding_box(bbox_a, bbox_b):
    """
    Doesn't really work. This function must also consider the bounding box
    transforms.
    """
    bbox_new = DB.BoundingBoxXYZ()

    bbox_new.Min = DB.XYZ(
        min(bbox_a.Min.X, bbox_b.Min.X),
        min(bbox_a.Min.Y, bbox_b.Min.Y),
        min(bbox_a.Min.Z, bbox_b.Min.Z)
        )

    bbox_new.Max = DB.XYZ(
        max(bbox_a.Max.X, bbox_b.Max.X),
        max(bbox_a.Max.Y, bbox_b.Max.Y),
        max(bbox_a.Max.Z, bbox_b.Max.Z)
        )

    bbox_new.Transform = bbox_a.Transform

    LOGGER.info(bbox_new.Transform.Origin)

    return bbox_new


def from_vector(geometry_element, vector, origin=DB.XYZ(0,0,0)):
    plane = antler.geometry.z_oriented_plane_from_vector(vector, origin)

    xform = antler.geometry.transform.from_plane(plane)
    transformed_geometry_element = geometry_element.GetTransformed(xform)

    bbox = get_filtered_bounding_box(transformed_geometry_element)

    return bbox


def valid_solid_filter(geometry_object):
    if isinstance(geometry_object, DB.Solid):
        if geometry_object.Faces.Size > 0:
            return True


def get_filtered_bounding_box(geometry_element, filter_func=valid_solid_filter):
    bboxes = []

    LOGGER.debug(geometry_element)

    union_bbox = None

    for geometry_object in geometry_element:

        if filter_func(geometry_object):
            bbox = geometry_object.GetBoundingBox()

            LOGGER.debug(bbox)
            LOGGER.debug(query(bbox))
            LOGGER.info("Transform")
            [LOGGER.info(a) for a in antler.geometry.transform.query(bbox.Transform).items()]

            if not union_bbox:
               union_bbox = geometry_object.GetBoundingBox()
            else:
               union_bbox = union_bounding_box(union_bbox, geometry_object.GetBoundingBox())

            bboxes.append(bbox)

            #if bbox.Enabled:
            #    bboxes.append(bbox)

    return union_bbox
