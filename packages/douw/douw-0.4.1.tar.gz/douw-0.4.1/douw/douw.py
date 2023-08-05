#!/usr/bin/env python3.8

import argparse
import time
import datetime
import os
import sys
import subprocess
import fnmatch
import shutil

import sqlite3

from douw.site import Site
from douw.version import __version__

currentTime = str(time.time())

assume_yes = False


def create_root_arg_parser():
    parser = argparse.ArgumentParser(
        description='Manage website deployments'
    )

    parser.add_argument('--basedir', metavar='PATH', default='/srv/www/sites',
                        help='set the directories the sites are stored in')

    parser.add_argument('--force-useless', action='store_true', help='force operations even if they are useless')
    parser.add_argument('--force-dangerous', action='store_true', help='force operations even if they are dangerous')

    parser.add_argument('--assume-defaults', '-y', action='store_true',
                        help='assume defaults instead of prompting, or abort if no sane default can be guessed')

    parser.add_argument('--no-inherit-env', dest='inherit_env', action='store_false',
                        help='do not forward environment variables to hook scripts')
    parser.add_argument('--env', '-e', dest='env_args', metavar='[stage:]key[=value]',
                        action='append',
                        help='define additional environment variables for hook scripts')

    return parser


def create_arg_parser():
    parser = create_root_arg_parser()

    subparsers = parser.add_subparsers(title='action', dest='action', metavar='ACTION')

    create_list_parser(subparsers)
    create_deps_parser(subparsers)
    create_add_parser(subparsers)
    create_edit_parser(subparsers)
    create_deploy_parser(subparsers)
    create_revert_parser(subparsers)
    create_clean_parser(subparsers)
    create_help_parser(parser, subparsers)
    create_remove_parser(subparsers)
    create_var_parser(subparsers)
    create_version_parser(subparsers)

    return parser


def create_list_parser(subparsers):
    list_parser = subparsers.add_parser('list', help='list all known sites')
    list_parser.set_defaults(action=list)

    list_parser.add_argument('--site', metavar='*', default='*', help='a glob-style pattern to filter site names')
    list_parser.add_argument('--remote', metavar='*', default='*', help='a glob-style pattern to filter remote URLs')


def create_deps_parser(subparsers):
    deps_parser = subparsers.add_parser('deployments', help='list all deployments')
    deps_parser.set_defaults(action=deps)

    deps_parser.add_argument('site', metavar='SITE', help='the site to get deployments for')
    deps_parser.add_argument('--deleted', action='store_true', help='Also show deleted deployments')


def create_add_parser(subparsers):
    add_parser = subparsers.add_parser('add', help='add a site',
                                       description='Missing properties are prompted from standard input.')
    add_parser.set_defaults(action=add)

    populate_add_edit_parser(add_parser)


def create_edit_parser(subparsers):
    edit_parser = subparsers.add_parser('edit', help='edit a site', description='modify site properties')
    edit_parser.set_defaults(action=edit)

    edit_parser.add_argument('site', metavar='SITE', help='the site to edit')

    populate_add_edit_parser(edit_parser)


def populate_add_edit_parser(subparser):
    subparser.add_argument('--name', metavar='NAME', help='the name of the site')
    subparser.add_argument('--remote', metavar='URL', help='the repository to pull changes from')
    subparser.add_argument('--branch', metavar='TREE-ISH', help='the branch (or tag or commit) to clone by default')
    subparser.add_argument('--env', metavar='ENV', help='the DTAP environment to deploy as')


def create_deploy_parser(subparsers):
    deploy_parser = subparsers.add_parser('deploy', help='deploy one or more sites')
    deploy_parser.set_defaults(action=deploy)

    deploy_parser.add_argument('site', metavar='SITE', help='the site to deploy')
    deploy_parser.add_argument('treeish', metavar='TREE-ISH', nargs='?', help='the branch, tag, or commit to deploy')

    deploy_parser.add_argument('--revert', action='store_true', help='revert if the revision already exists')
    deploy_parser.add_argument('--copy-from', metavar='PATH', help='copy files locally instead of cloning')


