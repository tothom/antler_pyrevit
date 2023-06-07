from rpw import revit, DB
from pyrevit import forms, script

import math
import clr

from System.Collections.Generic import List

logger = script.get_logger()

import transform
import bounding_box
from antler import utils


def z_oriented_plane_from_vector(vector, origin=DB.XYZ(0,0,0)):
    """
    Returns a plane facing in direction of input vector direction, where side
    orientation (y-axis) is always horisontal. It's a plane without any roll.
    """
    vector = vector.Normalize()

    if vector.IsAlmostEqualTo(DB.XYZ(0,0,1)):
        y_axis = DB.XYZ(0, 1,0)

    elif vector.IsAlmostEqualTo(DB.XYZ(0,0,-1)):
        y_axis = DB.XYZ(0,-1,0)

    else:
        y_axis = DB.XYZ(0,0,1).CrossProduct(vector)
        y_axis = y_axis.Normalize()

    plane = DB.Plane.CreateByOriginAndBasis(origin, vector, y_axis)

    return plane





def mesh_from_floor(floor, **mesh_settings):
    floor_curve_loops = None





def room_query(room_element, doc=revit.doc, **options):
    faces = []
    materials = []
    elements = []

    if room_element.Area == 0:
        return None, None, None

    spatialElementBoundaryOptions = DB.SpatialElementBoundaryOptions()

    for name, value in options:
        setattr(spatialElementBoundaryOptions, name, value)

    spatialElementBoundaryOptions.SpatialElementBoundaryLocation = DB.SpatialElementBoundaryLocation.Finish

    calculator = SpatialElementGeometryCalculator(doc, spatialElementBoundaryOptions)
    results = calculator.CalculateSpatialElementGeometry(room)

    roomSolid = results.GetGeometry()

    for roomSolidFace in roomSolid.Faces:
        materials_tmp = []
        faces_tmp = []
        elements_tmp = []

        for subface in results.GetBoundaryFaceInfo(roomSolidFace):
            boundingElementface = subface.GetBoundingElementFace()
            material = doc.GetElement(boundingElementface.MaterialElementId)
            materials_tmp.append(material)

            boundary_element = doc.GetElement(subface.SpatialBoundaryElement.HostElementId)
            elements_tmp.append(boundary_element)

            face = subface.GetSubface()
            faces_tmp.append(face.Convert()[0])


        elements.append(elements_tmp)
        materials.append(materials_tmp)
        faces.append(faces_tmp)

    return faces, materials, elements


def crv_loops_from_room(room, inner_boundary=False):
    """
    """
    options = DB.SpatialElementBoundaryOptions()
    options.SpatialElementBoundaryLocation = DB.SpatialElementBoundaryLocation.Finish

    boundary_segments = room.GetBoundarySegments(options)

    crv_loops = List[DB.CurveLoop]()

    crvs = List[DB.Curve]()

    for segment in boundary_segments[0]:
        crv = segment.GetCurve()
        crvs.Add(crv)

    crv_loop = DB.CurveLoop.Create(crvs)

    crv_loops.Add(crv_loop)

    if boundary_segments.Count > 1 and inner_boundary:
        crvs = List[DB.Curve]()

        for segment in boundary_segments[1]:
            crv = segment.GetCurve()
            crvs.Add(crv)

        crv_loop = DB.CurveLoop.Create(crvs)

        crv_loops.Add(crv_loop)

    return crv_loops


def find_associated_floor(window_door, view_3d, ray_offset=1, max_proximity=3):
    floor_filter = DB.ElementCategoryFilter(DB.BuiltInCategory.OST_Floors)
    # floor_filter = DB.ElementClassFilter(DB.Floor)

    # collector = DB.FilteredElementCollector(revit.doc, view_3d).OfClass(DB.Floor)
    element_list = List

    location_offset = window_door.FacingOrientation.Negate().Multiply(ray_offset)

    logger.info(window_door.FacingOrientation)
    logger.info(location_offset)

    # location_offset.Multiply(ray_offset)

    origin = window_door.Location.Point.Add(location_offset)

    logger.info(window_door.Location.Point)
    logger.info(origin)

    direction = DB.XYZ(0,0,-1)

    # floors_list = List[object](floors)

    intersector = DB.ReferenceIntersector(floor_filter, DB.FindReferenceTarget.Element, view_3d)

    reference_with_context = intersector.FindNearest(origin, direction)

    logger.info(reference_with_context)
    logger.info(reference_with_context.Proximity)

    if reference_with_context:# and reference_with_context.Proximity < max_proximity:
        reference = reference_with_context.GetReference()

        return reference.ElementId, reference.GlobalPoint


def get_family_instance_faces(family_instance, options=DB.Options()):
    faces = []
    # material_ids = []

    for geometry_element in family_instance.get_Geometry(options):

        geometry_element_faces = []
        # geometry_element_material_ids = []

        for geometry in geometry_element.GetSymbolGeometry():
            if isinstance(geometry, Autodesk.Revit.DB.Solid):
                # face_materials_ids = []
                # faces = []
                geometry_element_faces.append(geometry.Faces)

                # for face in geometry.Faces:
                #     faces.append(face)
                    # face_materials_ids.append(face.MaterialElementId)

                # geometry_element_faces.append(faces)
                # geometry_element_material_ids.append(face_materials_ids)

            # geometry_element_faces.append(solid_faces)
            # geometry_element_material_ids.append(solid_face_material_ids)

        faces.append(geometry_element_faces)
        # material_ids.append(geometry_element_material_ids)

    return faces
