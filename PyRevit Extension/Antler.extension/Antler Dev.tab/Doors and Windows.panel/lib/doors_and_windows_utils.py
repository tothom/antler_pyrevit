

def write_handing(family_instance, parameter, right_string='R', left_string='L'):
    if family_instance.HandFlipped != family_instance.FacingFlipped:
        parameter.Set(right_string)
    else:
        parameter.Set(left_string)

    return family_instance
