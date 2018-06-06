import os
import pymongo
import uuid
import logging
import math
from datetime import datetime
from apis.exceptions import ApiError
from pymongo import MongoClient

log = logging.getLogger(__name__)

class DeveloperService(object):

    def __init__(self):
        self.client = MongoClient('mongodb://root:hello@192.168.99.100:31459')
        self.db = self.client.developerdb
        self.developers = self.db.developers
    
    def search(self, args):
        page = args.get('page')
        pageSize = args.get('pageSize')
        sort = args.get('sort')
        name = args.get('name')
        team = args.get('team')
        skills = args.get('skills')

        # get all
        resp = self.developers.find({})
            
        # map
        foundItems = resp
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
        resp = self.developers.find_one({'id': id})
        item = resp
        if not item:
            return None
       
        return self.__mapOne(item)

    def __mapOne(self, item):
        return {
            'id': item['id'],
            'name': item['name'],
            'team': item['team'],
            'skills': self.__deserialiseSkills(item['skills']),
            'pullRequest': item['pull_request']
        }
    
    def __serialiseSkills(self, skills):
        if skills and len(skills) >= 1:
            return ','.join(skills)
        return ''
    
    def __deserialiseSkills(self, str):
        return str.split(',')

    def create(self, data):
        id = str(uuid.uuid4())

        self.developers.insert_one({
                'id': id,
                'name': data.get('name'),
                'team': data.get('team'),
                'skills': self.__serialiseSkills(data.get('skills')),
                'created_at': datetime.now().isoformat()
            }
        )

        return self.getOne(id)

    def update(self, id, data):
        pass
    
    def delete(self, id):
        pass


_srv = DeveloperService()
