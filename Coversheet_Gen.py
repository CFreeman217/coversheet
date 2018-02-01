# github repository: https://github.com/CFreeman217/coversheet.git

import csv
import calendar
import docx
# The built-in comma-separated-value library is useful
# for parsing data files.


ref_word_doc = docx.Document('pyCoverSheet.docx')

class Umkc_course:
    '''
    Represents an instance of the UMKC Class that I am taking this semester.
    '''
    def __init__(self, prefix, c_num, c_title, instructor, sem, year, count):
        self.prefix = prefix
        self.course_number = c_num
        self.title = c_title
        self.professor = instructor
        self.semester = sem
        self.year = year
        self.count = count
    @property
    def printname(self):
        return '{} {} : {}'.format(self.prefix, self.course_number, self.title)

    @property
    def savestring(self):
        return '{},{},{},{},{},{},{}\n'.format(self.prefix, 
                                                self.course_number, 
                                                self.title, 
                                                self.professor, 
                                                self.semester, 
                                                self.year, 
                                                self.count)
    def addfile(self, filename):
        with open(filename, 'a') as savefile:
            savefile.write(self.savestring)

def user_courseinput(in_num):
    pfx = input('Enter Prefix [ME] : ')
    if pfx == '':
        pfx = 'ME' 
    n_course = input('Enter Course Number [{}]: '.format(in_num))
    if n_course == '':
        n_course = str(in_num)
    t_course = input('Enter Course Title : ').title()
    i_course = input('Enter Instructor Name :').title()
    s_course = input('Enter Semester [(f)/s]: ').title()
    if s_course == '':
        s_course = 'Fall'
    y_course = input('Enter Year (2018) : ')
    if y_course == '':
        y_course = '2018'
    c_course = 0
    coursedict[n_course] = Umkc_course(pfx, n_course, t_course, i_course, s_course, y_course, c_course)
    coursedict[n_course].addfile('savefile.csv')

def display_courseload():
    print('\nCurrently Loaded Courses : \n')
    for courseno in coursedict.keys():
        print('{} : {}'.format(courseno, coursedict[courseno].printname))
 
# Function parses tab delimited file information
# fileName must be within the current working directory
def readFile(fileName):
    c_dict = {}
    # Using a 'with' statement is safer than
    # needing to remember to close the file afer reading
    with open(fileName) as file:
        # Delimiter is the character separating the values
        reader = csv.reader(file)
        # Generates a list of the stored information
        data = list(reader)
    # Returns the list of data gathered from the file
    
    for entry in data:
        c_dict[entry[1]] = Umkc_course(entry[0], 
                                            entry[1], 
                                            entry[2], 
                                            entry[3], 
                                            entry[4], 
                                            entry[5], 
                                            entry[6])
    return c_dict

def stripDate(in_str):
    month = int(in_str[:2])
    day = int(in_str[2:4])
    year = int('20' + in_str[4:])
    return '{} {} {}'.format(day, calendar.month_name[month], year)


coursedict = readFile('savefile.csv')


display_courseload()
c_select = input('Generate Homework Coversheet for class : ')
if c_select not in coursedict.keys():
    new = input('New Course Number Detected...\n\tCreate New Entry? [(y)/n] : ')
    if new == '' or new.lower() == 'y':
        user_courseinput(c_select)
a_num = input('Assignment Number ({}) : '.format(coursedict[c_select].count))
if a_num == '':
    a_num = coursedict[c_select].count
while True:
    ddate = input('Enter Due Date [MMDDYY] : ')
    if ddate.isdigit() and len(ddate) == 6:
        due_date = stripDate(ddate)
        break
    print('Enter Date in the form : MMDDYY')      

line_1 = coursedict[c_select].printname
line_2 = '{} - {} {}'.format(coursedict[c_select].professor,
                            coursedict[c_select].semester,
                            coursedict[c_select].year)
line_3 = 'Homework Assignment No. {}'.format(a_num)
line_4 = due_date




ref_word_doc.add_paragraph(line_1, 'Subtitle')
ref_word_doc.add_paragraph(line_2, 'Subtitle')
ref_word_doc.add_paragraph(line_3, 'Subtitle')
ref_word_doc.add_paragraph(line_4, 'Subtitle')
ref_word_doc.save('ME{}_HW{}_coversheet_{}.docx'.format(c_select, a_num, ddate))