from fastapi import FastAPI, Request
from xml.dom import minidom
import json


app = FastAPI()

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
    print(epiEntryList)
    for entry in epiEntryList:
        if entry["resource"]["resourceType"] == "Composition":
            compositions += 1
            for extension in entry["resource"]["extension"]:
                if extension["extension"][1]["url"] == "concept":
                    if extension["extension"][1]["valueCodeableReference"]["concept"] != None:
                        for coding in extension["extension"][1]["valueCodeableReference"]["concept"]["coding"]:
                            if coding["code"] in listOfCategoriesToSearch:
                                print("Extension: " + extension["extension"][0]["valueString"] + ":" + coding["code"])
                                categories.append(extension["extension"][0]["valueString"])
    if compositions == 0:
        raise Exception('Bad ePI: no category "Composition" found')
    
    if len(categories) == 0:
        return htmlData
    
    return await annotateHTMLsection(htmlData, categories, "highlight")

@app.get("/pregnancy")
async def welcomeMessage():
    return {"advice": "Welcome to the pregnancy lense!"}

async def annotateHTMLsection(htmlData, categories, enhanceTag):
    # TO-DO: make this function.
    pass
