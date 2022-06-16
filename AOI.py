from pickle import BYTEARRAY8
import q_main
import Geom
import Ifc
import AOI
from OCC.Core.BRep import BRep_Tool
import ifcopenshell
import ifcopenshell.geom 
import ifcopenshell.util
import ifcopenshell.util.element
from ifcopenshell.util.selector import Selector
from OCC.Core.gp import (gp_Pnt)
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.Bnd import Bnd_Box 
from OCC.Extend.TopologyUtils import TopologyExplorer
import json
import numpy


def create_aoi_file(data_filename, filename, newfile_name):
    model = ifcopenshell.open(filename)   
    Ifc.create_ifc(model,newfile_name)
    f = ifcopenshell.open(newfile_name)

def new_aoi_instance(data_filename,schadenObjekt,i,key,aoi_string):
    
    schadenquery = q_main.query_schaden(data_filename,schadenObjekt)

    if "AOI" not in schadenquery:
        q_main.create_AOI(data_filename,schadenObjekt)

    schadenquery = q_main.query_schaden(data_filename,schadenObjekt)

    aoi = str(schadenquery["AOI"])[32:]

    q_main.add_AOI(data_filename,aoi,key,aoi_string)

def bauteildefinition_as_aoi(bauteildefinition,data_filename,schadenObjekt,i,bauteilTyp):    
    query_btd = q_main.query_bauteildefinition(data_filename,bauteildefinition)
    while True: 
        if str(bauteilTyp) ==  "RAILING":
            if "Fuss" in str(query_btd.values()):
                AOI.new_aoi_instance(data_filename,schadenObjekt,i,"ANSK","OrtsangabeBauteilSchaden_Allgemein_Unterseite")
                break
            if "Handlauf" in str(query_btd.values()):
                AOI.new_aoi_instance(data_filename,schadenObjekt,i,"ANSK","OrtsangabeBauteilSchaden_Allgemein_Oberseite")
                break
        if str(bauteilTyp) == "Widerlager_Wand_Vorne":
                AOI.new_aoi_instance(data_filename,schadenObjekt,i,"AONS","130091300000000_Hinten")
                break
        if str(bauteilTyp) == "Widerlager_Wand_Hinten":
                AOI.new_aoi_instance(data_filename,schadenObjekt,i,"AONS","130091100000000_Vorne")
                break
        if str(bauteilTyp) == "Fluegel_Wand_Hinten":
                if "Rechts" in str(query_btd.values()):
                    AOI.new_aoi_instance(data_filename,schadenObjekt,i,"AONS","130101200000000_Rechts")
                    break
                elif "Links" in str(query_btd.values()):
                    AOI.new_aoi_instance(data_filename,schadenObjekt,i,"AONS","130101100000000_Links")
                    break 
                else:
                    AOI.new_aoi_instance(data_filename,schadenObjekt,i,"ANSK","OrtsangabeBauteilSchaden_Allgemein_beidseitig")
                    break   
        else:
            break


def merge_box(box1,box2):
    try:
        xx = max(box1[0].X(), box2[0].X())
        yy = max(box1[0].Y(), box2[0].Y())
        zz = max(box1[0].Z(), box2[0].Z())
        aa = min(box1[1].X(), box2[1].X())
        bb = min(box1[1].Y(), box2[1].Y())
        cc = min(box1[1].Z(), box2[1].Z())
        corner_1 = gp_Pnt(xx,yy,zz)
        corner_2 = gp_Pnt(aa,bb,cc)
    except:
        corner_1 = gp_Pnt(box1[0].X(),box1[0].Y(),box1[0].Z())
        corner_2 = gp_Pnt(box1[1].X(),box1[1].Y(),box1[1].Z())
    return corner_1,corner_2

