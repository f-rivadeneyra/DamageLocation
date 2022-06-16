from rdflib import Graph, Literal, Namespace, URIRef, BNode
from rdflib.namespace import OWL, RDF, RDFS, XSD
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.parser import AskQuery
import q_main
import json
import random

def connect(database_name):
    graph = Graph()
    graph.parse(database_name, format = "turtle")
    return graph

def query_tbw(data_filename):
    graph = connect(data_filename)
    tbw_list = []
    query_tbw = prepareQuery("""
        prefix : <http://example.org/sibbw7936662#> 
        prefix aoi: <https://w3id.org/aoi#> 
        prefix asb: <https://w3id.org/asbingowl/core#> 
        prefix asbkey: <https://w3id.org/asbingowl/keys#> 
        prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        SELECT DISTINCT ?Teilbauwerk 
        WHERE{
            ?Teilbauwerk a asb:Teilbauwerk .
        }
        """)
    for i in graph.query(query_tbw):
        tbw_list.append(i[0].partition('#')[-1])
    return tbw_list

def get_bauteildefinition(data_filename):
    graph = connect(data_filename)
    btd_list = []
    query_btd = prepareQuery("""
        prefix : <http://example.org/sibbw7936662#> 
        prefix aoi: <https://w3id.org/aoi#> 
        prefix asb: <https://w3id.org/asbingowl/core#> 
        prefix asbkey: <https://w3id.org/asbingowl/keys#> 
        prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        SELECT DISTINCT ?Bauteildefinition
        WHERE{
            ?Bauteildefinition a asb:ASBING13_BauteilDefinition.
        }
        """)
    for i in graph.query(query_btd):
        btd_list.append(i[0])
    return btd_list

def get_schadenObjekte(data_filename):
    graph = connect(data_filename)
    sO_list = []
    query_sO= prepareQuery("""
        prefix : <http://example.org/sibbw7936662#> 
        prefix aoi: <https://w3id.org/aoi#> 
        prefix asb: <https://w3id.org/asbingowl/core#> 
        prefix asbkey: <https://w3id.org/asbingowl/keys#> 
        prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        SELECT DISTINCT ?schadenObjekte
        WHERE{
            ?schadenObjekte a asb:SchadenObjekt.
        }
        """)
    for i in graph.query(query_sO):
        sO_list.append(i[0])
    return sO_list

def get_schadenObjekte(data_filename):
    graph = connect(data_filename)
    sO_list = []
    query_sO= prepareQuery("""
        prefix : <http://example.org/sibbw7936662#> 
        prefix aoi: <https://w3id.org/aoi#> 
        prefix asb: <https://w3id.org/asbingowl/core#> 
        prefix asbkey: <https://w3id.org/asbingowl/keys#> 
        prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
        prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
        SELECT DISTINCT ?schadenObjekte
        WHERE{
            ?schadenObjekte a asb:SchadenObjekt.
        }
        """)
    for i in graph.query(query_sO):
        sO_list.append(i[0])
    return sO_list


def query_schaden(data_filename,schadenObjekt):
    graph = connect(data_filename)
    schaden_dic = {}
    bauteildefinition_query = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
    SELECT DISTINCT ?bauteildefinition
    WHERE{
        <""" + str(schadenObjekt) + """> a asb:SchadenObjekt .
        <""" + str(schadenObjekt) + """> asb:hatBauteilDefinition ?bauteildefinition

    }
    """)
    for i in graph.query(bauteildefinition_query):
        schaden_dic["Bauteildefinition"] = i[0]

    aoi_query = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
    SELECT DISTINCT ?aoi
    WHERE{

        ?aoi aoi:locatesDamage <""" + str(schadenObjekt) + """>
    }
    """)
    for i in graph.query(aoi_query):
        schaden_dic["AOI"] = i[0]

    return schaden_dic

