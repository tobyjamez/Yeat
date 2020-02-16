import markovify
from bs4 import BeautifulSoup
import pickle

def model_to_file(outfile:str)
    with open("../../data/recipes.xml") as f:
        soup = BeautifulSoup(f.read())

    text = "\n".join([str(method)[8:-9] for method in soup.find_all("method")])

    text_model = markovify.Text(text)

    text_model = text_model.compile()

    with open(outfile, 'wb') as outf:
        pickle.dump(text_model, outf)


if __name__ == "__main__":
    model_to_file("model.mkv.pickle")
