#!/usr/bin/env python

"""

"""

import csv
import xml.etree.ElementTree as ElementTree

import requests

__author__ = "Aamir Hasan"
__version__ = "1.0"
__email__ = "hasanaamir215@gmail.com"

base_url = "https://courses.illinois.edu/cisapp/explorer/schedule/2018/fall.xml"
filename = "data.csv"

file = open(filename, 'a+')
fieldnames = ['course_number', 'course_name', 'start_date', 'end_date', 'section_number', 'type', 'start_time',
              'end_time'
    , 'meeting_days', 'room_number', 'building_name', 'instructors']

writer = csv.DictWriter(file, fieldnames=fieldnames)
writer.writeheader()


def get_data(url):
    req = requests.get(url)
    return ElementTree.fromstring(req.text)


def get_child_hrefs(root, find_arg):
    children_hrefs = list()

    for child in root.findall(find_arg):
        children_hrefs.append(child.get('href'))

    return children_hrefs


def get_attribute(element, attribute):
    try:
        return element.find(attribute).text
    except AttributeError:
        return ""


def get_subject_data(subjects):
    for subject_url in subjects:
        courses = get_child_hrefs(get_data(subject_url), './courses/course')

        for course_url in courses:
            course_data = get_data(course_url)

            class_details = dict()
            class_details['course_number'] = course_data.get('id')

            print('Retrieving details for ', class_details['course_number'], '...', sep="")

            class_details['course_name'] = get_attribute(course_data, 'label')

            sections = get_child_hrefs(course_data, './sections/section')

            for section_url in sections:
                section_data = get_data(section_url)

                class_details['start_date'] = get_attribute(section_data, 'startDate')
                class_details['end_date'] = get_attribute(section_data, 'endDate')
                class_details['section_number'] = get_attribute(section_data, 'sectionNumber')

                meetings = section_data.findall('./meetings/meeting')

                for meeting in meetings:
                    class_details['type'] = get_attribute(meeting, 'type')
                    class_details['start_time'] = get_attribute(meeting, 'start')
                    class_details['end_time'] = get_attribute(meeting, 'end')
                    class_details['meeting_days'] = get_attribute(meeting, 'daysOfTheWeek')
                    class_details['room_number'] = get_attribute(meeting, 'roomNumber')
                    class_details['building_name'] = get_attribute(meeting, 'buildingName')

                    instructors = ""
                    instructors_data = meeting.findall('./instructors/instructor')
                    for instructor in instructors_data:
                        instructors += instructor.text + ";"

                    class_details['instructors'] = instructors

                    writer.writerow(class_details)


get_subject_data(get_child_hrefs(get_data(base_url), './subjects/subject'))
file.close()
