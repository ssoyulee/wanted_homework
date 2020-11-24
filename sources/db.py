import configparser
from sqlalchemy import create_engine, text, func, distinct, and_
from models import db, Company, CompanyLang
import json

config = configparser.ConfigParser()
config.read('resources/resource.conf')

ps_url = config['DB']['POSTGRES_URL']
engine = create_engine(ps_url)

def open_connection() :
    return engine

def select_company_info(list_company) :
    ''' 조회, 수정, 삭제 결과를 조회해온다. '''
    response = []
    for company in list_company :
        
        company_id = int(company[0])

        list_company_lang = db.session.query(CompanyLang)\
                            .filter(and_(CompanyLang.company_id == company_id, CompanyLang.company_lang_type=='ko'))
        company_ko = list_company_lang[0].company_lang_name
        tag_ko = list_company_lang[0].company_lang_tag

        list_company_lang = db.session.query(CompanyLang)\
                            .filter(and_(CompanyLang.company_id == company_id, CompanyLang.company_lang_type=='en'))
        company_en = list_company_lang[0].company_lang_name
        tag_en = list_company_lang[0].company_lang_tag

        list_company_lang = db.session.query(CompanyLang)\
                            .filter(and_(CompanyLang.company_id == company_id, CompanyLang.company_lang_type=='ja'))
        company_ja = list_company_lang[0].company_lang_name
        tag_ja = list_company_lang[0].company_lang_tag

        result = {
            'company_id' : company_id,
            'company_ko' : company_ko,
            'tag_ko' : tag_ko,
            'company_en' : company_en,
            'tag_en' : tag_en,
            'company_ja' : company_ja,
            'tag_ja' : tag_ja
        }

        response.append(result)

    return response
    
def select_company(search_word) :
    ''' 회사를 검색한다. '''
    list_company = db.session.query(CompanyLang.company_id.distinct())\
                    .filter(CompanyLang.company_lang_name.like('%' + search_word + '%'))

    return select_company_info(list_company)

def select_company_tag(search_word) :
    ''' 회사 태그를 검색한다. '''
    list_company = db.session.query(CompanyLang.company_id.distinct())\
                    .filter(CompanyLang.company_lang_tag.like('%' + search_word + '%'))

    return select_company_info(list_company)

def update_company_tag(company_id, update_tag_lang, update_tag) :
    ''' 회사 태그를 수정한다. '''
    result = db.session.query(CompanyLang)\
            .filter(and_(CompanyLang.company_id==company_id, CompanyLang.company_lang_type==update_tag_lang))
    company = result[0]
   
    company.company_lang_tag = update_tag
    db.session.commit()

    list_company = []
    list_company.append(tuple(str(company.company_id),))

    return select_company_info(list_company)

def delete_company_tag(company_id, company_tag_lang) :
    ''' 회사 태그를 삭제한다. '''
    result = db.session.query(CompanyLang)\
        .filter(and_(CompanyLang.company_id==company_id, CompanyLang.company_lang_type==company_tag_lang))
    company = result[0]
    company.company_lang_tag = ''
    db.session.commit()

    list_company = []
    list_company.append(tuple(str(company.company_id),))

    return select_company_info(list_company)

def init_datebase() :
    ''' 데이터 초기 적재... '''
    with open('../file/wanted_temp_data.csv') as company_data :
        index = 0
        for line in company_data :
            try :
                
                if index > 0 :
                    
                    row = line.rstrip('\n')
                    split_row = row.split(',')

                    company_ko = split_row[0]
                    company_en = split_row[1]
                    company_ja = split_row[2]
                    tag_ko = split_row[3]
                    tag_en = split_row[4]
                    tag_ja = split_row[5]
                    
                    # print(f'company_ko : {company_ko} company_en : {company_en} company_ja : {company_ja}')

                    if company_ko :
                        rep_company_name = company_ko
                    elif company_en :
                        rep_company_name = company_en
                    elif company_ja :
                        rep_company_name = company_en
                    
                    if rep_company_name is None :
                        raise Exception('회사 정보가 존재하지 않습니다.')

                    company = Company(
                        company_id = index,
                        company_rep_name = rep_company_name
                    )

                    company_lang_ko = CompanyLang(
                        company_id = index,
                        company_lang_type = 'ko',
                        company_lang_name = company_ko,
                        company_lang_tag = tag_ko
                    )
                    company_lang_en = CompanyLang(
                        company_id = index,
                        company_lang_type = 'en',
                        company_lang_name = company_en,
                        company_lang_tag = tag_en
                    )
                    company_lang_ja = CompanyLang(
                        company_id = index,
                        company_lang_type = 'ja',
                        company_lang_name = company_ja,
                        company_lang_tag = tag_ja
                    )

                    db.session.add(company)
                    db.session.add(company_lang_ko)
                    db.session.add(company_lang_en)
                    db.session.add(company_lang_ja)
                    db.session.commit()

                index += 1

            except Exception as e :
                print(e)

if __name__ == '__main__' :
    connect = open_connection()
    result = connect.execute(text('select 1'))
    print(result.rowcount)

    init_datebase()
