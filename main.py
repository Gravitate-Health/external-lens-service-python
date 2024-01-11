from fastapi import FastAPI, Request
import json
from bs4 import BeautifulSoup, UnicodeDammit
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class DOMResponse(BaseModel):
    htmlString: str

@app.post("/pregnancy")
async def pregnancyLense(request: Request):
    body = await request.json()
    
    htmlData = body["htmlData"]
    epiData = body["epiData"]
    ipsData = body["ipsData"]
    
    # The list of codes to search
    listOfCategoriesToSearch = ["W78", "77386006", "69840006"]

    if ipsData == "" or ipsData == None:
        raise Exception("Failed to load IPS: the LEE is getting a empty IPS")

    ipsData = json.loads(ipsData)

    ipsEntryList = ipsData["entry"]
    epiData = json.loads(epiData)

    for entry in ipsEntryList:
        if entry["resource"]["resourceType"] == "Patient":
            gender = entry["resource"]["gender"]
            if gender != "female":
                return htmlData

    epiEntryList = epiData["entry"]
    compositions = 0
    categories = []
    for entry in epiEntryList:
        if entry["resource"]["resourceType"] == "Composition":
            compositions += 1
            for extension in entry["resource"]["extension"]:
                if extension["extension"][1]["url"] == "concept":
                    if extension["extension"][1]["valueCodeableReference"].get("concept") != None:
                        for coding in extension["extension"][1]["valueCodeableReference"]["concept"]["coding"]:
                            if coding["code"] in listOfCategoriesToSearch:
                                categories.append(extension["extension"][0]["valueString"])
    if compositions == 0:
        raise Exception('Bad ePI: no category "Composition" found')
    
    if len(categories) == 0:
        return htmlData
    
    return annotateHTMLsection(htmlData, categories, "highlight")

@app.get("/pregnancy")
async def welcomeMessage():
    return {"advice": "Welcome to the pregnancy lense!"}

def annotateHTMLsection(htmlData, categories, enhanceTag):
    # Parse the HTML data
    response = htmlData
    htmlDOM = BeautifulSoup(htmlData, "html.parser")
    print(htmlDOM.prettify())
    htmlDOM = annotationProcecess(categories, enhanceTag, htmlDOM, response)
    strDOM = str(htmlDOM)
    item = DOMResponse(htmlString=strDOM)
    jsonCompatibleData = jsonable_encoder(item)
    
    return JSONResponse(content=jsonCompatibleData)
    

def annotationProcecess(categories: list[str], enhanceTag: str, htmlDOM: BeautifulSoup, response: str):
    for category in categories:
        if category in response:
            elements = htmlDOM.find_all(class_=category)
            for element in elements:
                element["class"].append(enhanceTag)
    
    return htmlDOM
