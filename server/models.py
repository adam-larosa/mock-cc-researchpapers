from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy( metadata = metadata)

#           research -----< research_author >----- author


class ResearchAuthor( db.Model, SerializerMixin ):
    __tablename__ = 'research_authors' 
    id = db.Column( db.Integer, primary_key = True )
    author_id = db.Column( db.Integer, db.ForeignKey( 'authors.id' ) )
    research_id = db.Column( db.Integer, db.ForeignKey( 'researches.id' ) )


class Research( db.Model, SerializerMixin ):
    __tablename__ = 'researches'

    serialize_rules = ( '-research_authors', 'authors' )

    id = db.Column( db.Integer, primary_key = True )
    topic = db.Column( db.String )
    year = db.Column( db.Integer )
    page_count = db.Column( db.Integer )

    research_authors = db.relationship( 'ResearchAuthor', backref = 'research',
                                        cascade = 'all, delete-orphan' )
    authors = association_proxy( 'research_authors', 'author' )

    @validates( 'year' )
    def validate_year( self, key, year_integer ):
        if len( str( year_integer ) ) != 4:
            raise ValueError( 'year must be four digits' )
        return year_integer



class Author( db.Model, SerializerMixin ):
    __tablename__ = 'authors'

    serialize_rules = ( '-research_authors', )

    id = db.Column( db.Integer, primary_key = True )
    name = db.Column( db.String )
    field_of_study = db.Column( db.String )

    research_authors = db.relationship( 'ResearchAuthor', backref = 'author' )
    researches = association_proxy( 'research_authors', 'research' )

    @validates( 'field_of_study' )
    def validate_study( self, key, field_string ):
        fields = [ 'AI', 'Robotics', 'Machine Learning', 'Vision', 
                   'Cybersecurity' ]
        if field_string not in fields:
            raise ValueError( 'study something different!!!' )
        return field_string