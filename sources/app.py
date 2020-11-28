from flask import Flask, request
from flask_restx import Api, Namespace, reqparse, Resource, fields
from models import db
import configparser
from repository import init_datebase, select_company_tag, select_company, update_company_tag, delete_company_tag

app = Flask(__name__)


''' db 설정 '''
config = configparser.ConfigParser()
config.read('resources/resource.conf')

ps_url = config['DB']['POSTGRES_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = ps_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
db.reflect(app=app)
''' db 설정 '''


''' api 설정 '''
api = Api(app, title='wanted api', description='wanted api homework', doc='/wanted/doc')
init_api = Namespace('wanted init', path='/init', description='init api')
#api.add_namespace(init_api)


search_init_api = Namespace('wanted init db', path='/init', description='db init api')

api.add_namespace(search_init_api)

search_all_company_api = Namespace('wanted search_company', path='/search_all_company', description='search_all_company api')

api.add_namespace(search_all_company_api)

search_company_api = Namespace('wanted search_company', path='/search_company', description='search_company api')
search_company_parser = reqparse.RequestParser()
search_company_parser.add_argument('search_word', type=str, default='', help='검색 조건')

api.add_namespace(search_company_api)

search_tag_api = Namespace('wanted search_tag', path='/search_tag', description='search_tag api')
search_tag_parser = reqparse.RequestParser()
search_tag_parser.add_argument('search_word', type=str, default='', help='검색 조건')

api.add_namespace(search_tag_api)

update_tag_api = Namespace('wanted update_tag', path='/update_tag', description='update_tag api')
update_tag_model = update_tag_api.model('update_tag',{
    'update_tag_lang': fields.String(description='ko|en|ja', required=True, example="ko"),
    'update_tag': fields.String(description='수정할 태그명', required=True, example="TAG_A")
})

api.add_namespace(update_tag_api)

delete_tag_api = Namespace('wanted delete_tag', path='/delete_tag', description='delete_tag api')
delete_tag_model = delete_tag_api.model('delete_tag',{
    'delete_tag_lang': fields.String(description='삭제할 태그 lang(ko|en|ja)', required=True, example="ko")
})

api.add_namespace(delete_tag_api)

result_model = api.model('result',{
    'company_id': fields.String(description='ID', required=True, example="1"),
    'company_ko': fields.String(description='회사명(한국어)', required=True, example="원티드"),
    'tag_ko': fields.String(description='테그명(한국어)', required=True, example="TAG_A"),
    'company_en': fields.String(description='회사명(영문)', required=True, example="WANTED"),
    'tag_en': fields.String(description='테그명(영문)', required=True, example="TAG_A"),
    'company_ja': fields.String(description='회사명(일본어)', required=True, example="WANTED"),
    'tag_ja': fields.String(description='테그명(일본어)', required=True, example="TAG_A")
})

list_result_model = api.model('result_list',{
    'result_cd' : fields.String(description='결과코드', required=True, example="00"),
    'result_msg' : fields.String(description='결과값', required=True, example="SUCCESS"),
    'result_list' : fields.List(fields.Nested(result_model))
})
''' api 설정 '''


@search_init_api.route('', methods=['GET'])
class InitDatabase(Resource) :
    @search_init_api.response(200, 'Success',list_result_model)
    @search_init_api.response(400, 'Bad Request')
    
    def get(self) :
        
        response = {}
        try :
            init_datebase()
            result_list = select_company(search_word='')

            response['result_cd'] = '00'
            response['result_msg'] = 'SUCCESS'
            response['result_list'] = result_list

        except Exception as e :
            response['result_cd'] = '99'
            response['result_msg'] = '데이터가 이미 들어가 있습니다.'

        return response

@search_all_company_api.route('',methods=['GET'])
class SearchAllCompany(Resource) :
    ''' 회사를 검색하는 API ''' 
    @search_all_company_api.response(200, 'Success',list_result_model)
    @search_all_company_api.response(400, 'Bad Request')
    
    def get(self) :

        response = {}
        try :
            result_list = select_company(search_word='')

            response['result_cd'] = '00'
            response['result_msg'] = 'SUCCESS'
            response['result_list'] = result_list

        except Exception as e :
            response['result_cd'] = '99'
            response['result_msg'] = str(e)

        return response

@search_company_api.route('',methods=['GET'])
class SearchCompany(Resource) :
    ''' 회사를 검색하는 API ''' 
    @search_company_api.expect(search_company_parser)
    @search_company_api.response(200, 'Success',list_result_model)
    @search_company_api.response(400, 'Bad Request')
    
    def get(self) :

        response = {}
        try :
            search_word = request.args.get('search_word')
            result_list = select_company(search_word=search_word)

            response['result_cd'] = '00'
            response['result_msg'] = 'SUCCESS'
            response['result_list'] = result_list

        except Exception as e :
            response['result_cd'] = '99'
            response['result_msg'] = str(e)

        return response

@search_tag_api.route('', methods=['GET'])
class SearchTag(Resource) :
    ''' 태그를 검색하는 API ''' 
    @search_tag_api.expect(search_tag_parser)
    @search_tag_api.response(200, 'Success',list_result_model)
    @search_tag_api.response(400, 'Bad Request')
    
    def get(self) :

        response = {}
        try :
            search_word = request.args.get('search_word')
            result_list = select_company_tag(search_word=search_word)

            response['result_cd'] = '00'
            response['result_msg'] = 'SUCCESS'
            response['result_list'] = result_list

        except Exception as e :
            response['result_cd'] = '99'
            response['result_msg'] = str(e)

        return response


@update_tag_api.route('/<int:company_id>', methods=['PUT'])
@update_tag_api.doc(params={'company_id': 'company_id'})
class UpdateTag(Resource) :
    ''' 태그를 추가/수정하는 API ''' 
    @update_tag_api.expect(update_tag_model)
    @update_tag_api.response(200, 'Success', list_result_model)
    @update_tag_api.response(400, 'Bad Request')
    
    def put(self, company_id) :
        
        response = {}
        try :

            body = request.get_json()
            update_tag_lang = body['update_tag_lang']
            update_tag = body['update_tag']

            result_list = update_company_tag(company_id, update_tag_lang, update_tag)

            response['result_cd'] = '00'
            response['result_msg'] = 'SUCCESS'
            response['result_list'] = result_list

        except Exception as e :
            response['result_cd'] = '99'
            response['result_msg'] = str(e)

        return response

@delete_tag_api.route('/<int:company_id>/<string:company_tag_lang>', methods=['DELETE'])
@delete_tag_api.doc(params={'company_id': 'company_id'})
@delete_tag_api.doc(params={'company_tag_lang': 'company_tag_lang'})
class DeleteTag(Resource) :
    ''' 태그를 삭제하는 API ''' 
    @delete_tag_api.expect(delete_tag_model)
    @delete_tag_api.response(200, 'Success')
    @delete_tag_api.response(400, 'Bad Request')
    
    def delete(self, company_id, company_tag_lang) :
        
        response = {}
        try :

            result_list = delete_company_tag(company_id, company_tag_lang)

            response['result_cd'] = '00'
            response['result_msg'] = 'SUCCESS'
            response['result_list'] = result_list

        except Exception as e :
            response['result_cd'] = '99'
            response['result_msg'] = str(e)

        return response

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port='5000', debug=True)
