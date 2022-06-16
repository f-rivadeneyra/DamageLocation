import ifcopenshell
import ifcopenshell.geom 
import ifcopenshell.util
import ifcopenshell.util.element
from ifcopenshell.util.selector import Selector
from OCC.Core.gp import (gp_Vec, gp_Pnt,gp_XYZ, gp_Ax2, gp_Dir)
from OCC.Core.BRepBndLib import brepbndlib_Add, brepbndlib_AddOBB
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.TopoDS import TopoDS_Solid
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.Bnd import Bnd_OBB, Bnd_Box 
import math

def midpoint(pntA, pntB):
    
    """ computes the point that lies in the middle between pntA and pntB
    Parameters
    ----------
    pntA, pntB : gp_Pnt
    Returns
    -------
    gp_Pnt
    """
    vec1 = gp_Vec(pntA.XYZ())
    vec2 = gp_Vec(pntB.XYZ())
    veccie = (vec1 + vec2) * 0.5
    return gp_Pnt(veccie.XYZ())


def bounding_box_center(self):
    """
    Returns: center of Bnd_Box von Bauteil 
    """    
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)   
    if isinstance(self, ifcopenshell.entity_instance):
        shape = ifcopenshell.geom.create_shape(settings, self).geometry
    elif isinstance(self, TopoDS_Solid):
        shape = self
    
    bbox = Bnd_Box()
    brepbndlib_Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    corner1 = gp_Pnt(xmin, ymin, zmin)
    corner2 = gp_Pnt(xmax, ymax, zmax)
    center = midpoint(corner1, corner2)
    return center

def zmin_bauteil(self):
    """
    Returns: center of Bnd_Box von Bauteil 
    """    
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)   
    if isinstance(self, ifcopenshell.entity_instance):
        shape = ifcopenshell.geom.create_shape(settings, self).geometry
    elif isinstance(self, TopoDS_Solid):
        shape = self
    
    bbox = Bnd_Box()
    brepbndlib_Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    corner1 = gp_Pnt(xmin, ymin, zmin)
    corner2 = gp_Pnt(xmax, ymax, zmax)
    center = midpoint(corner1, corner2)
    return zmin

def ConvertBndToShape(theBox):
    aBaryCenter = theBox.Center()
    aXDir = theBox.XDirection()
    aYDir = theBox.YDirection()
    aZDir = theBox.ZDirection()
    aHalfX = theBox.XHSize()
    aHalfY = theBox.YHSize()
    aHalfZ = theBox.ZHSize()
    ax = gp_XYZ(aXDir.X(), aXDir.Y(), aXDir.Z())
    ay = gp_XYZ(aYDir.X(), aYDir.Y(), aYDir.Z())
    az = gp_XYZ(aZDir.X(), aZDir.Y(), aZDir.Z())
    p = gp_Pnt(aBaryCenter.X(), aBaryCenter.Y(), aBaryCenter.Z())
    anAxes = gp_Ax2(p, gp_Dir(aZDir), gp_Dir(aXDir))
    anAxes.SetLocation(gp_Pnt(p.XYZ() - ax*aHalfX - ay*aHalfY - az*aHalfZ))
    aBox = BRepPrimAPI_MakeBox(anAxes, 2.0*aHalfX, 2.0*aHalfY, 2.0*aHalfZ)
    return (aBox,ax,ay,az,aBaryCenter)


def get_front_face(BBox):
    """
    get Front Face(with FrontFace of BBox)
    """
    FrontF = BBox.FrontFace()
    return FrontF

def get_right_face(BBox):
    """
    get right Face(with RightFace of BBox)
    """
    RightF = BBox.RightFace()
    return RightF

def get_left_face(BBox):
    """
    get left Face(with LeftFace of BBox)
    """
    LeftF = BBox.LeftFace()
    return LeftF   

def get_top_face(BBox):
    """
    get left Face(with LeftFace of BBox)
    """
    TopF = BBox.TopFace()
    return TopF   
    
    
def get_vertex_list_bottom(BBox):
    """
    get vertex list of Bottom Face(with BottomFace of BBox)
    """
    BotF = BBox.BottomFace()
    vertex = TopExp_Explorer(BotF,TopAbs_VERTEX)
    return vertex