def query_schaden_btd(data_filename,schadenObjekt):
    graph = connect(data_filename)
    btd = []
    bauteildefinition_query = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
    SELECT DISTINCT ?bauteildefinition
    WHERE{
        <""" + str(schadenObjekt) + """> a asb:SchadenObjekt .
        <""" + str(schadenObjekt) + """> asb:hatBauteilDefinition ?bauteildefinition.

    }
    """)
    for i in graph.query(bauteildefinition_query):
        btd.append(i[0])
    
    return btd

def query_schaden_aoi(data_filename,schadenObjekt):
    graph = connect(data_filename)
    aoi_dic = {}
    aoi_query = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
    SELECT DISTINCT ?aoi
    WHERE{

        ?aoi aoi:locatesDamage <""" + str(schadenObjekt) + """>
    }
    """)
    for i in graph.query(aoi_query):
        aoi_dic["AOI"] = i[0]

    return aoi_dic

def query_bauteildefinition(data_filename,bauteildefinition):
    graph = connect(data_filename)
    dictionary = {}
    list_bauteil = []
    list_bauteilgruppe = []
    list_konstruktionsteil = []
    list_teilbauwerk = []
    list_ortsangabe = []
    list_abst_anz = []
    q1 = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT ?Bauteil 
    WHERE{
        <""" + str(bauteildefinition) + """> a asb:ASBING13_BauteilDefinition .
        <""" + str(bauteildefinition) + """> asb:ASBING13_Bauteil ?Bauteil.
    }
    """)
    for i in graph.query(q1):
        list_bauteil.append(i[0])

    q2 = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT  ?Bauteilgruppe
    WHERE{
        <""" + str(bauteildefinition) + """> a asb:ASBING13_BauteilDefinition .
        <""" + str(bauteildefinition) + """> asb:ASBING13_Bauteilgruppe ?Bauteilgruppe.
    }
    """)
    for i in graph.query(q2):
        list_bauteilgruppe.append(i[0])

    q3 = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT ?Konstruktionsteil 
    WHERE{
        <""" + str(bauteildefinition) + """> a asb:ASBING13_BauteilDefinition .
        <""" + str(bauteildefinition) + """>asb:ASBING13_Konstruktionsteil ?Konstruktionsteil.
    }
    """)
    for i in graph.query(q3):
        list_konstruktionsteil.append(i[0])  

    q4 = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT  ?Teilbauwerk
    WHERE{
        <""" + str(bauteildefinition) + """> a asb:ASBING13_BauteilDefinition .
        <""" + str(bauteildefinition) + """> asb:associatedWith ?Teilbauwerk .
    }
    """)
    q5 = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT  ?Ortsangabe
    WHERE{
        <""" + str(bauteildefinition) + """> a asb:ASBING13_BauteilDefinition .
        <""" + str(bauteildefinition) + """> asb:Schaden_Ortsangabe [asb:Ortsangabe_Ortsangabe ?Ortsangabe].
    }
    """)
    for i in graph.query(q5):
        list_ortsangabe.append(str(i[0]))     
    q6 = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT  ?Abstand_Anzahl
    WHERE{
        <""" + str(bauteildefinition) + """> a asb:ASBING13_BauteilDefinition .
        <""" + str(bauteildefinition) + """> asb:Schaden_Ortsangabe [asb:Ortsangabe_GroesseOrtsangabe [asb:AbstandAnzahl_Anzahl ?Abstand_Anzahl]] .
    }
    """)
    for i in graph.query(q6):
        list_abst_anz.append(str(i[0]))    
    j= 0
    while True:       
        if j == len(list_bauteil):
                break
        for i in list_bauteil:
            dictionary["Bauteil_0"] = list_bauteil[0]
            if list_bauteil[j]==list_bauteil[j-1]:
                continue
            else:
                dictionary["Bauteil_"+str(j)] = i
        j = j + 1
    j = 0
    while True:       
        if j == len(list_bauteilgruppe):
                break
        for i in list_bauteilgruppe:
            dictionary["Bauteilgruppe_0"] = list_bauteilgruppe[0]
            if list_bauteilgruppe[j]==list_bauteilgruppe[j-1]:
                continue
            else:
                dictionary["Bauteilgruppe_"+str(j)] = i
        j = j + 1
    j = 0
    while True:       
        if j == len(list_konstruktionsteil):
                break
        for i in list_konstruktionsteil:
            dictionary["Konstruktionsteil_0"] = list_konstruktionsteil[0]
            if list_konstruktionsteil[j]==list_konstruktionsteil[j-1]:
                continue
            else:
                dictionary["Konstruktionsteil_"+str(j)] = i
        j = j + 1
    j = 0
    while True:       
        if j == len(list_teilbauwerk):
                break
        for i in list_teilbauwerk:
            dictionary["Teilbauwerk_0"] = list_teilbauwerk[0]
            if list_teilbauwerk[j]==list_teilbauwerk[j-1]:
                continue
            else:
                dictionary["Teilbauwerk_"+str(j)] = i
        j = j + 1
    j = 0
    while True:       
        if j == len(list_ortsangabe):
                break
        for i in list_ortsangabe:
            dictionary["Ortsangabe_"+str(j)] = i
            j = j+1  
    j = 0
    while True:       
        if j == len(list_abst_anz):
                break
        for i in list_abst_anz:
            dictionary["Abstand_Anzahl_0"] = list_abst_anz[0]
            if list_abst_anz[j]==list_abst_anz[j-1]:
                continue
            else:
                dictionary["Abstand_Anzahl_"+str(j)] = i
        j = j + 1     
    return dictionary

