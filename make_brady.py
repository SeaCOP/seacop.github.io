#!/usr/bin/env python
from itertools import chain
from csv import DictWriter
from requests import get

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from io import BytesIO

brady_url = 'https://cdn.muckrock.com/foia_files/2021/09/23/4.7_Potential_Brady_List_8.17.2021.pdf'
with get(brady_url) as response:
    fd = BytesIO(response.content)
    parser = PDFParser(fd)
    document = PDFDocument(parser)
    r = PDFResourceManager()
    device = PDFPageAggregator(r, laparams=LAParams())
    interpreter = PDFPageInterpreter(r, device)

    layouts = []
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for l in layout:
            if isinstance(l, LTTextBox) or isinstance(l, LTTextLine):
                layouts.append(l)

    names = [i.strip()
             for i in chain(*[l.get_text().split('\n')
			      for l in layouts if 70 < l.x0 < 80 ])
             if i and not i in {'Hinderer, Cheryl ', 'Name ', ' '}]

    badges = [i.strip() for i in chain(*[l.get_text().split('\n')
                                         for l in layouts if 270 < l.x0 < 350 ])
	      if i and not i in {'(NEW) ',
                                 '09864 ',
                                 '(OLD) ',
                                 'Fingerprint Tenprint ',
                                 'Supervisor ',
                                 'Badge No. '}]

    agency = [i.strip()
	      for i in chain(*[l.get_text().split('\n')
			       for l in layouts if 400.800 < l.x0 < 500 ])
	      if i and not i in {'Agency ', 'FBI ', 'Security Guard '}]

fieldnames = ["name",
	      "badge",
	      "agency"]
rows = [dict(zip(fieldnames, [names[i], badges[i],agency[i]]))
        for i in range(len(agency))]

with open('_data/brady_cops.csv', 'w') as fd:
    dw = DictWriter(fd, fieldnames)
    dw.writeheader()
    dw.writerows(rows)
# w = writer(fd)
# w.writerow(row)
