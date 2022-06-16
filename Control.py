import q_main
import Geom
import Ifc
import ifcopenshell
import ifcopenshell.geom 
import ifcopenshell.util
import ifcopenshell.util.element
from ifcopenshell.util.selector import Selector
from OCC.Core.gp import (gp_Pnt,gp_Pln)
from OCC.Core.BRepBndLib import brepbndlib_Add, brepbndlib_AddOBB
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.TopoDS import TopoDS_Solid
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.Bnd import Bnd_OBB, Bnd_Box 
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BOPAlgo import  BOPAlgo_Builder
from OCC.Core.BRepBuilderAPI import  BRepBuilderAPI_MakeFace
from OCC.Extend.TopologyUtils import TopologyExplorer
from ifcopenshell.util import element

def create_bt_file(filename, newfile_name):
    model = ifcopenshell.open(filename)   
    Ifc.create_ifc(model,newfile_name)
    f = ifcopenshell.open(newfile_name)
    model_box_ifc(filename,f,newfile_name)
    rechts_links(filename,f,newfile_name)
    anfang_endeDesBauwerks("Anfang",filename,newfile_name)
    anfang_endeDesBauwerks("Ende",filename,newfile_name)
    feld(filename,newfile_name)  

def model_box_ifc(filename,newfile,newfile_name):    
    box = Geom.model_box(filename)[0]
    height_box = Geom.model_box(filename)[7]
    top2_up_bottom = TopologyExplorer(box.Shape())
    for i, sol2 in enumerate(top2_up_bottom.solids()):
        vertex_F = TopExp_Explorer(sol2,TopAbs_VERTEX)
        x_y_F = []
        while vertex_F.More() == True:
            currentvertex = vertex_F.Current()
            point = BRep_Tool.Pnt(currentvertex)
            if[round(point.X(),2),round(point.Y(),2)] not in x_y_F:
                x_y_F.append([round(point.X(),2),round(point.Y(),2)])
            vertex_F.Next()
        plea_TBW = Geom.sorted_point_list_extrusion_area(sol2,x_y_F)

    Ifc.place_object(newfile,box,plea_TBW,height_box,"Gesamt",newfile_name)

    
def feld(filename,newfile_name):
    selector = Selector()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True) 
    model = ifcopenshell.open(filename)   
    pfeiler = []
    column= selector.parse(model, '.IfcColumn')
    for i in column:     
        if "PIERSTEM" in str(element.get_type(i)):
                pfeiler.append(i)          
    bauteile= selector.parse(model, '.IfcBuildingElementProxy | .IfcWall | .IfcColumn | .IfcSlab | .IfcBeam') 
    bbox = Bnd_Box()
    for i in bauteile:
        shape = ifcopenshell.geom.create_shape(settings, i).geometry
        brepbndlib_Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    corner1 = gp_Pnt(xmin, ymin, zmin)
    corner2 = gp_Pnt(xmax, ymax, zmax)
    box = BRepPrimAPI_MakeBox(corner1, corner2)
    h = Geom.model_box(filename)[7]
    cutlist = []
    center_pfeiler = []
    pnt_pfeiler = []
    for pfeiler1 in pfeiler:   
        center1 = Geom.bounding_box_center(pfeiler1)
        center_pfeiler.append((center1.X(),center1.Y(),center1.Z()))
    center_pfeiler_sorted = sorted(center_pfeiler, key=lambda x: x[0])
    for i in center_pfeiler_sorted:
        pnt_pfeiler.append(gp_Pnt(i[0],i[1],i[2]))
    i = 0
    while True:
        if i == len(pfeiler):
            break     
        else:
            pfeiler1 = pfeiler[i]  
            center1 = pnt_pfeiler[i]
            if isinstance(pfeiler1, ifcopenshell.entity_instance):
                shape = ifcopenshell.geom.create_shape(settings, pfeiler1).geometry
            elif isinstance(pfeiler1, TopoDS_Solid):
                shape = pfeiler1
            obb1 = Bnd_OBB()
            brepbndlib_AddOBB(shape, obb1)
            box1 = Geom.ConvertBndToShape(obb1)[0]
            rightface = Geom.get_top_face(box1)
            surf = BRepAdaptor_Surface(rightface, True)  
            plane = surf.Plane()
            normal = gp_Pln.Axis(plane).Direction()
            p1, v1 = gp_Pnt(center1.X()-2.0,center1.Y(),-2.0), normal
            p2 , v2 = gp_Pnt(center1.X()+2.0,center1.Y(),-2.0), normal
            fc1 = BRepBuilderAPI_MakeFace(gp_Pln(p1, v1))
            fc2 = BRepBuilderAPI_MakeFace(gp_Pln(p2, v2))
            cutlist.append(fc1)
            cutlist.append(fc2)
        i = i + 1
    #cut box in fields
    bo_F = BOPAlgo_Builder()
    bo_F.AddArgument(box.Shape())
    for cutlist1 in cutlist:
        bo_F.AddArgument(cutlist1.Shape())
    bo_F.Perform()
    top2 = TopologyExplorer(bo_F.Shape())
    h = 0
    t = 1
    for i, sol2 in enumerate(top2.solids()):
        if (h % 2 != 0):
            pass
        else:
            vertex_F = TopExp_Explorer(sol2,TopAbs_VERTEX)
            x_y_F = []
            while vertex_F.More() == True:
                currentvertex = vertex_F.Current()
                point = BRep_Tool.Pnt(currentvertex)
                if[round(point.X(),2),round(point.Y(),2)] not in x_y_F:
                    x_y_F.append([round(point.X(),2),round(point.Y(),2)])
                vertex_F.Next()
            plea_Feld = Geom.sorted_point_list_extrusion_area(sol2,x_y_F)
            zmin_model = Geom.model_box(filename)[3]
            zmax_model = Geom.model_box(filename)[6]
            height_box = zmax_model - zmin_model + 1.0
            k = ifcopenshell.open(newfile_name)
            Ifc.place_object(k,box,plea_Feld,height_box,str(t)+". Feld",newfile_name,along_model_height=True, zmin=zmin_model - 1.0)
            t = t + 1
        h = h + 1

