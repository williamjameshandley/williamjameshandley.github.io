import datetime
import yaml
import os

class Student(object):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        self.level = kwargs.pop('level')
        self.start = kwargs.pop('start')
        self.end = kwargs.pop('end', None)
        self.email = kwargs.pop('email', None)
        self.original_image = kwargs.pop('original_image', None)
        self.image = kwargs.pop('image', None)
        self.co_supervisors = kwargs.pop('co_supervisors', None)

    def __repr__(self):
        string = self.name
        string += ' (%s)' % self.level
        if self.email is not None:
            string += ' <%s>' % self.email
        string += ': %s --' % self.start
        if self.end is not None:
            string += ' %s' % self.end
        return string

seniority = {'postdoc': 0, 'phd': 1, 'mphil': 2, 'partiii': 3, 'summer':4}

levels = {'postdoc': 'Post-Doc',
          'phd': 'PhD student',
          'mphil': 'MPhil student',
          'partiii': 'Part III student',
          'summer': 'Summer student'}

co_supervisors = {'AL': ("Anthony Lasenby", "https://www.phy.cam.ac.uk/directory/lasenbya"),
                  'MH': ("Mike Hobson", "https://www.phy.cam.ac.uk/directory/hobsonm"),
                  'EA': ("Eloy de Lera Acedo", "https://www.phy.cam.ac.uk/directory/dr-eloy-de-lera-acedo"),
                  'AF': ("Anastasia Fialkov", "https://www.ast.cam.ac.uk/people/Anastasia.Fialkov"),
                  'NR': ("Nima Razavi-Ghods", "https://www.phy.cam.ac.uk/staff/dr-nima-razavi-ghods"),
                  'MA': ("Mark Ashdown", "https://www.phy.cam.ac.uk/staff/dr-mark-ashdown"),
                  'KG': ("Keith Grainge", "https://www.research.manchester.ac.uk/portal/keith.grainge.html"),
                  'MO': ("Malak Olamaie", "https://www.yorksj.ac.uk/our-staff/staff-profiles/malak-olamaie.php"),
                  }

yaml_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'students.yaml')

with open(yaml_file) as f:
    students = [Student(**kwargs) for kwargs in yaml.safe_load(f)]

students = sorted(students, key=lambda s: (seniority[s.level], s.start, s.name))

with open(yaml_file, 'w') as f:
    yaml.dump([{k: v for k, v in s.__dict__.items() if v is not None}
               for s in students], 
               f, default_flow_style=False, sort_keys=False)
