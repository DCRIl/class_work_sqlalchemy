from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('city_from', required=True)


parser_jobs = reqparse.RequestParser()
parser_jobs.add_argument('team_leader', required=True)
parser_jobs.add_argument('job', required=True)
parser_jobs.add_argument('work_size', required=True)
parser_jobs.add_argument('content', required=True)
parser_jobs.add_argument('collaborators', required=True)
parser_jobs.add_argument('is_finished', required=True)
parser_jobs.add_argument('categories', required=True)