def query_bauteildefinition_hasModelRepresentation(data_filename,bauteildefinition):
    graph = connect(data_filename)
    list_guid = []
    q1 = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT ?MR
    WHERE{
        <""" + str(bauteildefinition) + """> a asb:ASBING13_BauteilDefinition .
        <""" + str(bauteildefinition) + """> asb:hasModelRepresentation ?MR.
    }
    """)
    for i in graph.query(q1):
        list_guid.append(str(i[0]))
    
    return list_guid

def query_bauteildefinition_bauteilTyp(data_filename,bauteildefinition):
    graph = connect(data_filename)
    BauteilTyp = "Proxy"
    q1 = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT ?BT_Typ
    WHERE{
        <""" + str(bauteildefinition) + """> a asb:ASBING13_BauteilDefinition .
        <""" + str(bauteildefinition) + """> asb:BauteilTyp ?BT_Typ.
    }
    """)
    for i in graph.query(q1):
        BauteilTyp = i[0]    
    return BauteilTyp

def query_aoi(data_filename,aoi):
    graph = connect(data_filename)
    aoi_list = []
    query_aoi = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
    SELECT DISTINCT ?aoi 
    WHERE{
        <""" + aoi + """> a ?aoi .
    }
    """)
    for i in graph.query(query_aoi):
        aoi_list.append(i[0])
    return aoi_list

def add_hasModelRepresentation(data_filename,bauteilId,bauteildefinition):
    g = Graph()
    g.parse(data_filename)
    asb =Namespace("https://w3id.org/asbingowl/core#")
    inst =Namespace("https://asbingowl.org/TwinGenDemo/BW452#")
    g.bind("inst",inst)
    g.bind("asb",asb)
    bauteildefinition_ref  = URIRef(bauteildefinition)
    g.add((bauteildefinition_ref,asb.hasModelRepresentation,(URIRef(bauteilId))))
    g.serialize(destination=data_filename)

def add_BauteilTyp(data_filename,bauteilTyp,bauteildefinition):
    g = Graph()
    g.parse(data_filename)
    asb =Namespace("https://w3id.org/asbingowl/core#")
    g.bind("asb",asb)
    bauteildefinition_ref  = URIRef(bauteildefinition)
    g.add((bauteildefinition_ref,asb.BauteilTyp,Literal(bauteilTyp)))
    g.serialize(destination=data_filename)

def get_Ortsangabe(data_filename,bauteildefinition):
    with open("map_damage_location.json", "r") as file:
        map_damage_location = json.loads(file.read())    
    dictionary_oa = {}
    dictionary_tesBauteil = {}
    dictionary_Feld = {}
    dictionary_links_rechts = {}
    dictionary_anfang_ende = {}
    qbtd = q_main.query_bauteildefinition(data_filename,bauteildefinition)
    count = 0
    if "Abstand_Anzahl" in str(qbtd.keys()):
        for i in qbtd.keys():   
            if "Abstand_Anzahl" in i:
                count = count + 1
        i = 0
        while True:   
            dictionary_oa[str(i)] = qbtd["Abstand_Anzahl_"+str(i)]  
            OA = qbtd["Ortsangabe_"+str(i)]
            OA_map = map_damage_location[OA]
            dictionary_oa[str(i)] = str(dictionary_oa[str(i)])+ str(OA_map) 
            del qbtd["Abstand_Anzahl_"+str(i)]
            del qbtd["Ortsangabe_"+str(i)]
            i = i + 1
            if i == count:
                break
    if "Ortsangabe" and not "Abstand_Anzahl" in str(qbtd.keys()):    
        count_2 = count
        for i in qbtd.keys():
            if "Ortsangabe" in i:
                OA = qbtd["Ortsangabe_"+str(count_2)]
                OA_map = map_damage_location[OA]
                dictionary_oa[str(count_2)] = str(OA_map) 
                count_2 = count_2 + 1            
    j = 0
    for i in list(dictionary_oa):
        if "BauteilVon" in dictionary_oa[i]:
            dictionary_tesBauteil[j] = dictionary_oa[i]
            dictionary_oa.pop(i)
    for i in list(dictionary_oa):
        if "Feld" in dictionary_oa[i]:
            dictionary_Feld[j] = dictionary_oa[i]
            dictionary_oa.pop(i)
    for i in list(dictionary_oa):
        if "Control_EndeDesBauwerks" in dictionary_oa[i]  or  "Control_AnfangDesBauwerks" in dictionary_oa[i]:
            dictionary_anfang_ende[str(j)] = dictionary_oa[i]
            dictionary_oa.pop(i)
    j = 0
    for i in list(dictionary_oa):
        if "Rechts"in dictionary_oa[i]  or "Links" in dictionary_oa[i]:
            dictionary_links_rechts[j] = dictionary_oa[i]
            dictionary_oa.pop(i)
            j = j + 1

    return dictionary_oa, dictionary_tesBauteil, dictionary_Feld, dictionary_links_rechts, dictionary_anfang_ende

def create_AOI(data_filename,schadenObjekt):
    g = Graph()
    g.parse(data_filename)

    INS = Namespace("http://example.org/sibbw7936662#")
    AOI = Namespace("https://w3id.org/aoi#")

    g.bind("", INS)
    g.bind("aoi",  AOI)   

    aoi_ref  = str(random.randint(1000000,9999999))+"_AOI"
    print("New AOI: "+str(aoi_ref))
    g.add((URIRef(INS + aoi_ref),AOI.locatesDamage,URIRef(schadenObjekt)))
    g.serialize(destination=data_filename)

def add_AOI(data_filename,aoi_ref,key,new_aoi):
    g = Graph()
    g.parse(data_filename)

    INS = Namespace("http://example.org/sibbw7936662#")
    ANS = Namespace("https://w3id.org/asbingowl/core#")
    AONS = Namespace("https://w3id.org/asbingowl/keys/2013#")
    ANSK = Namespace("https://w3id.org/asbingowl/keys#")
    AOI = Namespace("https://w3id.org/aoi#")

    map = {"INS":INS,"ANSK": ANSK,"AONS":AONS,"ANS":ANS,"AOI":AOI }

    g.bind("", INS)
    g.bind("owl", OWL)
    g.bind("asb", ANS)
    g.bind("asbkey13",  AONS)
    g.bind("asbkey",  ANSK)
    g.bind("aoi",  AOI)   

    g.add((URIRef(INS + aoi_ref),RDF.type,URIRef(map[key] + new_aoi)))
    g.serialize(destination=data_filename)

def query_instance(lbd_filename,GlobalId):
    graph = connect(lbd_filename)
    q1 = prepareQuery("""
    prefix schema: <http://schema.org/> 
    prefix owl: <http://www.w3.org/2002/07/owl#> 
    prefix bot: <https://w3id.org/bot#> 
    prefix ifc: <https://standards.buildingsmart.org/IFC/DEV/IFC4/ADD2/OWL#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    prefix lbd: <https://linkebuildingdata.org/LBD#> 
    prefix props: <http://lbd.arch.rwth-aachen.de/props#> 
    prefix geo: <http://www.opengis.net/ont/geosparql#> 
    prefix unit: <http://qudt.org/vocab/unit/> 
    prefix IFC4-PSD: <https://www.linkedbuildingdata.net/IFC4-PSD#> 
    prefix smls: <https://w3id.org/def/smls-owl#> 
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix inst: <https://asbingowl.org/TwinGenDemo/BW452#> 
    prefix prov: <http://www.w3.org/ns/prov#> 

    SELECT ?globalIdIfcRoot
    WHERE{
        ?globalIdIfcRoot schema:value \"""" + str(GlobalId) + """\"  .        
    }
    """)
    for i in graph.query(q1):
        globalIdIfcRoot = i[0] 
    
    q2 = prepareQuery("""
    prefix schema: <http://schema.org/> 
    prefix owl: <http://www.w3.org/2002/07/owl#> 
    prefix bot: <https://w3id.org/bot#> 
    prefix ifc: <https://standards.buildingsmart.org/IFC/DEV/IFC4/ADD2/OWL#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    prefix lbd: <https://linkebuildingdata.org/LBD#> 
    prefix props: <http://lbd.arch.rwth-aachen.de/props#> 
    prefix geo: <http://www.opengis.net/ont/geosparql#> 
    prefix unit: <http://qudt.org/vocab/unit/> 
    prefix IFC4-PSD: <https://www.linkedbuildingdata.net/IFC4-PSD#> 
    prefix smls: <https://w3id.org/def/smls-owl#> 
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix inst: <https://asbingowl.org/TwinGenDemo/BW452#> 
    prefix prov: <http://www.w3.org/ns/prov#> 

    SELECT ?inst
    WHERE{
        ?inst props:globalIdIfcRoot <""" + str(globalIdIfcRoot) + """> .        
    }
    """)
    for i in graph.query(q2):
        inst = i[0]    
    
    return inst

def get_beschreibtBauteil(data_filename,bauteildefinition):
    graph = connect(data_filename)
    list_beschreibtBauteil = []

    q1 = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT ?beschreibtBauteil 
    WHERE{
        <""" + str(bauteildefinition) + """> a asb:ASBING13_BauteilDefinition .
        <""" + str(bauteildefinition) + """> asb:beschreibtBauteil ?beschreibtBauteil.
    }
    """)
    for i in graph.query(q1):
        list_beschreibtBauteil.append(i[0])

    return list_beschreibtBauteil


