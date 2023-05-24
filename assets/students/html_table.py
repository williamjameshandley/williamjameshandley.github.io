#!/usr/bin/env python
from students import students, levels
from yattag import Doc, indent
import os
from pandas import DataFrame, to_datetime
df = DataFrame()
df['data'] = students
df['level'] = df.data.apply(lambda x: min(x.levels).key)
df['present'] =  df.data.apply(lambda x: x.end()==None) 

html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'students.html')

css = """
.grid{
  display: grid;
  gap: 1rem;
  grid-template-colums: repeat(1, 1fr);
  grid-template-columns: 100%;
}

.grid-item img {
   border-radius: 20%;
   width: 200px;
}

@media screen and (min-width: 600px){
   .grid{
      grid-template-colums: repeat(2, 1fr);
      grid-template-columns: 30% 70%;
   }
}
"""

ignore = ["George Carter", "Toby Lovick", "Stephen Pickman"]

with open(html_file, 'w') as f:
    doc = Doc()

    with doc.tag('style'):
        doc.asis(css)

    for i, df in enumerate([df[df.present], df[~df.present]]):
        for level in levels:
            sdf = df[df.level==level].data.to_list()
            if len(sdf):

                with doc.tag('div', klass='wrapper', style='margin-top:30pt'):
                    with doc.tag('h1'):
                        if i==0:
                            doc.text('%ss' % levels[level].string)
                        else:
                            doc.text('Past %ss' % levels[level].string)
                    with doc.tag('div', klass="grid"):
                        for student in sdf:
                            if student.name in ignore:
                                continue
                            with doc.tag('div', klass="grid-item"):
                                if student.image:
                                    src = os.path.join('/assets/students/', student.image)
                                elif student.original_image:
                                    src = os.path.join('/assets/students/', student.original_image)
                                else:
                                    src = "/assets/images/user.png"
                                doc.stag('img', src=src)

                            with doc.tag('div', klass="grid-item"):
                                name = student.name
                                with doc.tag('p'):
                                    with doc.tag('font', size="+2"):
                                        doc.text(name)
                                with doc.tag('p'):
                                    with doc.tag('ul'):
                                        for l in student.levels:
                                            with doc.tag('li'):
                                                doc.text('%s from %s' % (l, l.start.strftime("%b %Y")))
                                                if l.end:
                                                    doc.text(' to %s' % l.end.strftime("%b %Y"))
                                                if l.supervisors:
                                                    str(l.supervisors[0])
                                                    with doc.tag('ul'):
                                                        with doc.tag('li'):
                                                            text = ', '.join([str(cs) for cs in  l.supervisors])
                                                            doc.asis("co-supervised with %s" % text)

                                        joint_papers = student.joint_papers()
                                        if joint_papers:
                                            with doc.tag('li'):
                                                doc.asis(joint_papers)

                                        if student.links:
                                            doc.line('li', 'Links:')
                                            with doc.tag('ul'):
                                                for l in student.links:
                                                    with doc.tag('li'):
                                                        doc.asis(l)

                                        if student.destination:
                                            doc.line('li', 'Subsequent career:')
                                            with doc.tag('ul'):
                                                for date, loc in student.destination.items():
                                                    with doc.tag('li'):
                                                        doc.asis("%s: %s" % (date.strftime("%b %Y"), loc))

    f.write(indent(doc.getvalue()))
