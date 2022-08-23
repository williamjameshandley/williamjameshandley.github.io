#!/usr/bin/env python
from collections import Counter
from students import students
import matplotlib.pyplot as plt
import os
import datetime
import numpy as np
grey = '#bbbbbb'
plt.rcParams['axes.edgecolor'] = grey
plt.rcParams['xtick.color'] = grey
plt.rcParams['ytick.color'] = grey
plt.rcParams['ytick.color'] = grey
plt.rcParams['ytick.color'] = grey


students = [s for s in students if s.start < datetime.date.today()]
students = sorted(students, key=lambda s: (s.start, min([(l.start, l.seniority) for l in s.levels])[1]))

colors = {'partiii': 'C1',
          'phd': 'C0',
          'postdoc': 'C2',
          'summer': 'C3',
          'mphil': 'C4'}

fig, ax = plt.subplots()
rects = {}
for i, student in enumerate(students):
    for l in student.levels:
        start = l.start.toordinal()
        if l.end is not None:
            end = l.end.toordinal() 
        else:
            end = datetime.date.today().toordinal()
            
        rect = plt.Rectangle((start, i), end-start, 1, fc=colors[l.key], ec='k') 
        rects[str(l)] = rect
        ax.add_artist(rect)
    ax.annotate(student.name, (student.start.toordinal()-10, i+0.5), va='center', ha='right', color=grey)
        
min_year = min([student.start.year for student in students])
date_labels = [datetime.date(i,1,1) for i in range(min_year+1,datetime.date.today().year+2)]
ax.set_xticks([d.toordinal() for d in date_labels])
ax.set_xticklabels([d.year for d in date_labels])

ax.set_xlim(min([student.start.toordinal() for student in students])-400, datetime.date.today().toordinal())
ax.set_ylim(0,i+1)
ax.set_yticks([])

labels, handles  = np.transpose(list(rects.items()))
ax.legend(handles, labels, labelcolor=grey, framealpha=0.0)

png_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'students.png')

fig.set_size_inches(9,9)
fig.tight_layout()
fig.savefig(png_file, transparent=True)
