import urllib2,urllib
import json

# API reference https://canvas.instructure.com/doc/api/submissions.html

BASE_URL = "https://<your_domain>.instructure.com/api/v1%s"
access_token = "<your_access_token>"
course_id = <the_course_id>  # not the sis_id but the canvas internal id

REQUEST_HEADERS = {'Authorization':'Bearer %s' % access_token}

# First, get the list of students in the course

students_endpoint = BASE_URL % '/courses/%d/students' % (course_id)

# Create a request, adding the REQUEST_HEADERS to it for authentication
student_request = urllib2.Request(students_endpoint,None,REQUEST_HEADERS)

# Fetch the response, read it and strip extra whitespace from the beginning and end
student_response = urllib2.urlopen(student_request).read().strip()

# Load the response as JSON
response_data = json.loads(student_response)

# Exit if there were no students in the returned data
if not response_data:
  print 'Sorry, there were no students registered in the course.'
  exit(0)

# Loop through the students, populating the student_ids list with their canvas ids
student_ids = [s['id'] for s in response_data]


# Build the endpoint for requesting submissions
submissions_endpoint = BASE_URL % '/courses/%d/students/submissions' % (course_id)

# Build the GET request parameters that are needed to fetch the submissions along with the
# total scores (grades)
submission_params = [ ('include[]','total_scores'), ('grouped',1) ]
submission_params.extend([('student_ids[]',s) for s in student_ids])

submission_params = urllib.urlencode(submission_params)


# Build a request, adding the REQUEST_HEADERS to it for authentication
req = urllib2.Request(submissions_endpoint + "?" +submission_params,None,{'Authorization':'Bearer %s' % access_token})
# Fetch the response, read it and strip extra whitespace from the beginning and end
grades_response = urllib2.urlopen(req).read().strip()

# Load the response as JSON
grades = json.loads(grades_response)
