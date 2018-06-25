'''
@author: Santirrium
'''

import re
import unicodedata
import json
import logging

#Set log
logging.basicConfig(
    filename='bot_detector.log', 
    level=logging.INFO, 
    format="%(asctime)s:%(threadName)10s:%(levelname)s: %(message)s", datefmt='%d/%m/%Y %I:%M:%S %p')

# Get configuration from file
def get_config(config_file):
    with open(config_file) as f:
        config = json.loads(f.read())
    return config

def clean_emojis(doc):
    
    emoji_pattern = re.compile("["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+")
    return emoji_pattern.sub(r'', doc)

def deEmojify(inputString):
    returnString = ""
    for character in inputString:
        try:
            character.encode("ascii")
            returnString += character
        except UnicodeEncodeError:
            returnString += ''
    return returnString


def clear(inputString):
    
    #eliminamos los emojis
    returnString = clean_emojis(inputString)
    #eliminamos otros caracteres raros
    returnString = deEmojify(returnString)
    #quitamos los saltos de linea
    returnString = returnString.replace("\r"," ")
    returnString = returnString.replace("\n"," ")
    #returnString = returnString.replace("@","-")
    #returnString = returnString.strip()
    #returnString = returnString.encode(encoding='utf_8', errors='strict')

    return returnString

def getattribute(objeto, name: str):
        """Returns the attribute matching passed name."""
        # Get internal dict value matching name.
        value = objeto.__dict__.get(name)
        if not value:
            # Raise AttributeError if attribute value not found.
            return None
        # Return attribute value.
        return value


if __name__ == "__main__":
    
    test = "Your remote ⚡️social media team. Hire pros who have grown audiences into the millions! https://t.co/YgQja8XiAS"
    
    print(clean_emojis(test))
    print(deEmojify(test))