def create_revert_parser(subparsers):
    revertParser = subparsers.add_parser('revert', help='revert to a previous revision')
    revertParser.set_defaults(action=revert)

    revertParser.add_argument('site', metavar='SITE', nargs='?', default=None)
    revertParser.add_argument('rev', metavar='REV', nargs='?', default=None)


def create_clean_parser(subparsers):
    cleanParser = subparsers.add_parser('clean', help='remove old deployments')
    cleanParser.set_defaults(action=clean)

    cleanParser.add_argument('site', metavar='SITE', help='the site to clean')


def create_help_parser(parser, subparsers):
    helpParser = subparsers.add_parser('help', help='show this help message and exit')
    helpParser.add_argument('haction', metavar='ACTION', help='the action to get help for', nargs='?')
    helpParser.set_defaults(action=lambda a:
        (parser if a.haction is None else subparsers.choices[a.haction]).print_help()
    )


def create_remove_parser(subparsers):
    removeParser = subparsers.add_parser('remove', help='remove a site')
    removeParser.set_defaults(action=remove)
    removeParser.add_argument('site', metavar='SITE')


def create_var_parser(subparsers):
    varParser = subparsers.add_parser('var', help='manage variables')
    varParser.set_defaults(action=var)
    varParser.add_argument('site', metavar='SITE', help='the site to manage the variables of')
    varParser.add_argument('var', metavar='NAME[=VALUE]', help='the value to get or set', nargs='?')


def create_version_parser(subparsers):
    version_parser = subparsers.add_parser('version', help='display version information')
    version_parser.set_defaults(action=version)

    version_parser.add_argument('--full', action='store_true', help='also list dependency versions')
    version_parser.add_argument('--no-copyright', action='store_true',
                                help='do not print narcissistic copyright information')


def main():
    parser = create_arg_parser()

    global args
    args = parser.parse_args()

    global assume_yes
    assume_yes = args.assume_defaults

    if args.action is None:
        parser.print_help()
        return

    if not os.path.isdir(args.basedir):
        raise FileNotFoundError(args.basedir)

    args.action(args)


def init_db(db):
    """
    Initializes the given database for use.

    This creates the base schema and applies migrations if necessary.

    :param db: the database to initialize
    """

    db.executescript("""
CREATE TABLE IF NOT EXISTS site (
    name TEXT PRIMARY KEY NOT NULL,
    remote TEXT NOT NULL,
    env TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS deployment (
    id INTEGER PRIMARY KEY NOT NULL,
    path TEXT NOT NULL,
    revision TEXT NOT NULL,
    date INTEGER NOT NULL,
    active INTEGER NOT NULL,
    present INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS variable (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL UNIQUE ON CONFLICT REPLACE,
    value TEXT NOT NULL
)
""")

    db.execute('PRAGMA user_version')
    ver = db.fetchone()[0]

    if ver < 1:
        db.execute('ALTER TABLE site ADD COLUMN default_treeish TEXT')

    db.execute('PRAGMA user_version = 1')


def get_site_db(basedir, name):
    """
    Returns the path to the database for the given site.

    :param basedir: the directory all sites are stored in
    :param name:  the name of the site
    :return: the path to the database
    """
    return os.path.join(basedir, name, 'site.db')


def open_site_db(basedir, name, must_exist=True):
    """
    Opens a connection to a site's database.

    The database is checked for existence and R/W rights if the database is assumed to exist.
    If the database is missing or cannot be modified, an error is raised (if must_exist is True) or the database is
    created and initialized (if must_exist is False).

    Upon successfully opening the database migrations are applied transparently.

    :param basedir: the directory all sites are stored in
    :param name: the name of the site
    :param must_exist: iff True, the file is checked for existence before attempting to open the database

    :return: a connection to the site's database
    """
    db_path = get_site_db(basedir, name)

    if must_exist and not os.access(db_path, os.F_OK):
        raise FileNotFoundError('The requested site could not be found at {}'.format(os.path.join(basedir, name)))

    if must_exist and not os.access(db_path, os.W_OK | os.R_OK):
        raise PermissionError('You do not have the permission to access {}'.format(os.path.join(basedir, name)))

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    init_db(cur)
    cur.close()
    conn.commit()

    return conn


