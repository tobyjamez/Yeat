from bs4 import BeautifulSoup
from tqdm import tqdm
import re

from _variables import DATA

def _is_recipe(title: str) -> bool:
    return (not title.startswith("Category") and
            not title.startswith("File") and
            not title.startswith("Special") and
            not title.startswith("Help") and
            not title.startswith("Forum") and
            not title.startswith("Portal") and
            not title.startswith("Board") and
            not title.startswith("Blog") and
            not title.startswith("Recipes Wiki") and
            not title.startswith("Talk") and
            not title.startswith("MediaWiki") and
            not title.startswith("Template") and
            not title.startswith("User") and
            not title.startswith("Thread") and
            not title.startswith("Message"))


def _remove_brackets(match) -> str:
    return match.group(2).split("|")[0]

def _clean_string(text: str, no_equal_split=False):
    text = "".join(text.split("\n\n")[1:-1])
    text = re.sub(r"(\[\[)([\w, \s]+\|*[\w, \s]*)(\]\])",
                  _remove_brackets,
                  text)
    text = re.sub(r"(\[\[)(Image\:.*)(\]\])", "", text)

    text = text.replace(";",
                        "").replace("&amp",
                                    "").replace("nbsp",
                                                "")

    if not no_equal_split:
        text = text.replace("Directions", "").replace("Ingredients",
                                                      "").replace("=", "")

    return text


def prepare(data_source: str,
            outfile: str,
            ) -> None:
    """
    """
    with open(data_source) as datafile:
        soup = BeautifulSoup(datafile.read(), features="html.parser")
        titles = []
        ingredients = []
        methods = []
        recipes_raw = soup.find_all("text")
        for index, title in enumerate(tqdm(soup.find_all("title"),
                                 desc="Reading soup")):
            title = str(title)[7:-8]
            if _is_recipe(title):
                temp_ing = []
                temp_met = []
                titles.append(title)
                method_appended = False
                recipe = _clean_string(str(recipes_raw[index]))
                for line in iter(recipe.splitlines()):
                            
                    if line.startswith("*"):
                        temp_ing.append(line[1:])
                    if line.startswith("#"):
                        temp_met.append(line[1:])
                        method_appended = True

                ingredients.append("\n".join(temp_ing))
                if not method_appended:
                    temp_met = [_clean_string(recipe.split("==")[-1],
                                              no_equal_split=True)]
                methods.append("\n".join(temp_met))

        for index, title in enumerate(tqdm(titles, desc="Writing out")):
            with open(outfile, 'a') as out:
                if titles[index] != "" and ingredients[index] != "" and methods[index] != "":
                    out.write("<recipe>\n")

                    out.write("<title>")
                    out.write(titles[index])
                    out.write("</title>\n")
                    
                    out.write("<ingredients>")
                    out.write(ingredients[index])
                    out.write("</ingredients>\n")

                    out.write("<method>")
                    out.write(methods[index])
                    out.write("</method>\n")

                    out.write("</recipe>")


def xml_to_csv(path: str,
               outpath: str) -> None:
    with open(path) as input_file:
        with open(outpath, 'a') as output_file:
            soup = BeautifulSoup(input_file.read())
            for title in soup.find_all("title"):
                output_file.write("title," + str(title).replace("\n", ".").replace(".,",".").replace(" .", ". ").replace("  ", " ")[7:-8] + "\n")
            for ingredients in soup.find_all("ingredients"):
                output_file.write("ingredients," + str(ingredients).replace("\n", ".").replace("..",".").replace(" .", ". ").replace("  ", " ")[13:-14] + "\n")
            for method in soup.find_all("method"):
                output_file.write("method," + str(method).replace("\n", ".").replace("..",".").replace(" .", ". ").replace("  ", " ")[8:-9] + "\n")
