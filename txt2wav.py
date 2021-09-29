#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# HTTP + URL packages
import re

import httplib2
from urllib.parse import urlencode, quote  # For URL creation
import argparse

# To play wave files
import pygame
import math  # For ceiling

divider: str
i_divider: str

def main():
    GENDERDIVIDE = [r'\*', r':', r'_', r'\-', r'/', r'·', r'\.', r'°', r'\'', r'\|']
    GENDERI = ['I', '!', 'ï']
    #TODO: Regex for special gendering
    # Student(innen)
    # Student(inn)en

    GENDERSYMBOL = ' '
    global divider, i_divider
    parser = argparse.ArgumentParser(description='Read gendered text out loud')
    parser.add_argument("gender_type", help="Gender", choices=['gendered', 'male', 'female'])
    parser.add_argument('text')
    parser.add_argument('-g', nargs='+')
    parser.add_argument('host', nargs='?')
    parser.add_argument('port', nargs='?')

    args = parser.parse_args()
    if args.g:
        GENDERDIVIDE.append(args.g)
    GENDERDIVIDE.extend(GENDERI)
    divider = r'|'.join(GENDERDIVIDE)
    i_divider = r'|'.join(GENDERI)

    def transform_gender(text):
        global divider, i_divider
        divider = r'(?<=[a-zäöüß])(' + divider + r')(?=(in|innen|r|n)(?![a-zäöüß]))'
        i_divider = r'(?<=[a-zäöüß])(' + i_divider + r')(?=(n|nnen)(?![a-zäöüß]))'
        text = re.sub(divider, GENDERSYMBOL, text)
        text = re.sub(i_divider, GENDERSYMBOL + r'i', text)
        return text

    def transform_male(text):
        global divider, i_divider
        divider1 = r'(?<=[a-zäöüß])(' + divider + r')(in|innen)(?![a-zäöüß])'
        nr = r'(?<=[a-zäöüß])(' + divider + r')(?=(r|n)(?![a-zäöüß]))'
        i_divider = r'(?<=[a-zäöüß])(' + i_divider + r')(n|nnen)(?![a-zäöüß])'
        text = re.sub(nr, '', text)
        text = re.sub(divider1, '', text)
        text = re.sub(i_divider, '', text)

        return text

    def transform_female(text):
        global divider, i_divider
        divider1 = r'(?<=[a-zäöüß])(' + divider + r')(?=(in|innen)(?![a-zäöüß]))'
        nr = r'(?<=[a-zäöüß])(' + divider + r')(r|n)(?![a-zäöüß])'
        i_divider = r'(?<=[a-zäöüß])(' + i_divider + r')(n|nnen)(?![a-zäöüß])'
        text = re.sub(divider1, '', text)
        text = re.sub(i_divider, '', text)
        text = re.sub(nr, '', text)
        return text

    if args.gender_type in 'gendered':
        input_text = transform_gender(args.text)
    elif args.gender_type in 'male':
        input_text = transform_male(args.text)
    elif args.gender_type in 'female':
        input_text = transform_female(args.text)
    else:
        input_text = "Mary python client test"

    print("Transformierter Text: ",input_text)

    # Mary server informations
    if args.host:
        mary_host = args.host
    else:
        mary_host = "localhost"
    if args.port:
        mary_port = args.port
    else:
        mary_port = "59125"

    # Build the query
    query_hash = {"INPUT_TEXT": input_text,
                  "INPUT_TYPE": "TEXT",  # Input text
                  "LOCALE": "de",
                  "VOICE": "dfki-pavoque-styles",  # Voice informations  (need to be compatible)
                  "OUTPUT_TYPE": "AUDIO",
                  "AUDIO": "WAVE",  # Audio informations (need both)
                  }
    query = urlencode(query_hash)
    print("query = \"http://%s:%s/process?%s\"" % (mary_host, mary_port, query))

    # Run the query to mary http server
    h_mary = httplib2.Http()
    resp, content = h_mary.request("http://%s:%s/process?" % (mary_host, mary_port), "POST", query)

    #  Decode the wav file or raise an exception if no wav files
    if (resp["content-type"] == "audio/x-wav"):

        # Write the wav file
        f = open("/tmp/output_wav.wav", "wb")
        f.write(content)
        f.close()

        # Play the wav file
        pygame.mixer.init(frequency=16000)  # Initialise the mixer
        s = pygame.mixer.Sound("/tmp/output_wav.wav")
        s.play()
        pygame.time.wait(int(math.ceil(s.get_length() * 1000)))

    else:
        raise Exception(content)


if __name__ == '__main__':
    main()


"Damit es für jede:n Einwohner:in Jenas und des näheren Umlands möglich ist, dass es nicht zu Konflikten zwischen Radfahrer:innen und Fußgänger:innen kommt. Anwohner:innen-Kfz-Verkehr. Kampagnen an Schulen sollten sich gezielt an Lehrer:innen, Schüler:innen und Eltern richten. Jede:r Schüler:in sollte die Möglichkeit haben,"