def get_associatedWith(data_filename,beschreibtBauteil):
    graph = connect(data_filename)
    list_associatedWith = []

    q1 = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT ?associatedWith 
    WHERE{

        <""" + beschreibtBauteil + """> asb:associatedWith ?associatedWith.
    }
    """)
    for i in graph.query(q1):
        list_associatedWith.append(i[0])

    return list_associatedWith

def get_bauteil(data_filename,associatedWith):
    graph = connect(data_filename)
    list_bauteil = []

    q1 = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT ?bauteil 
    WHERE{
        <""" + associatedWith + """> a ?bauteil .
    }
    """)
    for i in graph.query(q1):
        list_bauteil.append(i[0])

    return list_bauteil

def get_FrzR_Art(data_filename,associatedWith):
    graph = connect(data_filename)
    list_FrzR_Art = []

    q1 = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT ?FrzR_Art 
    WHERE{
        <""" + associatedWith + """> asb:FahrzeugRueckhaltesystem_Art [ asb:ArtFahrzeugRueckhaltesystem_Systembezeichnung [ asb:Systembezeichnung_Bezeichnung  ?FrzR_Art] ] .
    }
    """)
    for i in graph.query(q1):
        list_FrzR_Art.append(i[0])

    return list_FrzR_Art

def get_einfacheBauteilart_Art(data_filename,associatedWith):
    graph = connect(data_filename)
    list_einfacheBt_Art = []

    q1 = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT ?einfacheBt
    WHERE{
        <""" + associatedWith + """> asb:EinfacheBauteilart_Art  ?einfacheBt.
    }
    """)
    for i in graph.query(q1):
        list_einfacheBt_Art.append(i[0])

    return list_einfacheBt_Art

