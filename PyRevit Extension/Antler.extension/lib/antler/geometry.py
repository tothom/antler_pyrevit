from rpw import revit, DB
from pyrevit import forms, script

import math
import clr
import util

from System.Collections.Generic import List

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


# def transform2coordinatesystem(transform):
# 	origin = transform.Origin
# 	origin_pt = Autodesk.DesignScript.Geometry.Point.ByCoordinates(origin.X, origin.Y, origin.Z)
#
# 	basisX = transform.BasisX
# 	vectorX = Vector.ByCoordinates(basisX.X,basisX.Y,basisX.Z)
#
# 	basisY = transform.BasisY
# 	vectorY = Vector.ByCoordinates(basisY.X,basisY.Y,basisY.Z)
#
# 	basisZ = transform.BasisZ
# 	vectorZ = Vector.ByCoordinates(basisZ.X,basisZ.Y,basisZ.Z)
#
# 	coordinate_system = CoordinateSystem.ByOriginVectors(origin_pt, vectorX, vectorY, vectorZ)
#
# 	return coordinate_system


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
				# 	faces.append(face)
					# face_materials_ids.append(face.MaterialElementId)

				# geometry_element_faces.append(faces)
				# geometry_element_material_ids.append(face_materials_ids)

			# geometry_element_faces.append(solid_faces)
			# geometry_element_material_ids.append(solid_face_material_ids)

		faces.append(geometry_element_faces)
		# material_ids.append(geometry_element_material_ids)

	return faces
