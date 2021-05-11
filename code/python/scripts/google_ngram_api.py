import io
import json

import requests


class NGramRequest:
    __google_ngram_url_template = "https://books.google.com/ngrams/json?" \
                                  "content={0}&year_start={1}&year_end={2}&corpus={3}&smoothing={4}"
    __search_term_sep = "%2C"

    def __init__(self, content, start_year=1500, end_year=2019, corpus=26, smoothing=3):
        if type(content) == str:
            self.content = [content]
        elif type(content) == list:
            self.content = content
        else:
            raise Exception(f"Invalid input type: {type(content)}")
        self.start_year = start_year
        self.end_year = end_year
        self.corpus = corpus
        self.smoothing = smoothing

    def __format_content(self):
        if len(self.content) > 1:
            phrases = []
            for term in self.content:
                phrases.append(term.strip().replace(" ", "+"))
            content_str = self.__search_term_sep.join(phrases)
            return content_str
        elif len(self.content) == 1:
            return self.content[0].replace(" ", "+")
        else:
            raise Exception("Too few content arguments")

    def __str__(self):
        return self.__google_ngram_url_template.format(self.__format_content(), self.start_year, self.end_year,
                                                       self.corpus, self.smoothing)

    def getJSON(self):
        response = requests.get(self)
        response.raise_for_status()
        results = json.loads(response.text)
        return results