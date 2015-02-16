import math
import sys
inStr = open(sys.argv[-2]).read()
solutionFile = open(sys.argv[-1])
lines = inStr.split('\n')
del lines[-1]
print lines
names = [line.split()[0] for line in lines]
nameToNum = dict(zip(names, range(len(names))))

fields = ["name", "ServingSize", "Calories", "CaloriesFromFat", "TotalFat", "TotalFatPercent", "SaturatedFat", "SaturatedFatPercent", "TransFat", "TransFatPercent", "Cholesterol", "CholesterolPercent", "Sodium", "SodiumPercent", "TotalCarbs", "TotalCarbsPercent", "DietaryFiber", "DietaryFiberPercent", "Sugars", "SugarsPercent", "Protein", "VitaminA", "VitaminC", "Calcium", "Iron", "isFruitVeg", "isDairy", "isCereal", "isMeat", "Price"]

foodValues = {}

def f(x):
    if x.startswith("-"):
        return "0"
    else:
        return x
for line in lines:
    values = dict(zip(fields, line.split()))
    name = values["name"]
    id = nameToNum[name]
    foodValues[id] = {}
    foodValues[id]["name"] = name
    del values["name"]
    for i in values.keys():
        foodValues[id][i] = float(f(values[i]))
        
solutionPairs = []
for line in solutionFile.read().split('\n'):
    sLine = line.split()
    solutionPairs.append((int(sLine[0]), float(sLine[1])))

score = 1000
calories = 0
caloriesFromFat = 0
proteins = 0
dietaryFiber = 0
fruitPortions = 0
dairyPortions = 0
cerealPortions = 0
meatPortions = 0
transFat = 0
saturatedFat = 0

fields2 = [x for x in fields if x != "name"]

totals = dict(zip(fields2, [0 for i in range(len(fields2))]))

for p in solutionPairs:
    for f in fields2:
        totals[f] += p[1] * foodValues[p[0]][f]

print totals
score -= abs(totals["Calories"] - 2000)
if totals["CaloriesFromFat"]/totals["Calories"]*100 > 25:
    score -= 5 *float(totals["CaloriesFromFat"])/totals["Calories"] - 25
score -= 2 * abs(totals["Protein"] - 100)
score -= 3 * abs(totals["DietaryFiber"] - 20)
"isFruitVeg", "isDairy", "isCereal", "isMeat"
if totals["isFruitVeg"] < 6:
    score -= 50*abs(6-totals["isFruitVeg"])
elif totals["isFruitVeg"] > 6:
    score -= 20*abs(6-totals["isFruitVeg"])
if totals["isCereal"] < 6:
    score -= 50*abs(6-totals["isCereal"])
elif totals["isCereal"] > 6:
    score -= 20*abs(6-totals["isCereal"])
if totals["isMeat"] < 2:
    score -= 50*abs(2-totals["isMeat"])
elif totals["isMeat"] > 2:
    score -= 20*abs(2-totals["isMeat"])
if totals["isDairy"] < 2:
    score -= 50*abs(2-totals["isDairy"])
elif totals["isDairy"] > 2:
    score -= 20*abs(2-totals["isDairy"])
score -= 2* (totals["TransFat"]+totals["SaturatedFat"])
print "SOLUTION: %s" % map(lambda x: (foodValues[x[0]]["name"],x[1]), solutionPairs)
print "SCORE: %s" % score

"VitaminA", "VitaminC", "Calcium", "Iron"
if not totals["VitaminA"] >= 100:
    print totals["VitaminA"]
    print "BAD: does not satisfy vitamin A"
if not totals["VitaminC"] >= 100:
    print "BAD: does not satisfy vitamin C"
if not totals["Calcium"] >= 100:
    print "BAD: does not satisfy calcium"
if not totals["Iron"] >= 100:
    print "BAD: does not satisfy iron"
if not len(solutionPairs) <= 10:
    print "BAD: too many ingredients!"
if not totals["Price"] <= 1500:
    print "BAD: too expensive!"
print totals["Price"]
