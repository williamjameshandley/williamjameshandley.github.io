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

yaml_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'students.yaml')

with open(yaml_file) as f:
    students = [Student(**kwargs) for kwargs in yaml.safe_load(f)]

students = sorted(students, key=lambda s: (seniority[s.level], s.start, s.name))

with open(yaml_file, 'w') as f:
    yaml.dump([{k: v for k, v in s.__dict__.items() if v is not None}
               for s in students], 
               f, default_flow_style=False, sort_keys=False)