def get_site_info(db):
    db.execute('SELECT site.name, site.remote, site.env, site.default_treeish FROM site;')
    site_info = db.fetchone()

    db.execute('SELECT revision, path FROM deployment WHERE active = 1;')
    rev_info = db.fetchone() or {'revision': None, 'path': None}

    return Site(
        site_info['name'], site_info['remote'], site_info['env'], site_info['default_treeish'],
        rev_info['revision'], rev_info['path']
    )


def accessible_sites(basedir):
    """
    A generator yielding all sites accessible by the current user.

    :param basedir: the directory all sites are stored in
    """
    for ent in os.scandir(basedir):
        ent_db = get_site_db(basedir, ent.name)
        if os.access(ent_db, os.R_OK | os.W_OK):
            conn = sqlite3.connect(ent_db)
            conn.row_factory = sqlite3.Row
            db = conn.cursor()
            init_db(db)

            db.execute('SELECT name, remote, env, default_treeish FROM site;')

            yield db.fetchone()

            conn.close()


def list(args):
    sites = [*accessible_sites(args.basedir)]

    # For each column, find the longest string.
    lengths = {'env': 3, 'name': 4, 'remote': 6, 'default_treeish': max(len('(repo default)'), len('default branch'))}
    for site in sites:
        if not (fnmatch.fnmatch(site['name'], args.site) and fnmatch.fnmatch(site['remote'], args.remote)):
            continue

        for column in site.keys():
            lengths[column] = max(lengths[column], len(site[column] or ''))

    print_site_listing(lengths, {'env': 'env', 'name': 'site', 'remote': 'remote', 'default_treeish': 'default branch'})

    for site in sites:
        if not (fnmatch.fnmatch(site['name'], args.site) and fnmatch.fnmatch(site['remote'], args.remote)):
            continue

        print_site_listing(lengths, site)


def print_site_listing(lengths, site):
    print("{:<{env_width}} | {:<{name_width}} | {:<{remote_width}} | {:<{default_treeish_width}}".format(
        site['env'],
        site['name'],
        site['remote'],
        site['default_treeish'] or '\033[37m(repo default)\033[0m',
        env_width=lengths['env'],
        name_width=lengths['name'],
        remote_width=lengths['remote'],
        default_treeish_width=lengths['default_treeish']
    ))


def deps(args):
    conn = open_site_db(args.basedir, args.site)
    db = conn.cursor()

    db.execute("""
        SELECT deployment.path, deployment.date, deployment.active, deployment.revision, deployment.present
          FROM deployment
          ORDER BY date;
    """)

    dbDeployments = db.fetchall()
    deployments = []

    # Translate each timestamp into a date and calculate the required column widths.
    lengths = {'active': 1, 'path': 4, 'date': 4, 'revision': 6, 'present': 0}
    for dbDep in dbDeployments:
        deployment = {}

        for column in dbDep.keys():
            deployment[column] = dbDep[column]

        deployment['date'] = datetime.datetime.utcfromtimestamp(int(dbDep['date'])).isoformat()

        for column in dbDep.keys():
            if column == 'active':
                continue

            lengths[column] = max(lengths[column], len(str(deployment[column])))

        deployments.append(deployment)

    print_dep_listing(lengths, {
        'active': True, 'path': 'path', 'date': 'date', 'revision': 'commit', 'present': True
    })

    for deployment in deployments:
        if deployment['present'] or args.deleted:
            print_dep_listing(lengths, deployment)

    conn.close()


def print_dep_listing(lengths, dep):
    print("{} | {:<{path_width}} | {:<{date_width}} | {:<{rev_width}}".format(
        ('*' if dep['active'] else 'D' if not dep['present'] else ' '),
        dep['path'],
        dep['date'],
        dep['revision'],
        path_width=lengths['path'],
        date_width=lengths['date'],
        rev_width=lengths['revision']
    ))


