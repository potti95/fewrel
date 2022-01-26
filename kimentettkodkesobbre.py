
for k in data['P177']:
    string=""
    for i in k['tokens']:
        if i == " ":
            continue
        string+=i+" "
    mondatok.append(string)


for k in data['P177']:
    for i in k['h']:
      heads.append(i)
      break

for k in data['P177']:
    for i in k['t']:
        tails.append(i)
        break





category = ["P177"]
mondat=[]
head=[]
tail=[]
headposition=[]
tailposition=[]

#kéne külső set for ciklussal iterálható p177
#Egy lépésben tudjuk csinálni 
#positions.append(data["P177"][0]["h"][2][0])
#print(positions[0])  #összes pozicio
#print(positions[0][0]) #elso pozicio
for i in category:
    for k in data[i]:
        string=""
        for j in k['tokens']:
            if j == " ":
                continue
            string+=j+" "
        mondat.append(string)
        head.append(k['h'][0])
        headposition.append(k['h'][2][0])
        tail.append(k['t'][0])
        tailposition.append(k['t'][2][0])






    splittedmondat=mondat.split(" ")
    keresettszo=splittedmondat[int]
    index = mondat.index(keresettszo)
    print("index: ")
    print(index)
    return index