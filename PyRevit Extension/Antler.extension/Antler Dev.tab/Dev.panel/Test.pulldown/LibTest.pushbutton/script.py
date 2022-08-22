import sys
import antler_revit

print(sys.path)
print(dir(antler_revit))

print([a for a in antler_revit.utils.drange(0, 5, 0.33)])
