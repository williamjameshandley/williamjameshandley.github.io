#!/usr/bin/env python
from students import students, seniority, levels, co_supervisors
from yattag import Doc, indent
import os

students = list(reversed(sorted(students, key=lambda s: (s.start))))
unique_students = list(dict.fromkeys([student.name for student in students]))
from pandas import DataFrame, to_datetime

df = DataFrame([s.__dict__ for s in students])
df['data'] = students
df.start = df.start.apply(to_datetime)
df.end = df.end.apply(to_datetime)
df.sort_values('start', ascending=False, inplace=True)
group = df.groupby('name').data.apply(list)
df = group.to_frame()
df['start'] = df.data.apply(lambda x: x[0].start)
df['end'] = df.data.apply(lambda x: x[0].end)
df['level'] = df.data.apply(lambda x: x[0].level)
df['seniority'] = df.data.apply(lambda x: min([seniority[xi.level] for xi in x]))
df['present'] = df.data.apply(lambda x: x[0].end is None)

present = df[df.present].sort_values(['seniority','start']) 
past = df[~df.present].sort_values(['seniority','end'], ascending=[True, False])
df

url = r'https://arxiv.org/search/?query=handley%%2C+w%%3B+%s%%2C%s&searchtype=author'

import arxiv
def npapers(name, i):
    query = 'au:Handley_W AND au:%s_%s' % (name, i)
    query = query.replace('-','_')
    search = arxiv.Search(query=query)
    return len(list(search.results()))

html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'students.html')

with open(html_file, 'w') as f:


    for i, df in enumerate([present, past]):
        doc = Doc()

        if i==0:
            with doc.tag('h1'):
                doc.text("Present")
        else:
            with doc.tag('h1'):
                doc.text("Past")

        with doc.tag('table', style="border:none"):
            for dat in df.data.to_list():
                with doc.tag('tr', style="border:none"):

                    with doc.tag('td', style="width:30%;border:none"):
                        if dat[0].image:
                            src = os.path.join('/assets/students/', dat[0].image)
                        elif dat[0].original_image:
                            src = os.path.join('/assets/students/', dat[0].original_image)
                        else:
                            src = "/assets/images/user.png"
                        doc.stag('img', src=src, style="border-radius: 20%")


                    with doc.tag('td', style="border:none;"):
                        name = dat[0].name
                        with doc.tag('p'):
                            with doc.tag('font', size="+2"):
                                doc.text(name)
                        with doc.tag('p'):
                            with doc.tag('ul'):
                                for d in dat:
                                    with doc.tag('li'):
                                        doc.text('%s from %s' % (levels[d.level], d.start.strftime("%b %Y")))
                                        if d.end:
                                            doc.text(' to %s' % d.end.strftime("%b %Y"))
                                        if d.co_supervisors:
                                            with doc.tag('ul'):
                                                with doc.tag('li'):
                                                    text = ', '.join([co_supervisors[cs] for cs in d.co_supervisors])
                                                    doc.asis("co-supervised with %s" % text)

                                arr = name.split(' ')
                                surname = arr[-1]
                                forename = arr[0]
                                n = npapers(surname, forename[0])
                                if n > 0:
                                    with doc.tag('li'):
                                        with doc.tag('a', href=url % (surname, forename[0])):
                                            doc.text("Shared research papers (%i)" % n)
                                if any([d.links is not None for d in dat]):
                                    doc.line('li', 'Links:')
                                    with doc.tag('ul'):
                                        for d in dat:
                                            if d.links is not None:
                                                for l in d.links:
                                                    with doc.tag('li'):
                                                        doc.asis(l)

        f.write(indent(doc.getvalue()))
