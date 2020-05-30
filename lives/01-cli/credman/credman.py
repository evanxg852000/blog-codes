#!/usr/bin/env python3 

from pathlib import Path
import os.path
import pickledb

import click
from pathlib import Path


class Storage(object):
    def __init__(self, file, s=None):
        if s is None:
            self._db = pickledb.load(file, True)
            self._db.dump()
        else:
            self._db = s

    def create(self, file):
        if os.path.exio(file):
            raise Exception('space already exist')
        db = pickledb.load(file, True)
        return db.dump()

    def set(self, key, value):
        return self._db.set(key, value)

    def get(self, key):
        if not self._db.exists(key):
            raise KeyError(f'The key `{key}` does not exist')
        return self._db.get(key)

    def list(self):
        return [(k, self._db.get(k)) for k in self._db.getall()]
   
    def delete(self, key):
        if not self._db.exists(key):
            raise KeyError(f'The key `{key}` does not exist')
        return self._db.rem(key)




class Config(object):

    def __init__(self):
        self.path = str(Path.home())
        self.space = '_default.cdb'

    def ensure(self):
        try:
            self.path = os.path.join(self.path, '.credman')
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            return True
        except OSError:
            return False

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--path', type=click.Path())
@click.option('--space')
@click.option('--verbose', is_flag=True)
@pass_config
def main(config, path, space, verbose):
    '''A wonderful tool to manage your crdentials'''
    config.verbose = verbose
    if path:
        config.path = path
    if space:
        config.space = space

    if not config.ensure():
        raise '[error] unbale to ensure'

    config.storage = Storage(
        os.path.join(config.path, config.space)
    )

@main.command()
@click.argument('name')
@pass_config
def create(config, name):
    '''Create key space'''
    try:
        file = os.path.join(config.path, f'{name}.cdb')
        config.storage.create(file)
        click.echo(f'👍 [ok] space `{name}` created')
    except Exception as ex:
        details = f'{ex}' if config.verbose else ''
        click.echo(f'💥 [error] creating space `{name}` -{details}')


@main.command()
@pass_config
def list(config):
    '''Lists all entries in key space'''
    try:
        entries = config.storage.list()
        for (k, v) in entries:
            click.echo(f' {k} -> {v}')
    except Exception:
        click.echo(f'💥 [error] listing entries')


@main.command()
@click.argument('key')
@click.argument('value')
@pass_config
def put(config, key, value):
    '''Puts an entry in key space'''
    if not config.storage.set(key, value) :
        click.echo(f'💥 [error] saving {key} -> {value} in {config.space}')
  
@main.command()
@click.argument('key')
@pass_config
def get(config, key):
    '''Gets an entry from key space'''
    try:
        v = config.storage.get(key)
        click.echo(v)
    except Exception:
        click.echo(f'💥 [error] {key} does not exist in {config.space}')


@main.command()
@click.argument('key')
@pass_config
def delete(config, key):
    '''Deletes an entry in key space'''
    try:
        config.storage.delete(key)
    except Exception:
       click.echo(f'💥 [error] {key} does not exist in {config.space}')
