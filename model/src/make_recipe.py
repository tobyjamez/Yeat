import nltk
import re
import random
import pickle

DO_NOT_REPLACE = ["cook",
                  "rub",
                  "information",
                  "nutritional",
                  "heat",
                  "point",
                  "end",
                  "peel",
                  "warm",
                  "fry",
                  "oven",
                  "leave",
                  "hand",
                  "pan",
                  "ingredient",
                  "line",
                  "pinch",
                  "crush",
                  "plastic",
                  "freezer",
                  "spoonful",
                  "sheet",
                  "discard",
                  "spread",
                  "fridge",
                  "refrigerator",
                  "second",
                  "cube",
                  "smooth",
                  "sear",
                  "seasoning",
                  "bowl",
                  "plate",
                  "saucepan",
                  "skillet",
                  "hob",
                  "fork",
                  "knife",
                  "boil",
                  "dish",
                  "cut",
                  "strip",
                  "slice",
                  "chop",
                  "bake",
                  "whisk",
                  "processor",
                  "foil",
                  "stir",
                  "rolls",
                  "roll",
                  "dollop",
                  "teaspoon",
                  "spoon",
                  "tablespoon",
                  "ground",
                  "brown",
                  "minute",
                  "cover",
                  "sit",
                  "beat",
                  "rest",
                  "uncover",
                  "cover",
                  "remove",
                  "sieve",
                  "mill",
                  "mix",
                  "place",
                  "tender",
                  "add",
                  "surface",
                  "container",
                  "freeze",
                  "drizzle",
                  "pour",
                  "center",
                  "centre",
                  "combine",
                  "stock",
                  "place",
                  "coat",
                  "cooking",
                  "spray",
                  "melt",
                  "frying",
                  "wok",
                  "color",
                  "colour",
                  "quart",
                  "return",
                  "broiler",
                  "barbecue",
                  "tin",
                  "pot",
                  "pat",
                  "boiling",
                  "flame",
                  "temperature",
                  "degree",
                  "flake",
                  "bottom",
                  "drying",
                  "use",
                  "drain",
                  "mash",
                  "blender",
                  "process",
                  "garnish",
                  "power",
                  "taste",
                  "time",
                  "one",
                  "pound",
                  "saute",
                  "sauté",
                  "toss",
                  "stir",
                  "shake",
                  "do",
                  "order",
                  "squeeze",
                  "mixture",
                  "strain",
                  "shoot",
                  "hour",
                  "quarter",
                  "close",
                  "lid",
                  "sprinkle",
                  "grind",
                  "circle",
                  "tb",
                  "fold",
                  "continue",
                  "blending",
                  "store",
                  "drop",
                  "yellow",
                  "green",
                  "red",
                  "blue",
                  "black",
                  "white",
                  "beat",
                  "tsp",
                  "⅛",
                  "scoop",
                  "day",
                  "serving",
                  "broil",
                  "inch",
                  "inches",
                  "side",
                  "glass",
                  "board",
                  "simmer",
                  "dishes",
                  "insert",
                  "grill",
                  "medium",
                  "blend",
                  "briefly",
                  "fill",
                  "dry",
                  "dries",
                  "shape",
                  "metal",
                  "wire",
                  "spatula",
                  "repeat",
                  "transfer",
                  "bring",
                  "well",
                  "slide",
                  "recipe",
                  "cool",
                  "half",
                  "ball",
                  "cup",
                  "mug",
                  "serve"]

DO_NOT_REPLACE.extend([word + "s" for word in DO_NOT_REPLACE])

def _clean_string(string):
    string = re.sub(r"(\w*)(\.)(\w*)", lambda m: m.group(1) + ". " + m.group(3), string)
    return string.replace(" .", ".").replace(" ,", ",")


def make_title(ingrediet_list, title_file):
    with open(title_file, 'rb') as f:
        model = pickle.load(f)

    out_string = model.make_sentence()

    random.shuffle(ingredient_list)

    for index, ingredient in enumerate(ingredient_list):
        out_string = _replace_with_word(out_string, ingredient, threshold=len(ingredient_list)/(nouns + ((len(ingredient_list) - index) / 4)))

    return out_string

def make_recipe(ingredient_list, model_file):
    with open(model_file, 'rb') as f:
        model = pickle.load(f)

    out_string = ""

    for ingredient in ingredient_list:
        out_string += model.make_sentence()
        for _ in range(int(random.uniform(0.5, 2))):
            out_string += model.make_sentence()

    out_string = _clean_string(out_string)
    print(out_string)
    nouns = _count_nouns(out_string)
    
    random.shuffle(ingredient_list)

    for index, ingredient in enumerate(ingredient_list):
        out_string = _replace_with_word(out_string, ingredient, threshold=len(ingredient_list)/(nouns + ((len(ingredient_list) - index) / 4)))

    return _clean_string(out_string.replace("__NOTOC__", "").replace("Nutritional information", "").replace(" & amp ; ltref & amp ; gt", ". ").replace("Contributed by", "")).replace("  ", " ")


def _replace_with_word(string, new_word, threshold=0.5):
    string = nltk.word_tokenize(string)
    tags = nltk.pos_tag(string)
    for index, word_meaning in enumerate(tags):
        if word_meaning[1].startswith("NN") and random.random() < threshold and word_meaning[0].lower() not in DO_NOT_REPLACE:
            tags[index] = (new_word, tags[index][1])
    return " ".join([word for word, pos in tags])


def _count_nouns(string):
    string = nltk.word_tokenize(string)
    return sum([1 if pos.startswith("NN") and word.lower() not in DO_NOT_REPLACE else 0 for word, pos in nltk.pos_tag(string)])
