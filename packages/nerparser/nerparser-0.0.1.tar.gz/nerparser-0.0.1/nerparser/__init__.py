import spacy

nlp = spacy.blank("en")
nlp_model = spacy.load('nlp_model')

#fonctions pour faire l extraction des informations personelles (nom ,adresse mail et numero de telephone)
import glob, os
import sys, fitz

def extract_with_ner(path):
    os.chdir(path)
    for file in glob.glob("*.pdf"):
        print('\n',file)
        doc = fitz.open(file)
        text = ""
        for page in doc:
            text = text + str(page.getText())
            tx = " ".join(text.split('\n'))
            doc = nlp_model(tx)
            for ent in doc.ents:
                print(f'{ent.label_.upper():{30}}- {ent.text}')