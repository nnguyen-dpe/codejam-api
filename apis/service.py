import os
import boto3
import uuid
import logging
import math
from datetime import datetime
from apis.exceptions import ApiError

log = logging.getLogger(__name__)

class DeveloperService(object):

    def __init__(self):
        offline = os.environ.get('IS_OFFLINE')
        if offline:
            self.client = boto3.client(
                'dynamodb',
                region_name='localhost',
                endpoint_url='http://localhost:8000'
            )
        else:
            self.client = boto3.client('dynamodb')
        self.table_name = os.environ['DEVELOPERS_TABLE']
    
    def search(self, args):
        page = args.get('page')
        pageSize = args.get('pageSize')
        sort = args.get('sort')
        name = args.get('name')
        team = args.get('team')
        skills = args.get('skills')

        # get all
        resp = self.client.scan(
            TableName=self.table_name
        )
            
        # map
        foundItems = resp.get('Items')
        items = []
        for it in foundItems:
            items.append(self.__mapOne(it))

        # filter
        filterRsp = self.__filter(items, name, team, skills)

        # sort
        sortRsp = self.__sort(filterRsp, sort)

        # paginated
        return self.__paginated(sortRsp, page, pageSize)

    def __paginated(self, lst, page, pageSize):
        totalRecords = len(lst)
        start = (page - 1) * pageSize
        upper = start + pageSize
        return {
            'totalRecords': totalRecords,
            'page': page, 
            'totalPages': math.ceil(totalRecords / pageSize),
            'records': lst[start:upper]
        }
    
    def __sort(self, lst, sort):
        if sort:
            sortPair = sort.split(',')
            for pair in sortPair:
                kv = pair.split(':')
                reverse = False
                if kv[1] == 'desc':
                    reverse = True                    
                lst = sorted(
                    lst, key=lambda dev: dev[kv[0]], reverse=reverse)
        return lst

    def __filter(self, lst, name, team, skills):
        byName = []
        if name:
            for it in lst:
                if it['name'] == name:
                    byName.append(it)
        else:
            byName = lst
            
        byTeam = []
        if team:
            for it in byName:
                if it['team'] == team:
                    byTeam.append(it)
        else:
            byTeam = byName

        bySkills = []
        if skills:
            listSkills = skills.split(',')
            for s in listSkills:
                for it in byTeam:
                    if it['skills'].count(s) >= 1:
                        found = False
                        for ex in bySkills:
                            if ex['id'] == it['id']:
                                found = True
                        if found == False:
                            bySkills.append(it)
        else:
            bySkills = byTeam
        
        return bySkills


    def getOne(self, id):
        resp = self.client.get_item(
            TableName=self.table_name,
            Key={
                'id': { 'S': id }
            }
        )
        
        item = resp.get('Item')
        if not item:
            return None
       
        return self.__mapOne(item)

    def __mapOne(self, item):
        return {
            'id': item.get('id').get('S'),
            'name': item.get('name').get('S'),
            'team': item.get('team').get('S'),
            'skills': self.__deserialiseSkills(item.get('skills').get('S'))
        }
    
    def __serialiseSkills(self, skills):
        if skills and len(skills) >= 1:
            return ','.join(skills)
        return ''
    
    def __deserialiseSkills(self, str):
        return str.split(',')

    def create(self, data):
        id = str(uuid.uuid4())
        
        self.client.put_item(
            TableName=self.table_name,
            Item={
                'id': { 'S': id },
                'name': { 'S': data.get('name') },
                'team': { 'S': data.get('team') },
                'skills': { 
                    'S': self.__serialiseSkills(data.get('skills'))
                },
                'created_at': { 'S': datetime.now().isoformat() }
            }
        )

        return self.getOne(id)

    def update(self, id, data):
        pass
    
    def delete(self, id):
        pass


_srv = DeveloperService()
