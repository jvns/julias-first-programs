import sys
inStr = file(sys.argv[-1]).read()
lines = [x for x in inStr.split('\n') if len(x)>0]
#print lines
names = [line.split()[0] for line in lines]
nameToNum = dict(zip(names, range(len(names))))

fields = ["name", "ServingSize", "Calories", "CaloriesFromFat", "TotalFat", "TotalFatPercent", "SaturatedFat", "SaturatedFatPercent", "TransFat", "TransFatPercent", "Cholesterol", "CholesterolPercent", "Sodium", "SodiumPercent", "TotalCarbs", "TotalCarbsPercent", "DietaryFiber", "DietaryFiberPercent", "Sugars", "SugarsPercent", "Protein", "VitaminA", "VitaminC", "Calcium", "Iron", "isFruitVeg", "isDairy", "isCereal", "isMeat", "Price"]


output = ""

def f(x):
    if x.startswith("-"):
        return "0"
    else:
        return x

for line in lines:
    values = dict(zip(fields, line.split()))
    name = values["name"]
    id = nameToNum[name]
    del values["name"]
    for i in values.keys():
        output += "%s %s %s\n" % (id, i, f(values[i]))
print output
