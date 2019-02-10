import praw
import sqlite3
import pandas as pd

from praw.models import Comment
from typing import Tuple


class Nightmare:
    def __init__(self, **kwargs):
        self.target_user = kwargs.get('target_user', 'tristan957')
        self._reddit = praw.Reddit(**kwargs)
        self._reddit_user = self._reddit.redditor(self.target_user)
        self._setup_db()

    def message(self, subject: str, msg: str):
        """Message the target user"""
        self._reddit_user.message(subject, msg)

    def get_latest_comment(self) -> Comment:
        """Return the users latest comment"""
        return self._reddit_user.comments.new(limit=1).next()

    def need_to_run(self) -> Tuple[bool, Comment]:
        """Determine if the latest comment needs to be nightmared"""
        latest_comment = self.get_latest_comment()
        return not self.has_been_nightmared(latest_comment), latest_comment

    def has_been_nightmared(self, comment: Comment) -> bool:
        self._cursor.execute(
            'select COUNT(*) from nightmare_comments where comment_id = ?;', (comment.id,))
        return self._cursor.fetchone()[0] > 0

    def run(self, comment: Comment):
        """Nightmare the given comment"""
        comment.reply(self._gen_reply(comment))
        comment.downvote()

    def _gen_reply(self, comment: Comment):
        """Generate a reply based on the comment"""
        # TODO: actually generate based on body and subreddit of comment
        return 'Great insight!'

    def _setup_db(self, setup=False):
        """Initialize the DB if first time and open cursor"""
        self.db_name = f'{self.target_user}.sql'
        self._con = sqlite3.connect(self.db_name)
        self._cursor = self._con.cursor()

        if setup:
            self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS nightmare_comments
            (
                id INTEGER
                    constraint nightmare_comments_pk
                        primary key autoincrement,
                comment_id varchar,
                modified_date datetime default CURRENT_TIMESTAMP
            );

            create unique index nightmare_comments_comment_id_uindex
                on nightmare_comments (comment_id);
            ''')
