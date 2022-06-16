from http.client import PARTIAL_CONTENT
import q_main
import Geom
import Bauteil
import Control
import ifcopenshell
import ifcopenshell.geom 
import ifcopenshell.util
import ifcopenshell.util.element
from ifcopenshell.util.selector import Selector
from ifcopenshell.util import element


def locate_caps(filename,newfile_name,dictionary_rechts_links):
    selector = Selector()
    model = ifcopenshell.open(filename)
    f = ifcopenshell.open(newfile_name)
    rechts_links =dictionary_rechts_links
    a = Geom.elements_in_box(rechts_links,model,f)
    b = []
    element_list = selector.parse(model, '.IfcBeam | .IfcBuildingElementProxy | .IfcWall | .IfcColumn | .IfcSlab')
    for i in element_list:     
        if "EDGEBEAM" in str(element.get_type(i)):
             b.append(i)
    intersection = list(set(a).intersection(b))
    if len(intersection)==1:
        Kappe = intersection[0]
    else:
        dic = {} 
        for i in intersection:
            dic[i] = Geom.bounding_box_center(i).Y()   
        if rechts_links == "Rechts":
            a = sorted(dic.items(), key=lambda x:x[1])
            sorted_a = dict(a)
            Kappe = next(iter(sorted_a.keys()))
        elif rechts_links == "Links":
            a = sorted(dic.items(), key=lambda x:x[1],reverse=True)
            sorted_a = dict(a)
            Kappe = next(iter(sorted_a.keys()))
        else:
            print("Error")
    return Kappe   

def locate_beam(filename,newfile_name,dictionary_bauteilsuche,dictionary_feld):
    selector = Selector()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True) 
    model = ifcopenshell.open(filename)
    f = ifcopenshell.open(newfile_name)
    feld = list(dictionary_feld.values())[0]
    bts =list(dictionary_bauteilsuche.values())[0]
    a = Geom.elements_in_box(feld,model,f)
    #b = selector.parse(model, '.IfcBuildingElementProxy[Name *= "Traeger" ]')
    b = []
    element_list = selector.parse(model, '.IfcBeam | .IfcBuildingElementProxy | .IfcWall | .IfcColumn | .IfcSlab')
    for i in element_list: 
        if "GIRDER_SEGMENT" in str(element.get_type(i)):
             b.append(i)
    intersection = list(set(a).intersection(b))
    dic_traeger = {}
    for key in intersection:
        dic_traeger[key] = (Geom.bounding_box_center(key).Y())
    if "BauteilVonLinks" in bts:
        n = int(bts[0])
        Traeger_von_rechts_nach_links = sorted(dic_traeger.items(), key=lambda x: x[1], reverse=True)
        Traeger = Traeger_von_rechts_nach_links[n-1]
    if "BauteilVonRechts" in bts:
        n = int(bts[0])
        Traeger_von_rechts_nach_links = sorted(dic_traeger.items(), key=lambda x: x[1], reverse=False)
        Traeger = Traeger_von_rechts_nach_links[n-1]
    
    return Traeger

def locate_roadway(filename):
    selector = Selector()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True) 
    model = ifcopenshell.open(filename)
    Fahrbahn = selector.parse(model, '.IfcSlab[Name *= "Landstrasse"]')
    return Fahrbahn

def locate_railing(filename,newfile_name,dictionary_rechts_links):
    selector = Selector()
    model = ifcopenshell.open(filename)
    f = ifcopenshell.open(newfile_name)
    rechts_links =dictionary_rechts_links
    a = Geom.elements_in_box(rechts_links,model,f)
    b = selector.parse(model, '.IfcRailing')
    intersection = list(set(a).intersection(b))
    if len(intersection)==1:
        railing = intersection[0]
    else:
        dic = {} 
        for i in intersection:
            dic[i] = Geom.bounding_box_center(i).Y()   
        if rechts_links == "Rechts":
            a = sorted(dic.items(), key=lambda x:x[1])
            sorted_a = dict(a)
            railing = next(iter(sorted_a.keys()))
        elif rechts_links == "Links":
            a = sorted(dic.items(), key=lambda x:x[1],reverse=True)
            sorted_a = dict(a)
            railing = next(iter(sorted_a.keys()))
        else:
            print("Error")
    return railing         

def locate_abutment(filename,newfile_name,dictionary_oa):
    selector = Selector()
    model = ifcopenshell.open(filename)
    f = ifcopenshell.open(newfile_name)
    print(dictionary_oa)
    if len(dictionary_oa) != 0:  
        a = Geom.elements_in_box(dictionary_oa["0"][8:],model,f)
        b = []
        element_list = selector.parse(model, '.IfcBeam | .IfcBuildingElementProxy | .IfcWall | .IfcColumn | .IfcSlab')
        for i in element_list: 
            if "RETAININGWALL" in str(element.get_type(i)):
                b.append(i)
        intersection = list(set(a).intersection(b))
        Abutment = intersection[0]
        print(Abutment)
    else:
        print("Error")
    return Abutment   

