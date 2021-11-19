from rpw import revit, DB
from pyrevit import forms, script

import math
import clr
import util

logger = script.get_logger()


def mesh_from_floor(floor, **mesh_settings):
    floor_curve_loops = None


def analysis_mesh_from_curveloop(curve_loops, height_offset, **mesh_settings):
    material = None
    operation_result = DB.TessellatedShapeBuilder.CreateMeshByExtrusion(
        curve_loops, DB.XYZ(0, 0, 1), height_offset, material)


def room_query(room_element, doc=revit.doc, boundary_location=DB.SpatialElementBoundaryLocation.Finish, ):
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
