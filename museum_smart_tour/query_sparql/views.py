from django.shortcuts import render
from django.http import HttpResponse
from SPARQLWrapper import SPARQLWrapper, RDFXML
from rdflib import Graph
from django.views.decorators.csrf import csrf_exempt
import cv2
from django.views.decorators.csrf import csrf_exempt

def main_html(request):
    return render(request, "main.html")
    # return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def open_camera(request):
    import cv2

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            value = scan_qrcode("opencv_frame_0.png")
            print("value", value)
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()
    
    cv2.destroyAllWindows()

@csrf_exempt
def scan_qrcode(filename):
    print("A")
    try:
        img = cv2.imread(filename)
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        print("B")
        return value
    except:
        print("C")
        return

# open_camera()

def artwork_search(input_string):
    artworkImage=[]
    artworkTitle=[]
    artworkWidth=[]
    artworkHeight=[]
    artworkId=[]
    artistName=[]
    productionYear=[]
    nationality=[]
    site=[]
    room=[]
    museumName=[]
    lifePeriod=[]
    artistDesc=[]
    artistImage=[]
    medium=[]
    sparql = SPARQLWrapper("http://ec2-35-90-181-153.us-west-2.compute.amazonaws.com:3030/#/dataset/tour/query")

    sparql.setQuery("""
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX umt: <http://www.semanticweb.org/artifact#>
    SELECT ?artistName ?title ?artworkID ?productionYear ?dimensions ?description ?classification ?imageUrl ?width ?height ?nationality ?site ?room ?museumName ?lifePeriod ?artistDesc ?artistImageUrl ?medium 
    WHERE {
    ?art rdf:type umt:Artifact;
    umt:isCreatedBy ?art2;
    umt:hasMedium ?medium;
    umt:hasDate ?productionYear;
    umt:hasArtifactID ?artworkID;
    umt:hasDimensions ?dimensions;
    umt:hasDescription ?description;
    umt:hasClassification ?classification;
    umt:hasImage ?imageUrl;
    umt:hasHeight ?height;
    umt:hasWidth ?width;
    umt:hasSite ?site;
    umt:hasRoom ?room;
    umt:hasMuseumName ?museumName.
 
  
    ?art2 rdf:type umt:Artist;
    umt:hasArtistName ?artistName;
    umt:hasNationality ?nationality;
    umt:hasLifeperiod ?lifePeriod;
    umt:hasArtistDescr ?artistDesc;
    umt:hasArtistImage ?artistImageUrl.
    FILTER regex(?title,""" +'"'+input_string+'")'+ """
    }
    LIMIT 1
    """)

    sparql.setReturnFormat(JSON)
    res = sparql.query().convert()

    res_1=res['results']['bindings']

    for r in res_1:
        try:
            artistName.append(r['artistName']['value'])
            artworkWidth.append(r['width']['value'])
            artworkImage.append(r['artworkImage']['value'])
            artworkId.append(r['artworkId']['value'])
            productionYear.append(r['productionYear']['value'])
            nationality.append(r['nationality']['value'])
            site.append(r['site']['value'])
            room.append(r['room']['value'])
            museumName.append(r['museumName']['value'])
            lifePeriod.append(r['lifePeriod']['value'])
            artistDesc.append(r['artistDesc']['value'])
            artistImage.append(r['artistImage']['value'])
            medium.append(r['medium']['value'])
        except:
            pass
    
    return artistName, artworkWidth, artworkImage, artworkId, productionYear, nationality, site, room, museumName, lifePeriod, artistDesc, artistImage, medium 
    
    @csrf_exempt 
    def searchByName(request):
        input_string=""
        if(request.method=='POST'):
            input_string=request.POST['fname']
    
        artistName, artworkWidth, artworkImage, artworkId, productionYear, nationality, site, room, museumName, lifePeriod, artistDesc, artistImage, medium  = artwork_search(keyString)
        return render(request, 'artworkSearch.html', {'artistName': artistName, 'artworkWidth' : artworkWidth, 'artworkImage' : artworkImage, 'artworkId' : artworkId, 'productionYear' : productionYear, 'nationality' : nationality, 'site' : site, 'room' : room, 'museumName' : museumName, 'lifePeriod' : lifePeriod, 'artistDesc' : artistDesc, 'artistImage' : artistImage, 'medium' : medium, 'keystring':keyString})