def add(args):
    site_name = args.name or prompt_nonempty('Site name')
    site_dir = os.path.join(args.basedir, site_name)

    if os.access(get_site_db(args.basedir, site_name), os.F_OK):
        print('\033[31;1mA site named {} already exists at {}\033[0m'.format(site_name, site_dir))
        if args.force_dangerous:
            setattr(args, 'site', site_name)
            remove(args)
            if os.access(get_site_db(args.basedir, site_name), os.F_OK):
                return
        else:
            return

    remote = args.remote or prompt_default('Remote', 'git.wukl.net:wukl/' + site_name)
    branch = args.branch or prompt_default('Branch (leave empty to use repository default)', None)
    env = args.env or prompt_default('DTAP Environment', 'P')

    os.makedirs(site_dir, mode=0o0775, exist_ok=True)

    conn = open_site_db(args.basedir, site_name, must_exist=False)
    db = conn.cursor()

    db.execute('INSERT INTO site (name, remote, env, default_treeish) VALUES (?, ?, ?, ?)',
               (site_name, remote, env, branch))

    conn.commit()
    conn.close()


def edit(args):
    site_name = args.site

    conn = open_site_db(args.basedir, site_name)
    db = conn.cursor()

    site_info = get_site_info(db)

    if args.name:
        print('\033[31;1mThe site name will be changed to {}. Note that the directory name does not change, ask your '
              'administrator or move the directory yourself.\033[0m'.format(args.name))
        site_info.name = args.name

    if args.remote:
        site_info.remote = args.remote

    if args.branch:
        site_info.default_treeish = args.branch

    if args.env:
        site_info.env = args.env

    db.execute('UPDATE site SET name = ?, remote = ?, env = ?, default_treeish = ? WHERE name = ?',
               (site_info.name, site_info.remote, site_info.env, site_info.default_treeish, site_name)
    )

    conn.commit()
    conn.close()


def prompt_default(prompt, default):
    global assume_yes
    if assume_yes:
        return default

    value = input(prompt + ' [' + (default if default is not None else '') + ']: ')
    if not value:
        return default
    else:
        return value


def prompt_nonempty(prompt):
    global assume_yes
    if assume_yes:
        raise Exception('Missing required value "{}"'.format(prompt))

    value = input(prompt + ': ')
    if value:
        return value

    return prompt_nonempty(prompt)


def prompt_bool(prompt):
    global assume_yes
    if assume_yes:
        return True

    value = input(prompt + ' [N/y]: ')
    if not value:
        return False

    vlower = value.lower()

    return vlower == 'y' or vlower == 'yes'


def fetch_from_cwd(args, deploy_dir):
    subprocess.run(['rsync', '-rlp', '--info=progress2', args.copy_from, deploy_dir], check=True)
    return 'file://{}#{}'.format(os.getcwd(), time.time())


def fetch_from_git(args, db, site_info, deploy_dir):
    subprocess.run(['git', 'clone', site_info.remote, deploy_dir + '/'], check=True)
    branch = args.treeish or site_info.default_treeish
    if branch is not None:
        subprocess.run(['git', '-C', deploy_dir, 'checkout', branch], check=True)
    result = subprocess.run(['git', 'rev-parse', 'HEAD'],
                            stdout=subprocess.PIPE, check=True, cwd=deploy_dir)
    rev_id = result.stdout.decode('utf8').partition("\n")[0]

    db.execute('SELECT 1 FROM deployment WHERE revision = ? AND present = 1;', (rev_id,))
    existing_deployment = db.fetchone()
    if existing_deployment is not None and args.force_useless is False and args.force_dangerous is False:
        print('\033[31;1mThis revision ({}) was already deployed\033[0m'.format(rev_id))
        shutil.rmtree(deploy_dir)
        db.connection.close()

        if args.revert:
            print('\033[33;1mReverting to previous deployment\033[0m')
            activate(args, site_info.name, rev_id)

        return None

    return rev_id


def fetch_files(args, db, site_info, deploy_dir):
    if args.copy_from is None:
        return fetch_from_git(args, db, site_info, deploy_dir)
    else:
        return fetch_from_cwd(args, deploy_dir)


