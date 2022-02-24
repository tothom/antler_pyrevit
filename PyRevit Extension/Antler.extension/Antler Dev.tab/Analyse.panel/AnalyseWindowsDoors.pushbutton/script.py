from rpw import revit, DB
from pyrevit import forms, script

import json

import antler

logger = script.get_logger()

window_doors = antler.ui.preselect(DB.FamilyInstance)

window_door = window_doors[0]
window_door_symbol = window_door.Symbol

profile_parameter = window_door_symbol.LookupParameter('Transparency Profile')

profile_parameter_value = profile_parameter.AsString()

if profile_parameter_value:
    transparency_profile = json.loads(profile_parameter.AsString())

    logger.info(transparency_profile)

    existing_hash = transparency_profile['hash']
    new_hash = antler.compare.hash_element_by_parameters(
       window_door_symbol, exceptions=[profile_parameter])
    #
    logger.info(existing_hash)
    logger.info(new_hash)
    logger.info(existing_hash == new_hash)

    if existing_hash == new_hash:
        script.exit()

analyser = antler.analysis.TransparencyAnalyser(window_door, grid_size=50)
analyser.analyse()

# logger.info(analyser.analysis_result)
logger.info(analyser.transparent_area)

profile = {
    'hash': antler.compare.hash_element_by_parameters(
        window_door_symbol, exceptions=[profile_parameter]),
    'profile': analyser.analysis_result
    }

profile_json = json.dumps(profile)

logger.info(profile_json)

with DB.Transaction(revit.doc, __commandname__) as t:
    t.Start()
    profile_parameter.Set(profile_json)
    t.Commit()



# logger.info(analyser.grid.bbox)

# logger.info(analyser.geometry)
