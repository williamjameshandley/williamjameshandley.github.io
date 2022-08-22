#!/usr/bin/env python
from collections import Counter
from students import students, seniority, levels
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
students = sorted(students, key=lambda s: (s.start, seniority[s.level]))

colors = {'partiii': 'C1',
          'phd': 'C0',
          'postdoc': 'C2',
          'summer': 'C3',
          'mphil': 'C4'}

fig, ax = plt.subplots()
student_names = [student.name for student in students]
unique_students = Counter(student_names)

rects = {}

for student in students:
    start = student.start.toordinal()
    if student.end is not None:
        end = student.end.toordinal() 
    else:
        end = datetime.date.today().toordinal()
        
        
    i = list(unique_students).index(student.name)

    rect = plt.Rectangle((start, i), end-start, 1, fc=colors[student.level], ec='k') 
    rects[student.level] = rect
    ax.add_artist(rect)
    if unique_students[student.name]:
        ax.annotate(student.name, (start-10, i+0.5), va='center', ha='right', color=grey)
    unique_students[student.name] = 0
    
min_year = min([student.start.year for student in students])
date_labels = [datetime.date(i,1,1) for i in range(min_year+1,datetime.date.today().year+2)]
ax.set_xticks([d.toordinal() for d in date_labels])
ax.set_xticklabels([d.year for d in date_labels])


ax.set_xlim(min([student.start.toordinal() for student in students])-400, datetime.date.today().toordinal())
ax.set_ylim(0,i+1)
ax.set_yticks([])

handles, labels = np.transpose([(rects[l], levels[l]) for l in levels])
ax.legend(handles, labels, labelcolor=grey, framealpha=0.0)

png_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'students.png')

fig.set_size_inches(9,9)
fig.tight_layout()
fig.savefig(png_file, transparent=True)
