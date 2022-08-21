#!/usr/bin/env python
from students import students, seniority
from yattag import Doc, indent
import os

students = list(reversed(sorted(students, key=lambda s: (s.start))))
unique_students = list(dict.fromkeys([student.name for student in students]))
from pandas import DataFrame, to_datetime

remap = {'postdoc': 'Post-Doc',
         'phd': 'PhD student',
         'mphil': 'MPhil student',
         'partiii': 'Part III student',
         'summer': 'Summer student'}

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


for i, df in enumerate([present, past]):
    if i==0:
        print('\n\n# Present students & postdocs\n\n')
    else:
        print('\n\n# Past students & postdocs\n\n')

    doc, tag, text, line = Doc().ttl()

    with tag('table'):
        for dat in df.data.to_list():
            with tag('tr'):
                with tag('td', style="width:50%"):
                    text(dat[0].name)
                    with tag('ul'):
                        for d in dat:
                            txt = '%s: %s --' % (remap[d.level], d.start)
                            if d.end:
                                txt += '%s' % d.end
                            line('li', txt)

                with tag('td', style="width:50%"):
                    if dat[0].original_image:
                        src = os.path.join('/assets/students/',
                                           dat[0].original_image)
                        doc.stag('img', src=src)


    print(indent(doc.getvalue()))
