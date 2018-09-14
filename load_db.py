from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from init_db import Author, Base, Book, User

engine = create_engine('sqlite:///authors.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

User1 = User(name="admin", email="admin@localhost", picture="admin.jpg")
session.add(User1)
session.commit()

author1 = Author(user_id=1, name="Jim Butcher")

session.add(author1)
session.commit()

book1 = Book(user_id=1, title="Storm Front", description="Harry Dresden is the best at what he does. Well, technically, he's the only at what he does.",
             author=author1)

session.add(book1)
session.commit()

book2 = Book(user_id=1, title="Fool Moon", description="Business has been slow. Okay, business has been dead. And not even of the undead variety.",
             author=author1)

session.add(book2)
session.commit()

book3 = Book(user_id=1, title="Grave Peril", description="Harry Dresden's faced some pretty terrifying foes during his career. Giant scorpions. Oversexed vampires. Psychotic werewolves.",
             author=author1)

session.add(book3)
session.commit()

book4 = Book(user_id=1, title="Summer Knight", description="Ever since his girlfriend left town to deal with her newly acquired taste for blood, Harry Dresden has been down and out in Chicago.",
             author=author1)

session.add(book4)
session.commit()

author2 = Author(user_id=1, name="Dennis Taylor")

session.add(author2)
session.commit()

book5 = Book(user_id=1, title="We Are Legion (We Are Bob)", description="Bob Johansson has just sold his software company and is looking forward to a life of leisure. ",
             author=author2)

session.add(book5)
session.commit()

book6 = Book(user_id=1, title="For We Are Many", description="Bob and his copies have been spreading out from Earth for 40 years now, looking for habitable planets.",
             author=author2)

session.add(book6)
session.commit()

book7 = Book(user_id=1, title="All These Worlds", description="Being a sentient spaceship really should be more fun. But after spreading out through space for almost a century, Bob and his clones just can't stay out of trouble.",
             author=author2)

session.add(book7)
session.commit()


print "DB Items loaded."
