"""

"""
# from rpw import revit, DB
# from pyrevit import script

from collections import OrderedDict

import math
import clr

from antler import LOGGER, DB, DOC
# global LOGGER
# global DOC

# LOGGER.info(globals())
# print(globals())
# global DB

MATERIAL_CACHE = {}

# DOC = revit.doc

def analysis_mesh_from_curveloop(curve_loops, height_offset, **mesh_settings):
    material = None
    operation_result = DB.TessellatedShapeBuilder.CreateMeshByExtrusion(
        curve_loops, DB.XYZ(0, 0, 1), height_offset, material)

class AnalysisRay():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
        self.ray = DB.Line.CreateUnbound(origin, direction)
        self.hits = []

    def intersect(self, face):
        intersection_result_array = clr.Reference[DB.IntersectionResultArray]()

        intersection = face.Intersect(self.ray, intersection_result_array)

        if intersection == DB.SetComparisonResult.Overlap:
            hit = {'face': face, 'intersections': intersection_result_array}
            self.hits.append(hit)

    @property
    def passed_through(self):
        global MATERIAL_CACHE

        passed_through = True

        for hit in self.hits:
            material_id = hit['face'].MaterialElementId

            if MATERIAL_CACHE.get(material_id):
                material = MATERIAL_CACHE[material_id]
            else:
                material = DOC.GetElement(material_id)
                MATERIAL_CACHE[material_id] = material

            if material.Transparency < 0.5:
                passed_through = False

                return passed_through

        return passed_through

    @property
    def has_hit(self):
        return bool(self.hits)

    @property
    def deconstructed(self):
        return self.origin, self.direction
        """
        iterator = hit['intersections'].ForwardIterator()
        iterator.Reset()
        while iterator.MoveNext():
            yield iterator.Current
        """


class AnalysisGrid():
    def __init__(self, bbox, size, side='back'):
        self.bbox = bbox
        if side.lower() == 'back':

            column_start = bbox.Min.Z
            self.column_steps = math.floor((bbox.Max.Z - column_start) / size)
            self.column_size = (bbox.Max.Z - column_start) / self.column_steps

            row_start = bbox.Min.X
            self.row_steps = math.floor((bbox.Max.X - row_start) / size)
            self.row_size = (bbox.Max.X - row_start) / self.row_steps

            self.cell_size = self.column_size * self.row_size

            y = bbox.Max.Y

            self.ray_direction = DB.XYZ(0, -1, 0)

            self.grid = OrderedDict()

            for i in range(int(self.column_steps)):
                z = column_start + (self.column_size / 2) + \
                    (i * self.column_size)

                row = []

                for i in range(int(self.row_steps)):
                    x = row_start + (self.row_size / 2) + (i * self.row_size)

                    ray = AnalysisRay(DB.XYZ(x, y, z), self.ray_direction)
                    row.append(ray)

                self.grid[z - column_start] = row

    def analyse_face(self, face):
        for row in self.grid.values():
            for ray in row:
                ray.intersect(face)

    @property
    def result(self):
        self._result = OrderedDict()

        for key, row in self.grid.items():
            row_sum = 0

            for ray in row:
                if ray.hits and ray.passed_through:
                    row_sum += self.cell_size

            key_metric = DB.UnitUtils.ConvertFromInternalUnits(
                key, DB.DisplayUnitType.DUT_MILLIMETERS)

            row_sum_metric = DB.UnitUtils.Convert(
                row_sum,
                DB.DisplayUnitType.DUT_SQUARE_FEET,
                DB.DisplayUnitType.DUT_SQUARE_METERS)

            # key_metric = round(key_metric, 1)
            # row_sum_metric = round(row_sum_metric, 3)

            self._result[key_metric] = row_sum_metric

        return self._result#.items()

    @property
    def deconstructed(self):
        return [[ray.deconstructed for ray in row] for row in self.grid.values()]


class TransparencyAnalyser():
    def __init__(self, element, grid_size=100, ray_direction=DB.XYZ(0,1,0)):
        if isinstance(element, DB.FamilySymbol):
            self.element = element
        elif isinstance(element, DB.FamilyInstance):
            self.element = element.Symbol
        else:
            self.element = element

        grid_size = DB.UnitUtils.ConvertToInternalUnits(
            grid_size, DB.DisplayUnitType.DUT_MILLIMETERS)

        self.bbox = self.element.get_BoundingBox(None)

        self.grid = AnalysisGrid(self.bbox, grid_size)

    def analyse(self):
        options = DB.Options()
        geometry_element = self.element.get_Geometry(options)

        logger.info(geometry_element)

        for geometry_object in geometry_element:
            if isinstance(geometry_object, DB.Solid):
                for face in geometry_object.Faces:
                    self.grid.analyse_face(face)

    @property
    def analysis_result(self):
        return self.grid.result

    @property
    def transparent_area(self):
        return sum(self.grid.result.values())



def get_sun_vectors(view):
    if view.SunAndShadowSettings.RelativeToView:
        # No sun settings are applied to the view...
        return

    elif view.SunAndShadowSettings.RelativeToView:
        pass
