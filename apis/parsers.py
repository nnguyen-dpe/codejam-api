from flask_restplus import reqparse

_get_devs_req = reqparse.RequestParser()

_get_devs_req.add_argument(
    name='name', type=str, required=False, location='args',
    help='Filter by the developer\'s name')

_get_devs_req.add_argument(
    name='team', type=str, required=False, location='args',
    help='Filter by the developer\'s assigned team')

_get_devs_req.add_argument(
    name='skills', type=str, required=False, location='args',
    help="""
Filter by the developer's skills. Provide multiple skills separated
by comma.""")

_get_devs_req.add_argument(
    name='page', type=int, required=False, default=1, location='args',
    help='The page number requested, starting from 1')

_get_devs_req.add_argument(
    name='pageSize', type=int, required=False, default=10, location='args',
    help='The number of records per page')

_get_devs_req.add_argument(
    name='sort', type=str, required=False, default='name:asc,team:asc', 
    location='args',
    help="""
Sort the results by the given field(s) and direction in format
`<field name>:(asc|desc),...`, e.g. `field1:asc,field2:desc`
    """)

_post_dev_req = reqparse.RequestParser()
_post_dev_req.add_argument(
    'name', type=str, required=True, location='json', help='Name is required'
)
