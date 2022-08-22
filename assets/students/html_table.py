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
df['seniority'] = df.level.apply(lambda x: seniority[x])
df['present'] = df.data.apply(lambda x: x[0].end is None)

present = df[df.present].sort_values(['seniority','start']) 
past = df[~df.present].sort_values(['seniority','end'], ascending=[True, False])

url = r'https://arxiv.org/search/?query=handley%%2C+w%%3B+%s%%2C%s&searchtype=author'

import arxiv
def npapers(name, i):
    query = 'au:handley_w AND au:%s_%s' % (name, i)
    search = arxiv.Search(query=query)
    return len(list(search.results()))



for i, df in enumerate([present, past]):
    if i==0:
        print('\n\n# Present students & postdocs\n\n')
    else:
        print('\n\n# Past students & postdocs\n\n')

    doc, tag, text, line = Doc().ttl()

    with tag('table'):
        for dat in df.data.to_list():
            with tag('tr'):
                with tag('td'):
                    name = dat[0].name
                    text(name)
                    with tag('ul'):
                        for d in dat:
                            with tag('li'):
                                text('%s: %s to ' % (levels[d.level], d.start.strftime("%b %Y")))
                                if d.end:
                                    text('%s' % d.end.strftime("%b %Y"))
                                else:
                                    text('present')
                                if d.co_supervisors:
                                    text(" (co-supervised by ")
                                    for i, cs in enumerate(d.co_supervisors):
                                        c, u= co_supervisors[cs]
                                        line('a', c, href=u)
                                        if i != len(d.co_supervisors)-1:
                                            text(", ")
                                    text(")")
                        arr = name.split(' ')
                        surname = arr[-1]
                        forename = arr[0]
                        n = npapers(surname, forename[0])
                        if n > 0:
                            with tag('li'):
                                with tag('a', href=url % (surname, forename[0])):
                                    text("Research papers (%i)" % n)


                with tag('td', style="width:30%"):
                    if dat[0].original_image:
                        src = os.path.join('/assets/students/', dat[0].original_image)
                    else:
                        src = "/assets/images/user.png"
                    doc.stag('img', src=src)


    print(indent(doc.getvalue()))