def points(box,type):
    if "New" in type:
        gesamt = box
        mapped = {"New":gesamt}
    else:
        settings = ifcopenshell.geom.settings()
        settings.set(settings.USE_PYTHON_OPENCASCADE, True) 
        bbox = Bnd_Box()
        try:
            shape = ifcopenshell.geom.create_shape(settings, box).geometry
        except:
            shape = ifcopenshell.geom.create_shape(settings, box[0]).geometry   
        brepbndlib_Add(shape, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
        delta_x = (xmax - xmin)/3
        delta_z = (zmax - zmin)/3
        if "X_" in type or "Y_" in type or "Z_" in type:
            gesamt = 0
        else:
            bbox2 = Bnd_Box()
            shape2 = ifcopenshell.geom.create_shape(settings,box).geometry
            brepbndlib_Add(shape2, bbox2)
            xmin2, ymin2, zmin2, xmax2, ymax2, zmax2 = bbox2.Get()
            c1_ges =  gp_Pnt(xmin2, ymin2, zmin2)
            c2_ges = gp_Pnt(xmax2, ymax2, zmax2)
            gesamt = (c1_ges,c2_ges)
        c_1A = gp_Pnt(xmin, ymin, zmin)
        c_1B = gp_Pnt(xmin + delta_x, ymin, zmin)
        c_1C = gp_Pnt(xmin + 2*delta_x, ymin, zmin)
        c_1D = gp_Pnt(xmin + 3*delta_x, ymin, zmin)
        c_2A = gp_Pnt(xmin, ymin+0.5, zmax)
        c_2B = gp_Pnt(xmin + delta_x, ymin+0.5, zmax)
        c_2C = gp_Pnt(xmin + 2*delta_x, ymin+0.5, zmax)
        c_2D = gp_Pnt(xmin + 3*delta_x, ymin+0.5, zmax)
        c_3A = gp_Pnt(xmin, ymax-0.5, zmin)
        c_3B = gp_Pnt(xmin + delta_x, ymax-0.5, zmin)
        c_3C = gp_Pnt(xmin + 2*delta_x, ymax-0.5, zmin)
        c_3D = gp_Pnt(xmin + 3*delta_x, ymax-0.5, zmin)
        c_4A = gp_Pnt(xmin, ymax, zmax)
        c_4B = gp_Pnt(xmin + delta_x, ymax, zmax)
        c_4C = gp_Pnt(xmin + 2*delta_x, ymax, zmax)
        c_4D = gp_Pnt(xmin + 3*delta_x, ymax, zmax)
        c_5A = gp_Pnt(xmin,ymin,zmin+delta_z)
        c_5B = gp_Pnt(xmax,ymax,zmin+delta_z)
        c_6A = gp_Pnt(xmin,ymin,zmin+2*delta_z)
        c_6B = gp_Pnt(xmax,ymax,zmin+2*delta_z)
        x0 = (c_1A, c_4B)
        x1 =(c_1B, c_4C)
        x2 = (c_1C, c_4D)
        y0 = (c_1A, c_2D)
        y1 = (c_3A, c_4D)
        z0 = (c_1A,c_5B)
        z1 = (c_5A,c_6B)
        z2 = (c_6A,c_4D)
        
        mapped = {"X_Hinten":x0,"X_Mitte":x1,"X_Vorne":x2,"Y_Rechts":y0,"Y_Links":y1,"Z_Unten":z0,"Z_Mitte":z1,"Z_Oben":z2,"EndeDesBauwerks" : gesamt,
        "AnfangDesBauwerks": gesamt, "Rechts":gesamt, "Links":gesamt, "New":gesamt}

    return mapped[type]

def place_aoi(box,height_box,aoi_filename,name,BauteilTyp):
    g = ifcopenshell.open(aoi_filename)
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
        plea = Geom.sorted_point_list_extrusion_area(sol2,x_y_F)
    Ifc.place_object(g,box,plea,height_box,name,aoi_filename,Description=BauteilTyp) 


def aoi_instance(lb,filename,bt_filename,aoi_filename,schadenObjekt,GlobalId,BauteilTyp):
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True) 
    selector = Selector()
    model = ifcopenshell.open(filename)
    f = ifcopenshell.open(bt_filename)
    number = 1
    for aoi_list in lb:
        list_of_boxes = {}
        for i in aoi_list:
            if "X_" in i or "Y_" in i or "Z_" in i:
                input_box = selector.parse(model, ".IfcBuildingElementProxy[GlobalId *= \""+GlobalId+"\"] | .IfcWall[GlobalId *= \""+GlobalId+"\"] | .IfcColumn[GlobalId *= \""+GlobalId+"\"] | .IfcRailing[GlobalId *= \""+GlobalId+"\"] | .IfcSlab[GlobalId *= \""+GlobalId+"\"] | .IfcBeam[GlobalId *= \""+GlobalId+"\"] | .IfcStairFlight[GlobalId *= \""+GlobalId+"\"]")[0]
                list_of_boxes[i] = input_box
            else:
                input_box = selector.parse(f, ".IfcBuildingElementProxy[Name*= \""+i+"\"]")[0]
                list_of_boxes[i] = input_box
        count = 0
        if len(list_of_boxes) == 1:
            a = list(list_of_boxes.values())[0]
            a_type = list(list_of_boxes.keys())[0]
            corner_1 =AOI.points(a,a_type)[0]
            corner_2 =AOI.points(a,a_type)[1]
            zmax =corner_1.Z()
            zmin = corner_2.Z()
            box = BRepPrimAPI_MakeBox(corner_1, corner_2)
        else:
            while True:
                    a = list(list_of_boxes.values())[0]
                    a_type = list(list_of_boxes.keys())[0]
                    b = list(list_of_boxes.values())[1]
                    b_type = list(list_of_boxes.keys())[1]
                    corner_1 =AOI.merge_box(AOI.points(a,a_type),AOI.points(b,b_type))[0]
                    corner_2 = AOI.merge_box(AOI.points(a,a_type),AOI.points(b,b_type))[1]
                    zmax = corner_1.Z()
                    zmin = corner_2.Z()
                    box = (corner_1, corner_2)
                    list_of_boxes.pop(a_type)
                    list_of_boxes.pop(b_type) 
                    list_of_boxes["New"] = (corner_1,corner_2)       
                    count = count + 2
                    if len(list_of_boxes) == 2:
                        a = list(list_of_boxes.values())[0]
                        a_type = list(list_of_boxes.keys())[0]
                        b = list(list_of_boxes.values())[1]
                        b_type = list(list_of_boxes.keys())[1]
                        corner_1 =AOI.merge_box(AOI.points(a,a_type),AOI.points(b,b_type))[0]
                        corner_2 = AOI.merge_box(AOI.points(a,a_type),AOI.points(b,b_type))[1]
                        zmax = corner_1.Z()
                        zmin = corner_2.Z()
                        box = BRepPrimAPI_MakeBox(corner_1, corner_2)   
                        count = count + 2  
                        break                    
                    elif len(list_of_boxes) == 1:
                        box = BRepPrimAPI_MakeBox(corner_1, corner_2)
                        break                        
        height_box = abs(zmax-zmin)
        AOI.place_aoi(box,height_box,aoi_filename,schadenObjekt[32:]+"_"+str(number),BauteilTyp)
        number = number + 1     

