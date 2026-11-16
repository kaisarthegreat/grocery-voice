"""Small, explicit English/Hindi/Hinglish grocery vocabulary for Stage 3.

Unknown item names are preserved rather than discarded. Add aliases here as
real recognition examples are collected from everyday use.
"""

GROCERY_ALIASES: dict[str, str] = {
    # Dairy and bakery
    "doodh": "Milk", "दूध": "Milk", "milk": "Milk",
    "dahi": "Curd", "दही": "Curd", "curd": "Curd", "yogurt": "Curd", "yoghurt": "Curd",
    "paneer": "Paneer", "पनीर": "Paneer",
    "makhan": "Butter", "मक्खन": "Butter", "butter": "Butter",
    "bread": "Bread", "ब्रेड": "Bread",
    "anda": "Eggs", "अंडा": "Eggs", "अंडे": "Eggs", "eggs": "Eggs", "egg": "Eggs",
    # Vegetables
    "aloo": "Potatoes", "आलू": "Potatoes", "potato": "Potatoes", "potatoes": "Potatoes",
    "pyaz": "Onions", "प्याज": "Onions", "प्याज़": "Onions", "onion": "Onions", "onions": "Onions",
    "tamatar": "Tomatoes", "टमाटर": "Tomatoes", "tomato": "Tomatoes", "tomatoes": "Tomatoes",
    "gajar": "Carrots", "गाजर": "Carrots", "carrot": "Carrots", "carrots": "Carrots",
    "bhindi": "Okra", "भिंडी": "Okra", "okra": "Okra",
    "gobhi": "Cauliflower", "गोभी": "Cauliflower", "cauliflower": "Cauliflower",
    "baingan": "Eggplant", "बैंगन": "Eggplant", "brinjal": "Eggplant", "eggplant": "Eggplant",
    "shimla mirch": "Capsicum", "शिमला मिर्च": "Capsicum", "capsicum": "Capsicum", "bell pepper": "Capsicum",
    "hari mirch": "Green chillies", "हरी मिर्च": "Green chillies", "green chilli": "Green chillies", "green chillies": "Green chillies",
    "dhania": "Coriander", "धनिया": "Coriander", "coriander": "Coriander", "cilantro": "Coriander",
    "adrak": "Ginger", "अदरक": "Ginger", "ginger": "Ginger",
    "lehsun": "Garlic", "लहसुन": "Garlic", "garlic": "Garlic",
    "nimbu": "Lemons", "नींबू": "Lemons", "lemon": "Lemons", "lemons": "Lemons",
    # Staples
    "chawal": "Rice", "चावल": "Rice", "rice": "Rice",
    "atta": "Wheat flour", "आटा": "Wheat flour", "wheat flour": "Wheat flour",
    "maida": "All-purpose flour", "मैदा": "All-purpose flour", "all purpose flour": "All-purpose flour",
    "dal": "Lentils", "दाल": "Lentils", "lentils": "Lentils",
    "cheeni": "Sugar", "चीनी": "Sugar", "sugar": "Sugar",
    "namak": "Salt", "नमक": "Salt", "salt": "Salt",
    "tel": "Cooking oil", "तेल": "Cooking oil", "oil": "Cooking oil", "cooking oil": "Cooking oil",
    "chai patti": "Tea", "चाय पत्ती": "Tea", "tea": "Tea", "tea leaves": "Tea",
}

NUMBER_WORDS: dict[str, str] = {
    "zero": "0", "one": "1", "a": "1", "an": "1", "two": "2", "three": "3",
    "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
    "half": "1/2", "quarter": "1/4", "aadha": "1/2", " आधा": "1/2", "आधा": "1/2", "आधे": "1/2",
    "pauna": "3/4", "पौना": "3/4", "sawa": "1.25", "सवा": "1.25", "dedh": "1.5", "डेढ़": "1.5", "ढाई": "2.5",
    "ek": "1", "एक": "1", "do": "2", "दो": "2", "teen": "3", "तीन": "3", "char": "4", "चार": "4",
    "paanch": "5", "पांच": "5", "पाँच": "5", "chhe": "6", "छह": "6", "saat": "7", "सात": "7",
    "aath": "8", "आठ": "8", "nau": "9", "नौ": "9", "das": "10", "दस": "10",
}

UNIT_ALIASES: dict[str, str] = {
    "pao": "pao", "पाव": "pao",
    "kg": "kg", "kgs": "kg", "kilo": "kg", "kilos": "kg", "kilogram": "kg", "kilograms": "kg", "किलो": "kg", "किलोग्राम": "kg",
    "g": "g", "gm": "g", "gms": "g", "gram": "g", "grams": "g", "ग्राम": "g",
    "l": "L", "lt": "L", "ltr": "L", "litre": "L", "litres": "L", "liter": "L", "liters": "L", "लीटर": "L",
    "ml": "ml", "millilitre": "ml", "millilitres": "ml", "milliliter": "ml", "milliliters": "ml", "मिलीलीटर": "ml",
    "pc": "pcs", "pcs": "pcs", "piece": "pcs", "pieces": "pcs", "पिस": "pcs", "नग": "pcs",
    "dozen": "dozen", " दर्जन": "dozen", "दर्जन": "dozen",
    "pack": "pack", "packs": "packs", "packet": "pack", "packets": "packs", "पैकेट": "pack",
}