def deploy(args):
    """
    Deploys a site.

    This function covers the entire deployment procedure:

    * clone the repository
    * check for matching deployments
    * register deployment (if new or previously deleted)
    * activate deployment

    :param args: the command line arguments
    :return: nothing
    """
    site_name = args.site

    conn = open_site_db(args.basedir, site_name)
    db = conn.cursor()

    site_info = get_site_info(db)
    site_dir = os.path.join(args.basedir, site_name)

    deploy_dir = os.path.join(site_dir, 'deployments', currentTime)

    print("\033[32;1mDeploying " + site_name + ".\033[0m")

    os.makedirs(deploy_dir, mode=0o755, exist_ok=True)

    rev_id = fetch_files(args, db, site_info, deploy_dir)
    if rev_id is None:
        return

    print('\u001B[32;1mFound revision {}.\u001B[0m'.format(rev_id))

    # Execute post-clone
    run_script(db, deploy_dir, site_info.name, site_info.env, rev_id, 'post-clone')

    db.execute('INSERT INTO deployment (path, revision, date, active) VALUES (?, ?, ?, 0);',
               (deploy_dir, rev_id, int(time.time())))

    conn.commit()
    conn.close()

    activate(args, site_info, rev_id)

    clean(args)


def activate(args, site_info, revision):
    """
    Activates an existing deployment.

    If the deployment does not exist (either was never deployed or previously deleted), an exception is raised.
    Otherwise the symlink is updated and

    :param args: command line arguments containing global settings
    :param site: the site to activate the deployment for
    :param revision: the revision ID indicating the deployment to activate
    :return:
    """
    site_name = site_info.name
    conn = open_site_db(args.basedir, site_name)
    db = conn.cursor()

    site_dir = os.path.join(args.basedir, site_name)
    link_name = os.path.join(site_dir, 'current')
    new_link_name = link_name + '.new'

    # Find the directory the deployment is in
    db.execute('SELECT path FROM deployment WHERE revision = ? AND present = 1 ORDER BY date DESC LIMIT 1', (revision,))
    path_info = db.fetchone()
    if path_info is None:
        raise Exception('No available deployment for revision {} for site {}'.format(revision, site_name))

    # Check that the directory actually exists
    new_path = path_info['path']
    old_path = site_info.cur_path
    if not os.path.exists(new_path):
        db.execute('UPDATE deployment SET present = 0 WHERE path = ?', (new_path,))
        conn.commit()
        conn.close()
        raise Exception('The selected revision ({}) has been removed'.format(revision))

    # Determine the location for the shared data
    shared_dir = os.path.join(site_dir, 'shared')
    shared_link_name = os.path.join(new_path, 'shared')
    new_shared_link_name = shared_link_name + '.new'

    # Switch the symlink to shared data, if the folder is present
    if os.path.exists(shared_dir):
        os.symlink(shared_dir, new_shared_link_name, target_is_directory=True)
        os.replace(new_shared_link_name, shared_link_name)

    # Execute pre-deactivate, pre-activate
    run_script(db, old_path, site_info.name, site_info.env, revision, 'pre-deactivate')
    run_script(db, new_path, site_info.name, site_info.env, site_info.cur_rev, 'pre-activate')

    # Switch the symlink
    os.symlink(new_path, new_link_name, target_is_directory=True)
    os.replace(new_link_name, link_name)

    # Register the new deployment
    db.execute('UPDATE deployment SET active = 0;')
    db.execute("""
        UPDATE deployment
          SET active = 1
          WHERE rowid = (SELECT rowid FROM deployment WHERE revision = ? ORDER BY date DESC LIMIT 1);
    """, (revision,))

    # Execute post-deactivate, post-activate
    run_script(db, old_path, site_info.name, site_info.env, site_info.cur_rev, 'post-deactivate')
    run_script(db, new_path, site_info.name, site_info.env, revision, 'post-activate')

    conn.commit()
    conn.close()


def revert(args):
    site = args.site

    conn = open_site_db(args.basedir, site)
    db = conn.cursor()

    rev = args.rev
    if rev is None:
        db.execute('SELECT revision FROM deployment WHERE active <> 1 AND present = 1 ORDER BY date DESC LIMIT 1')

        rev_info = db.fetchone()
        if rev_info is None:
            raise Exception('No available previous deployment to revert to')

        rev = rev_info['rev']

    activate(args, site, rev)

    conn.commit()
    conn.close()


