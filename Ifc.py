import ifcopenshell
import ifcopenshell.geom 
import ifcopenshell.util
import ifcopenshell.util.element
from ifcopenshell.util.selector import Selector
import uuid
import Geom 

def get_project_information(model):
    owner_history = ""
    project = model.by_type("IfcProject")[0]
    context = (project.RepresentationContexts)[0]
    site = model.by_type("IfcSite")[0]
    building = model.by_type("IfcBuilding")[0]
    building_storey = model.by_type("IfcBuildingStorey")[0]
    storey_placement = model.by_type("IfcLocalPlacement")[0]
    return (owner_history,context,site,building,building_storey,storey_placement)

def create_ifcaxis2placement(ifcfile, point=(0., 0., 0.), dir1=(1., 0., 0.), dir2=(0., 0., 1.)):
    """
    Creates an IfcAxis2Placement3D from Location, Axis and RefDirection specified as Python tuples
    """
    point = ifcfile.createIfcCartesianPoint(point)
    dir1 = ifcfile.createIfcDirection(dir1)
    dir2 = ifcfile.createIfcDirection(dir2)
    axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
    return axis2placement


def create_ifclocalplacement(ifcfile, point=(0., 0., 0.), dir1=(1., 0., 0.), dir2=(0., 0., 1.), relative_to=None):
    """
    Creates an IfcLocalPlacement from Location, Axis and RefDirection, specified as Python tuples, and relative placement
    """
    axis2placement = create_ifcaxis2placement(ifcfile,point,dir1,dir2)
    ifclocalplacement2 = ifcfile.createIfcLocalPlacement(relative_to,axis2placement)
    return ifclocalplacement2

def create_ifcpolyline(ifcfile, point_list):
    """
    Creates an IfcPolyLine from a list of points, specified as Python tuples
    """
    ifcpts = []
    for point in point_list:
        point = ifcfile.createIfcCartesianPoint(point)
        ifcpts.append(point)
    polyline = ifcfile.createIfcPolyLine(ifcpts)
    return polyline

def create_ifcextrudedareasolid(ifcfile, point_list, ifcaxis2placement, extrude_dir, extrusion):
    """
    Creates an IfcExtrudedAreaSolid from a list of points, specified as Python tuples
    """
    polyline = create_ifcpolyline(ifcfile, point_list)
    ifcclosedprofile = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
    ifcdir = ifcfile.createIfcDirection(extrude_dir)
    ifcextrudedareasolid = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile, ifcaxis2placement, ifcdir, extrusion)
    return ifcextrudedareasolid

def create_ifc(f,new_filename):     
    
    selector = Selector()
    bauteile= selector.parse(f, '.IfcBuildingElementProxy | .IfcWall | .IfcColumn | .IfcSlab | .IfcBeam | .IfcStair| .IfcStairFlight | .IfcRailing | .IfcFooting')

    for bauteil in bauteile:
        
        f.remove(bauteil)
    
    f.write(new_filename)

def place_object(file,box,point_list_extrusion_area,h,name,filename,along_model_height=False,zmin=0,Description = "BoundingBox"):
    """
    Creates a representation of bottom face in a new ifc-file
    """
    context = get_project_information(file)[1]
    building_storey = get_project_information(file)[4]
    storey_placement = get_project_information(file)[5]
    create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)
    bbox_placement = create_ifclocalplacement(file, relative_to=storey_placement)
    polyline = create_ifcpolyline(file, [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)])
    axis_representation = file.createIfcShapeRepresentation(context, "Axis", "Curve2D", [polyline])
    starting_z = Geom.get_starting_z(box,along_model_height,zmin)
    extrusion_placement = create_ifcaxis2placement(file, (starting_z, 0.0, 0.0), (1.0, 0.0, 0.0),(0.0, 0.0, 1.0))
    solid = create_ifcextrudedareasolid(file, point_list_extrusion_area, extrusion_placement, (0.0, 0.0, 1.0), h)
    body_representation = file.createIfcShapeRepresentation(context, "Body", "SweptSolid", [solid])
    product_shape = file.createIfcProductDefinitionShape(None, None, [axis_representation, body_representation])
    BBox = file.createIfcBuildingElementProxy(create_guid(), None, name, Description, None, bbox_placement, product_shape, None)
    file.createIfcRelContainedInSpatialStructure(create_guid(), None, "Building Storey Container", None, [BBox], building_storey)
    file.write(filename)