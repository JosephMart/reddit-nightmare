import os

import praw
import click
from dotenv import load_dotenv

from nightmare import Nightmare
from utils import seed_db, get_all_words

load_dotenv()
nightmare = Nightmare(client_id=os.environ['client_id'],
                      client_secret=os.environ['client_secret'],
                      username=os.environ['username'],
                      password=os.environ['password'],
                      target_user=os.environ['target_user'],
                      user_agent='A reddit users\'s worst nightmare',)


@click.group()
def cli():
    pass


@click.command()
def run():
    need_to_run, comment = nightmare.need_to_run()

    if need_to_run:
        print('running')
        nightmare.run(comment)
        return
    print('does not need to run')


@click.command()
def setup():
    seed_db(nightmare)


@click.command()
def gen_phrase():
    # print(nightmare.gen_reply())
    print(get_all_words(nightmare))


cli.add_command(run)
cli.add_command(setup)
cli.add_command(gen_phrase)

if __name__ == "__main__":
    cli()
