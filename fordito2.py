import requests, uuid, json, io


def fordito(mondat):
    # Add your subscription key and endpoint
    subscription_key = "f060c48b82fc46b1b9ff0e234cb4067b"
    endpoint = "https://api.cognitive.microsofttranslator.com"

    # Add your location, also known as region. The default is global.
    # This is required if using a Cognitive Services resource.
    location = "northeurope"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'includeAlignment': 'true',
        'from': 'en',
        'to': ['hu']
    }
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': mondat
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    magyarmondat = response[0]["translations"][0]["text"]
    projekcio = response[0]["translations"][0]["alignment"]["proj"]
    return magyarmondat, projekcio
    #print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))




def findmagyarentity(mondat, headposition, tailposition, magyarmondat, projekcio):
    #eredményül meg kell kapni melyik szavak az entitások head - tail és ezek pozíciói (hanyadik szó)
    #angol szavak és pozícióio
    #lefordítjuk
    #alignment alapján megkeressük melyik szavak mikre fordultak le
    #    meg kell tudni hanyadik karakternél kezdődnek az entitások és meddig tartanak
    #    az alignmentből kiírjuk a párjait
    #    majd megkeressük ezeket a szavakat és a pozíciójukat hanyadikak
    #    visszatérünk a a magyarhead magyartail es poziciokkal

    #head-tail szavainak keresése mondatban
    angolheadstringposition=[]
    angoltailstringposition=[]
    magyarheadstringposition=[]
    magyartailstringposition=[]
    magyarheadposition=[]
    magyartailposition=[]
    magyarhead=[]
    magyartail=[]
    for i in headposition:
        eredmeny=wordindextopositionindex(mondat, i)
        angolheadstringposition.append(eredmeny)
    for i in tailposition:
        eredmeny=wordindextopositionindex(mondat, i)
        angoltailstringposition.append(eredmeny)

    
    #ha megvan alignment alapján a magyar kezdődő karaktereket megkeresni
    projekciosplitted=projekcio.split(" ")
    partitionedstring=[]
   
    for i in projekciosplitted:
        partitionedstring=i.partition('-')
        part2=partitionedstring[0].partition(':')
        jobboldal=partitionedstring[2].partition(':')
        for k in angolheadstringposition:
            if int(part2[0]) == k:
                magyarheadstringposition.append(jobboldal[0])
        for k in angoltailstringposition:
            if int(part2[0]) == k:
                magyartailstringposition.append(jobboldal[0])

    for i in magyarheadstringposition:
        eredmeny=positionindextowordindex(magyarmondat, int(i))
        splittedmagyarmondat=magyarmondat.split(" ")
        magyarhead.append(splittedmagyarmondat[eredmeny])   #magyarhead
        magyarheadposition.append(eredmeny)                 #magyarheadpos
    for i in magyartailstringposition:
        eredmeny=positionindextowordindex(magyarmondat, int(i))
        splittedmagyarmondat=magyarmondat.split(" ")
        magyartail.append(splittedmagyarmondat[eredmeny])   #magyartail
        magyartailposition.append(eredmeny)                 #magyartailposition

    return magyarhead, magyarheadposition, magyartail, magyartailposition


def wordindextopositionindex(mondat, int):
    #megkeresni azt a szót és a hosszát lementeni
    #végigpróbálni a stringen és ha megvan kiírni a kezdőkaraktert és végkaraktert
    szokozokszama=0
    hanyadikkarakter=0
    for i in mondat:
        if szokozokszama==int:
            return hanyadikkarakter
        elif i==" ":
            szokozokszama+=1
            hanyadikkarakter+=1
        else: hanyadikkarakter+=1
    return hanyadikkarakter


def positionindextowordindex(magyarmondat, int):
    szokozokszama=0
    karaktercounter=0
    for i in magyarmondat:
        if karaktercounter==int:
            return szokozokszama
        elif i==" ":
            szokozokszama+=1
            karaktercounter+=1
        else: karaktercounter+=1
    return szokozokszama





f = open ('data/vegleges.json', "r")
data = json.loads(f.read())



category = ["P177", "P364","P2094","P361","P641","P59","P413","P206","P412","P155","P26","P410","P25","P463","P40","P921"]
#category = ["P412","P155","P26","P410","P25","P463","P40","P921"]
#category = ["P463","P40","P921"]
#category = ["P412"]
#category = ["P177"]

#positions.append(data["P177"][0]["h"][2][0])
#print(positions[0])  #összes pozicio
#print(positions[0][0]) #elso pozicio
#string=data["P177"][0]["tokens"]
hanyadikmondat=0
sum=0
for i in category:
    for k in data[i]:
        string=k['tokens']
        head=k['h'][0]
        headposition=k['h'][2][0]
        tail=k['t'][0]
        tailposition=k['t'][2][0]
        eredetiheadposition=headposition
        eredetitailpostition=tailposition

        #fordítás helye
        mondat=""
        hanyadikszo=0
        counter=0
        for j in string:
            if j == " ":
                for n in headposition:
                    if hanyadikszo<n:
                        headposition[counter]=n-1
                    counter+=1
                counter=0
                for n in tailposition:
                    if hanyadikszo<n:
                        tailposition[counter]=n-1
                    counter+=1
                hanyadikszo+=1
                continue
            else : 
                mondat+=j+" "
                hanyadikszo+=1
        #print(headposition)
        #print(tailposition)
        #print(mondat)
        print(hanyadikmondat)
        print(sum)
        print(mondat)
        magyarmondat, projekcio = fordito(mondat) # Assign returned tuple
        #print(magyarmondat)
        #print(projekcio)


        #kalkulációk
        magyarhead, magyarheadposition, magyartail, magyartailposition =findmagyarentity(mondat, headposition, tailposition, magyarmondat, projekcio)
        ##TESZTELNI!!!!!!!!!
        
        #beírás helye
        #magyartoken beír
        #head beír + headposition
        #tail beír + tailposition
        #print(magyarhead)
        #print(magyarheadposition)
        #print(magyartail)
        #print(magyartailposition)
        #print(magyarmondat)
        with open('data/veglegesmagyar.json', "r+", encoding='utf8') as jsonFile:
            data2 = json.load(jsonFile)
            if (not magyarhead) or (not magyarmondat) or (not magyarheadposition) or (not magyartail) or (not magyartailposition) :
                del data2[i][hanyadikmondat]
                jsonFile.seek(0)
                json.dump(data2, jsonFile, ensure_ascii=False)
                jsonFile.truncate()
            else:
                magyarsplittedmondat=magyarmondat.split(" ")
                data2[i][hanyadikmondat]["tokens"]=magyarsplittedmondat
                data2[i][hanyadikmondat]["h"][0]=magyarhead
                data2[i][hanyadikmondat]["h"][2][0]=magyarheadposition
                data2[i][hanyadikmondat]["t"][0]=magyartail
                data2[i][hanyadikmondat]["t"][2][0]=magyartailposition
                ## head-tail pozíciók kellenek még.
                jsonFile.seek(0)
                json.dump(data2, jsonFile, ensure_ascii=False)
                jsonFile.truncate()
                hanyadikmondat+=1
        sum+=1
    hanyadikmondat=0

f.close()