def locate_stair(filename,newfile_name,dictionary_oa):
    selector = Selector()
    model = ifcopenshell.open(filename)
    f = ifcopenshell.open(newfile_name)
    if len(dictionary_oa) != 0:    
        a = Geom.elements_in_box(dictionary_oa["0"][8:],model,f)
        b = selector.parse(model, '.IfcStair')
        intersection = list(set(a).intersection(b))
        Stair = intersection[0]
        print(Stair)
    else:
        print("Error")
    return Stair  

def check_model_representation(bauteildefinition,data_filename,filename,bt_filename,lbd_filename,ifcBridgeName,oa,dictionary_bauteilsuche,dictionary_feld,dictionary_ortsangaben):    
    dictionary_bauteil = {}
    dictionary_bauteil = Bauteil.find_model_representation(bauteildefinition,data_filename,filename,bt_filename,ifcBridgeName,oa,dictionary_bauteilsuche,dictionary_feld,dictionary_ortsangaben)
    bauteile = dictionary_bauteil[bauteildefinition]
    lbd_inst = q_main.query_instance(lbd_filename,bauteile.GlobalId)
    q_main.add_hasModelRepresentation(data_filename,lbd_inst,bauteildefinition)  
    q_main.add_BauteilTyp(data_filename,str(dictionary_bauteil["Bauteil"]),bauteildefinition)  

    return bauteile

def find_model_representation(bauteildefinition,data_filename,filename,bt_filename,ifcBridgeName,oa,dictionary_bauteilsuche,dictionary_feld,dictionary_ortsangaben):    
    bauteile = {}
    query_btd = q_main.query_bauteildefinition(data_filename,bauteildefinition)
    while True: 
        if "EDGEBEAM" in ifcBridgeName:
            bauteile[bauteildefinition] = Bauteil.locate_caps(filename,bt_filename,oa)
            bauteile["Bauteil"] = "EDGEBEAM"
            break
        if "GIRDER_SEGMENT" in ifcBridgeName:
            if len(dictionary_bauteilsuche)>0 and len(dictionary_feld)>0:
                bauteile[bauteildefinition] = Bauteil.locate_beam(filename,bt_filename,dictionary_bauteilsuche,dictionary_feld)[0]
                bauteile["Bauteil"] = "GIRDER_SEGMENT"
            break            
        if "SLAB" in ifcBridgeName:
            bauteile[bauteildefinition] = Bauteil.locate_roadway(filename)[0]
            bauteile["Bauteil"] = "SLAB"
            break
        if "RAILING" in ifcBridgeName:
            bauteile[bauteildefinition] = Bauteil.locate_railing(filename,bt_filename,oa)
            bauteile["Bauteil"] = "RAILING"
            break
        if "RETAININGWALL" in ifcBridgeName and "WiderlagerHinten" in str(query_btd.values()):
            bauteile[bauteildefinition] = Bauteil.locate_abutment(filename,bt_filename,dictionary_ortsangaben)
            bauteile["Bauteil"] = "Widerlager_Wand_Hinten"
            break
        if "RETAININGWALL" in ifcBridgeName and "WiderlagerVorn" in str(query_btd.values()) :
            bauteile[bauteildefinition] = Bauteil.locate_abutment(filename,bt_filename,dictionary_ortsangaben)
            bauteile["Bauteil"] = "Widerlager_Wand_Vorne"
            break
        if "RETAININGWALL" in ifcBridgeName and "Fluegel" in str(query_btd.values()) and "Hinten" in str(query_btd.values()):
            bauteile[bauteildefinition] = Bauteil.locate_abutment(filename,bt_filename,dictionary_ortsangaben)
            bauteile["Bauteil"] = "Fluegel_Wand_Hinten"
            break
        if "RETAININGWALL" in ifcBridgeName and "Fluegel" in str(query_btd.values()) and "Vorn" in str(query_btd.values()):
            bauteile[bauteildefinition] = Bauteil.locate_abutment(filename,bt_filename,dictionary_ortsangaben)
            bauteile["Bauteil"] = "Fluegel_Wand_Vorne"
            break
        if "STAIR" in ifcBridgeName and "beideWid" in str(query_btd.values()):
            bauteile[bauteildefinition] = Bauteil.locate_stair(filename,bt_filename,dictionary_ortsangaben)
            bauteile["Bauteil"] = "Widerlager_Wand_Vorne"
            break
        else:
            print("No Bauteil found for Bauteildefinition" )
            break
    return bauteile