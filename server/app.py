#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Research, Author, ResearchAuthor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
migrate = Migrate(app, db)
db.init_app(app)

api = Api( app )

class Researches( Resource ):

    def get( self ):
        r_list = []
        for r in Research.query.all():
            r_dict = {
                'id': r.id,
                'topic': r.topic,
                'year': r.year,
                'page count': r.page_count
            }
            r_list.append( r_dict )
        return make_response( r_list, 200 )

api.add_resource( Researches, '/research' )


class ResearchesById( Resource ):
    def get( self, id ):
        r_instance = Research.query.filter_by( id = id ).first()
        if r_instance == None:
            return make_response( { 'error': 'research not found' }, 404 )
        return make_response( r_instance.to_dict(), 200 )

    def delete( self, id ):
        r_instance = Research.query.filter_by( id = id ).first()
        if r_instance == None:
            return make_response( { 'error': 'research not found' }, 404 )

        # The "for" loop which would replace cascade = 'all, delete-orphan'
        # in the Model.

        # for ra in r_instance.research_authors:
        #     db.session.delete( ra )
        #     db.session.commit()
        
        db.session.delete( r_instance )
        db.session.commit()
        return make_response( "MEOWZER!", 204 )

api.add_resource( ResearchesById, '/research/<int:id>')

class Authors( Resource ):
    def get( self ):
        a_list = [ a.to_dict() for a in Author.query.all() ]
        return make_response( a_list, 200 ) 

api.add_resource( Authors, '/authors' )


class ResearchAuthors( Resource ):
    def post( self ):
        data = request.get_json()
        ra = ResearchAuthor( author_id = data['author_id'], 
                             research_id = data['research_id'] )
        db.session.add( ra )
        db.session.commit()
        return make_response( ra.author.to_dict(), 201 )

api.add_resource( ResearchAuthors, '/research_author' )



@app.route('/')
def index():
    return '<h1>Code challenge</h1>'



if __name__ == '__main__':
    app.run(port=5555, debug=True)