def aoi_main(schadenObjekt,bauteildefinition,data_filename,filename,bt_filename,aoi_filename,lbd_filename):

    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True) 
    selector = Selector()
    model = ifcopenshell.open(filename)
    f = ifcopenshell.open(bt_filename)

    schadenquery = q_main.query_schaden(data_filename,schadenObjekt)
    inst_list = q_main.query_bauteildefinition_hasModelRepresentation(data_filename,bauteildefinition)
    BauteilTyp = q_main.query_bauteildefinition_bauteilTyp(data_filename,bauteildefinition)

    with open("map_aoi.json", "r") as file:
        map_aoi = json.loads(file.read())

    for inst in inst_list:
        ####Fall 1: SchadenObjekt enthält Information zur AOI

        GlobalId = q_main.get_GlobalId(lbd_filename,inst)

        if "AOI" in schadenquery:

            aoi_query = q_main.query_aoi(data_filename,str(schadenquery["AOI"]))
            lx = []
            ly = []
            lz = []
            lc = []
            la = []
            for h in aoi_query:
                aoi = map_aoi[str(h)]
                for i in aoi:
                    if "X_" in i and i not in lx:
                        lx.append(i)
                    if "Y_" in i and i not in ly:
                        ly.append(i)
                    if "Z_" in i and i not in lz:
                        lz.append(i)
                    if "Control_" in i and i not in lc:
                        lc.append(i[8:])

            if lx:
                la.append(lx)
            if ly:
                la.append(ly)
            if lz:
                la.append(lz)
            if lc:
                la.append(lc)

            ####Falls SchadenObjekt nur modellübergreifende AOIs enthält -> Annahme: Vertikale Mitte des Bauteils:    
            if not lx and not ly and not lz:
                la.append("Z_Mitte")

            lb = [list(x) for x in numpy.array(numpy.meshgrid(*la)).T.reshape(-1,len(la))]
            AOI.aoi_instance(lb,filename,bt_filename,aoi_filename,schadenObjekt,GlobalId,BauteilTyp)


        # Fall 2: SchadenObjekt enthält keine Information zur AOI
        else:

            b = selector.parse(model, ".IfcBuildingElementProxy[GlobalId *= \""+GlobalId+"\"] | .IfcWall[GlobalId *= \""+GlobalId+"\"] | .IfcColumn[GlobalId *= \""+GlobalId+"\"] | .IfcSlab[GlobalId *= \""+GlobalId+"\"] | .IfcBeam[GlobalId *= \""+GlobalId+"\"] | .IfcStairFlight[GlobalId *= \""+GlobalId+"\"] | .IfcRailing[GlobalId *= \""+GlobalId+"\"]")[0]
            bbox = Bnd_Box()
            shape = ifcopenshell.geom.create_shape(settings, b).geometry
            brepbndlib_Add(shape, bbox)
            xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
            corner1 = gp_Pnt(xmin, ymin, zmin)
            corner2 = gp_Pnt(xmax, ymax, zmax)
            box = BRepPrimAPI_MakeBox(corner1, corner2)
            height_box = abs(zmax-zmin)
            AOI.place_aoi(box,height_box,aoi_filename,schadenObjekt[32:],BauteilTyp) 