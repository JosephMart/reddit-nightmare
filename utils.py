import praw

from nightmare import Nightmare
from markov import Markov


def seed_db(nigthmare: Nightmare):
    """Fetch all users comments and store in DB"""
    comments = nigthmare.get_all_comments().new(limit=8)
    count = 0

    for comment in comments:
        nigthmare.add_comment(comment)
        count += 1

    nigthmare.commit()
    print(f"Added {count} comments to DB {nigthmare.db_name}")


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_all_words(nightmare: Nightmare):
    nightmare._cursor.execute('select comments.body from comments;')
    data = nightmare._cursor.fetchall()
    words = ''
    for d in data:
        words += d[0]

    n = 10
    l = words.split()
    c = [l[i:i + n] for i in range(0, len(l), n)]
    print(c)
    m = Markov(c)
    # print(words.split())
    return m.generate_markov_text()
    # return words