def get_z_coordinates_bottom(BBox):
    list_z = []
    vertex = get_vertex_list_bottom(BBox)
    while vertex.More() == True:
        currentvertex = vertex.Current()
        point = BRep_Tool.Pnt(currentvertex)
        list_z.append(round(point.Z(),2))
        vertex.Next()
    return list_z   

def get_vertex_list_front(BBox):
    """
    get vertex list of Front Face(with FrontFace of BBox)
    """
    FrontF = BBox.FrontFace()
    vertex = TopExp_Explorer(FrontF,TopAbs_VERTEX)
    return vertex

def get_x_coordinates_front(BBox):
    list_x = []
    vertex = get_vertex_list_front(BBox)
    while vertex.More() == True:
        currentvertex = vertex.Current()
        point = BRep_Tool.Pnt(currentvertex)
        list_x.append(round(point.X(),2))
        vertex.Next()
    return list_x  



def get_starting_z(BBox,along_model_height=False,zmin=0):
    """
    get z coordinate for local placement of representation
    """
    if along_model_height == True:
        init_z = zmin
    else:
        init_z = get_z_coordinates_bottom(BBox)[0]
    return init_z

def sorted_point_list_extrusion_area(solid,point):
    obb2 = Bnd_OBB()
    brepbndlib_AddOBB(solid, obb2)
    origin = ConvertBndToShape(obb2)[4]
    origin_x  = origin.X()
    origin_y = origin.Y()
    

    def clockwiseangle_and_distance(point):
        """
        takes points of surface and returns them in clockwise-order
        """
        vector = [point[0]-origin_x, point[1]-origin_y]
        lenvector = math.hypot(vector[0], vector[1])
        if lenvector == 0:
            return -math.pi, 0
        normalized = [vector[0]/lenvector, vector[1]/lenvector]
        dotprod  = normalized[0]*0 + normalized[1]*1     
        diffprod = 1*normalized[0] - 0*normalized[1]     
        angle = math.atan2(diffprod, dotprod)
        if angle < 0:
            return 2*math.pi+angle, lenvector
        return angle, lenvector

    plea = sorted(point, key=clockwiseangle_and_distance)
    plea.append(plea[0])

    return plea

def model_box(filename):
    """
    Creates a bounding box that contains all elements in model.
    Output = 0:BoundingBox, 1:xmin, 2:ymin, 3:zmin, 4:xmax, 5:ymax, 6:zmax, 7:height of BoundingBox
    """
    model = ifcopenshell.open(filename)   
    selector = Selector()
    bauteile= selector.parse(model, '.IfcBuildingElementProxy | .IfcWall | .IfcColumn | .IfcSlab | .IfcBeam') 
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)   
    bbox = Bnd_Box()
    for element in bauteile:
        shape = ifcopenshell.geom.create_shape(settings, element).geometry
        brepbndlib_Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    corner1 = gp_Pnt(xmin, ymin, zmin)
    corner2 = gp_Pnt(xmax, ymax, zmax)
    box = BRepPrimAPI_MakeBox(corner1, corner2)
    height_box = zmax - zmin
    return (box, xmin, ymin, zmin, xmax, ymax, zmax, height_box)
    
def elements_in_box(box,model,newfile):
    selector = Selector()
    proxies = selector.parse(newfile, ".IfcBuildingElementProxy[Name *= \"" + box + "\"] | .IfcWall[Name *= \"" + box + "\"] | .IfcColumn[Name *= \"" + box + "\"] | .IfcSlab[Name *= \"" + box + "\"] | .IfcBeam[Name *= \"" + box + "\"]")
    tree_settings = ifcopenshell.geom.settings()
    tree_settings.set(tree_settings.DISABLE_OPENING_SUBTRACTIONS, True)
    t = ifcopenshell.geom.tree()
    t.add_file(model, tree_settings)
    t.add_file(newfile,tree_settings)
    elements_in_box = t.select(proxies[0], extend=0,completely_within=False)
    return elements_in_box           

