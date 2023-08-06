import sys
import os
# print("sys.path: ",sys.path)
# sys.path.append("E:\\tools\\python\\pyspeedx\\")
# sys.path.append("..\\pyspeedx\\")

path = os.path.abspath(__file__)
_dir = os.path.dirname(path)
package_dir = os.path.join(_dir,'..')
print("Test dir is : ",_dir)
print("package_dir  is : ",package_dir)

sys.path.append(package_dir)

# pyspeedx_path = os.path.dirname(path,'..')


# print(os.path.realpath(__file__))

# print("__file__ is :",__file__)
# print("__package__ is :",__package__)

# import os
# print (__file__)
# print (os.path.abspath(__file__))

#print("pyspeedx path is : ",pyspeedx_path)


# sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'..'))