def clean(args):
    site_name = args.site

    conn = open_site_db(args.basedir, site_name)
    db = conn.cursor()

    site_info = get_site_info(db)

    db.connection.commit()
    db.execute("""
        SELECT deployment.id, deployment.path, deployment.revision
          FROM deployment
          WHERE deployment.active <> 1
            AND deployment.present = 1
          ORDER BY deployment.date DESC
          LIMIT 1000000 OFFSET 4;
    """)

    results = db.fetchall()

    for result in results:
        print('\033[33;1mDeleting', result['path'], '\033[0m')

        run_script(db, result['path'], site_info.name, site_info.env, result['revision'], 'pre-remove')

        try:
            shutil.rmtree(result['path'])
        except Exception:
            pass

        db.execute('UPDATE deployment SET present = 0 WHERE id = ?', (result['id'],))

    conn.commit()
    conn.close()


def remove(args):
    site_name = args.site

    # Check for administrative access
    if not os.access(args.basedir, os.W_OK):
        raise PermissionError(
            'Administrative access (i.e., write access to the base directory) is required for deleting sites'
        )

    # Ensure that the database exists and is accessible
    conn = open_site_db(args.basedir, site_name)
    conn.close()

    site_dir = os.path.join(args.basedir, site_name)

    confirmed = prompt_bool('Are you sure you want to delete site {} at {}?'.format(site_name, site_dir))
    if not confirmed:
        print('\033[31;1mAborted\033[0m')
        return

    shutil.rmtree(site_dir)


def extract_env_args(stage):
    global args

    env = {}

    if args.env_args is not None:
        for arg in args.env_args:
            key, value = (arg.split('=', maxsplit=1) + [None])[:2]

            try:
                kstage, key = key.split(':', maxsplit=1)
                if kstage != stage:
                    continue
            except ValueError:
                pass

            env[key] = value

    return env


def run_script(db, deployment_path, site_name, environment, commit, stage):
    if deployment_path is None:
        return

    script_path = os.path.join(deployment_path, 'deploy', stage)
    if not os.path.exists(script_path):
        return

    global args

    env = dict(os.environ) if args.inherit_env else {}
    env.update({
        'DOUW_SITE_NAME': site_name,
        'DOUW_ENVIRONMENT': environment,
        'DOUW_REVISION': commit,
        'DOUW_STAGE': stage
    })
    env.update([(var['name'], var['value']) for var in get_vars(db)])
    env.update(extract_env_args(stage))

    subprocess.run([script_path], env=env, cwd=deployment_path, check=True)


def var(args):
    conn = open_site_db(args.basedir, args.site)
    db = conn.cursor()

    if args.var is None:
        list_vars(db)
    elif '=' in args.var:
        name, value = args.var.split('=', maxsplit=1)
        set_var(db, name, value)
        conn.commit()
    else:
        get_var(db, args.var)

    conn.close()


def get_vars(db):
    db.execute("SELECT variable.name, variable.value FROM variable ORDER BY variable.name")
    return [{'name': res['name'], 'value': res['value']} for res in db.fetchall()]


def print_var_listing(lengths, var):
    print("{:<{name_width}} | {:<{value_width}}".format(
        var['name'],
        var['value'],
        name_width=lengths['name'],
        value_width=lengths['value'],
    ))


def list_vars(db):
    results = get_vars(db)

    lengths = {'name': 4, 'value': 5}

    for var in results:
        for col in var.keys():
            lengths[col] = max(lengths[col], len(var[col] or ''))

    print_var_listing(lengths, {'name': 'name', 'value': 'value'})

    for var in results:
        print_var_listing(lengths, var)


def set_var(db, name, value):
    db.execute('INSERT INTO variable (name, value) VALUES (?, ?);', (name, value))


def get_var(db, name):
    db.execute('SELECT variable.value FROM variable WHERE variable.name = ?', (name,))
    var = db.fetchone()

    print(name, '=', var['value'], sep='')


def version(args):
    print('Douw {}'.format(__version__))

    if args.full:
        print('Python {}'.format(sys.version))

    if not args.no_copyright:
        print('Copyright © 2016–⁠2020 Luc Everse')
        print('https://git.wukl.net/wukl/douw')