def get_Unterbau_Art(data_filename,beschreibtBauteil):
    graph = connect(data_filename)
    list_Unterbau_Art = []

    q1 = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT ?Unterbau_Art 
    WHERE{
        <""" + beschreibtBauteil + """> asb:Unterbau_Art ?Unterbau_Art .
    }
    """)
    for i in graph.query(q1):
        list_Unterbau_Art.append(i[0])

    return list_Unterbau_Art

def get_ifcBridgeName(data_filename,bauteildefinition):
    beschreibtBauteil = get_beschreibtBauteil(data_filename,bauteildefinition)
    bauteil_list = []
    bauteilTyp_list = []
    for j in beschreibtBauteil:
        associatedWith = get_associatedWith(data_filename,str(j))
        Unterbau_Art = get_Unterbau_Art(data_filename,str(j))
        for k in associatedWith:
            bauteil = get_bauteil(data_filename,str(k))
            bauteil_list.append(str(bauteil))
            try:
                FrzR_Art = get_FrzR_Art(data_filename,str(k))
                bauteil_list.append(str(FrzR_Art))
            except:
                pass
            try:
                einfacheBt_Art = get_einfacheBauteilart_Art(data_filename,str(k))
                bauteil_list.append(str(einfacheBt_Art))
            except:
                pass
        for k in Unterbau_Art:
            bauteil_list.append(str(k))

    for j in bauteil_list:
        if "Bruecke" in str(j) or "Teilbauwerk" in str(j) or "Fahrzeug" in str(j) or "[]" in str(j):
            pass
        elif j not in bauteilTyp_list:
            bauteilTyp_list.append(j)
    return bauteilTyp_list

def get_GlobalId(data_filename,inst):
    graph = connect(data_filename)

    q1 = prepareQuery("""
    prefix schema: <http://schema.org/> 
    prefix owl: <http://www.w3.org/2002/07/owl#> 
    prefix bot: <https://w3id.org/bot#> 
    prefix ifc: <https://standards.buildingsmart.org/IFC/DEV/IFC4/ADD2/OWL#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    prefix lbd: <https://linkebuildingdata.org/LBD#> 
    prefix props: <http://lbd.arch.rwth-aachen.de/props#> 
    prefix geo: <http://www.opengis.net/ont/geosparql#> 
    prefix unit: <http://qudt.org/vocab/unit/> 
    prefix IFC4-PSD: <https://www.linkedbuildingdata.net/IFC4-PSD#> 
    prefix smls: <https://w3id.org/def/smls-owl#> 
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix inst: <https://asbingowl.org/TwinGenDemo/BW452#> 
    prefix prov: <http://www.w3.org/ns/prov#> 

    SELECT ?globalIdIfcRoot
    WHERE{
        <""" + str(inst) + """> props:globalIdIfcRoot ?globalIdIfcRoot.
    }
    """)
    for i in graph.query(q1):
        globalIdIfcRoot=i[0]
    
    
    q2 = prepareQuery("""
    prefix schema: <http://schema.org/> 
    prefix owl: <http://www.w3.org/2002/07/owl#> 
    prefix bot: <https://w3id.org/bot#> 
    prefix ifc: <https://standards.buildingsmart.org/IFC/DEV/IFC4/ADD2/OWL#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    prefix lbd: <https://linkebuildingdata.org/LBD#> 
    prefix props: <http://lbd.arch.rwth-aachen.de/props#> 
    prefix geo: <http://www.opengis.net/ont/geosparql#> 
    prefix unit: <http://qudt.org/vocab/unit/> 
    prefix IFC4-PSD: <https://www.linkedbuildingdata.net/IFC4-PSD#> 
    prefix smls: <https://w3id.org/def/smls-owl#> 
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix inst: <https://asbingowl.org/TwinGenDemo/BW452#> 
    prefix prov: <http://www.w3.org/ns/prov#> 

    SELECT ?globalId
    WHERE{
        <""" + str(globalIdIfcRoot) + """> schema:value ?globalId.
    }
    """)
    for i in graph.query(q2):
        globalId = i[0]

    return globalId