def anfang_endeDesBauwerks(anfang_ende,filename,newfile_name):
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)   
    selector = Selector()
    model = ifcopenshell.open(filename)
    f = ifcopenshell.open(newfile_name)
    bauteile= selector.parse(model, '.IfcBuildingElementProxy[Name *= "Ueberbau"]')
    #create BBox out of Fahrbahn-Boundaries with tolerance
    bbox = Bnd_Box()
    for element in bauteile:
        shape = ifcopenshell.geom.create_shape(settings, element).geometry
        brepbndlib_Add (shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    corner1 = gp_Pnt(xmin-2, ymin-2, zmin)
    corner2 = gp_Pnt(xmax+2, ymax+2, zmax)
    box = BRepPrimAPI_MakeBox(corner1, corner2)
    #define limit of (AnfangDesBauwerks) along x-Axis and make a plane to cut box
    DistanceAnfangDesBauwerks = 1.50
    if anfang_ende == "Anfang":
        limit_point_1 =gp_Pnt(xmin-DistanceAnfangDesBauwerks, ymin,zmin)
        limit_point_2 =gp_Pnt(xmin+DistanceAnfangDesBauwerks, ymin,zmin)
    elif anfang_ende == "Ende":
        limit_point_1 =gp_Pnt(xmax-DistanceAnfangDesBauwerks, ymax,zmax)
        limit_point_2 =gp_Pnt(xmax+DistanceAnfangDesBauwerks, ymax,zmax)
    else:
        print("Error")            
    Widerlager = selector.parse(model, '.IfcWall')[0]
    center1 = Geom.bounding_box_center(Widerlager)
    if isinstance(Widerlager, ifcopenshell.entity_instance):
        shape = ifcopenshell.geom.create_shape(settings, Widerlager).geometry
    elif isinstance(Widerlager, TopoDS_Solid):
        shape = Widerlager
    obb1 = Bnd_OBB()
    brepbndlib_AddOBB(shape, obb1)
    box1 = Geom.ConvertBndToShape(obb1)[0]
    frontface = Geom.get_front_face(box1)
    surf = BRepAdaptor_Surface(frontface, True)  
    plane = surf.Plane()
    normal = gp_Pln.Axis(plane).Direction()
    cutting_face_1 = BRepBuilderAPI_MakeFace(gp_Pln(limit_point_1, normal))
    cutting_face_2 = BRepBuilderAPI_MakeFace(gp_Pln(limit_point_2, normal))
    #cut and create new box
    bo_AnfBau = BOPAlgo_Builder()
    bo_AnfBau.AddArgument(box.Shape())
    bo_AnfBau.AddArgument(cutting_face_1.Shape())
    bo_AnfBau.AddArgument(cutting_face_2.Shape())
    bo_AnfBau.Perform()
    top_AnfBau = TopologyExplorer(bo_AnfBau.Shape())
    solids_AnfBau = []
    for i, sol in enumerate(top_AnfBau.solids()):
        solids_AnfBau.append(sol)
    solid_AnfBau = solids_AnfBau[1]
    vertex_AnfBau = TopExp_Explorer(solid_AnfBau,TopAbs_VERTEX)
    x_y_AnfBau = []
    while vertex_AnfBau.More() == True:
        currentvertex = vertex_AnfBau.Current()
        point = BRep_Tool.Pnt(currentvertex)
        if[round(point.X(),2),round(point.Y(),2)] not in x_y_AnfBau:
            x_y_AnfBau.append([round(point.X(),2),round(point.Y(),2)])
        vertex_AnfBau.Next()
    plea_AnfBau = Geom.sorted_point_list_extrusion_area(solid_AnfBau,x_y_AnfBau)
    zmin_model = Geom.model_box(filename)[3]
    zmax_model = Geom.model_box(filename)[6]
    height_box = zmax_model - zmin_model + 1.0
    Ifc.place_object(f,box,plea_AnfBau,height_box,anfang_ende+"DesBauwerks",newfile_name,along_model_height=True,zmin = zmin_model - 1.0)

def rechts_links(filename,newfile,newfile_name):
    box = Geom.model_box(filename)[0]
    h = Geom.model_box(filename)[7]
    #get Teilbauwerksachse and make a plane to cut box in half
    middle_front =gp_Pnt(Geom.model_box(filename)[1], Geom.model_box(filename)[2]+(Geom.model_box(filename)[5]-Geom.model_box(filename)[2])/2,Geom.model_box(filename)[3])
    point_1 = gp_Pnt(middle_front.X(), middle_front.Y()-0.01, middle_front.Z())
    point_2 = gp_Pnt(middle_front.X(), middle_front.Y()+0.01, middle_front.Z())
    rightface = Geom.get_right_face(box)
    surf = BRepAdaptor_Surface(rightface, True)  
    plane = surf.Plane()
    normal = gp_Pln.Axis(plane).Direction()
    cutting_face_1 = BRepBuilderAPI_MakeFace(gp_Pln(point_1, normal))
    cutting_face_2 = BRepBuilderAPI_MakeFace(gp_Pln(point_2, normal))
    #cut box in half
    bo_RL = BOPAlgo_Builder()
    bo_RL.AddArgument(box.Shape())
    bo_RL.AddArgument(cutting_face_1.Shape())
    bo_RL.AddArgument(cutting_face_2.Shape())
    bo_RL.Perform()
    top_RL = TopologyExplorer(bo_RL.Shape())
    solids_RL = []
    for i, sol in enumerate(top_RL.solids()):
        solids_RL.append(sol)
    #place RL 1 and 2 in "control" ifc-file
    rechts_links = ["Rechts","Mitte","Links"]
    i = 1
    for j in rechts_links:
        if j != "Mitte":
            solid_RL = solids_RL[i-1]
            vertex_RL = TopExp_Explorer(solid_RL,TopAbs_VERTEX)
            x_y_RL = []
            while vertex_RL.More() == True:
                currentvertex = vertex_RL.Current()
                point = BRep_Tool.Pnt(currentvertex)
                if[round(point.X(),2),round(point.Y(),2)] not in x_y_RL:
                    x_y_RL.append([round(point.X(),2),round(point.Y(),2)])
                vertex_RL.Next()
            plea_RL = Geom.sorted_point_list_extrusion_area(solid_RL,x_y_RL)
            Ifc.place_object(newfile,box,plea_RL,h,j,newfile_name)
        i = i + 1

