from rpw import DB
import System.Enum


def builtin_category_from_category(category):
    """
    Returns corresponding Builtin Category from Category.
    """
    logger.debug(type(category))

    if isinstance(category, DB.BuiltInCategory):
        return category

    for builtin_category in System.Enum.GetValues(DB.BuiltInCategory):
        if DB.ElementId(builtin_category).IntegerValue == category.Id.IntegerValue:
            return builtin_category

    return None
