from students import students, seniority
import matplotlib.pyplot as plt
import datetime

students = sorted(students, key=lambda s: (s.start, seniority[s.level]))

colors = {'partiii': 'C0',
          'phd': 'C1',
          'postdoc': 'C2',
          'summer': 'C3',
          'mphil': 'C4'}

fig, ax = plt.subplots()
student_names = [student.name for student in students]
unique_students = list(dict.fromkeys(student_names))

for student in students:
    start = student.start.toordinal()
    if student.end is not None:
        end = student.end.toordinal() 
    else:
        end = datetime.date.today().toordinal()
        
    i = unique_students.index(student.name)
    rect = plt.Rectangle((start, i), end-start, 1, fc=colors[student.level], ec='k') 
    print(rect)
    ax.add_artist(rect)
    ax.annotate(student.name, (start, i+0.5), va='center', ha='left')
    
min_year = min([student.start.year for student in students])
date_labels = [datetime.date(i,1,1) for i in range(min_year+1,datetime.date.today().year+2)]
ax.set_xticks([d.toordinal() for d in date_labels])
ax.set_xticklabels([d.year for d in date_labels])

ax.set_xlim(min([student.start.toordinal() for student in students]), datetime.date.today().toordinal()+300)
ax.set_ylim(0,i+1)
ax.set_yticks([])
fig.tight_layout()
