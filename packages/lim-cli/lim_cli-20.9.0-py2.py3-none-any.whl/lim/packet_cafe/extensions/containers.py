# -*- coding: utf-8 -*-

import argparse
import logging
import os
import re
import sys
import textwrap

from cliff.command import Command
from cliff.lister import Lister
from lim import execute
from lim.packet_cafe import add_docker_global_options
from lim.packet_cafe import add_packet_cafe_global_options
from lim.packet_cafe import containers_are_running
from lim.packet_cafe import get_containers
from lim.packet_cafe import get_images
from lim.packet_cafe import get_output
from lim.packet_cafe import get_workers_definitions
from lim.packet_cafe import rm_images
from lim.packet_cafe import Packet_Cafe


logger = logging.getLogger(__name__)

RUNNING_MSG = '[-] packet-cafe containers are already running'
NOT_RUNNING_MSG = '[-] packet-cafe containers are not running'
UPDATE_MSG = "[!] to pull changes, use the '--update' option"
NO_UPDATE_MSG = "[-] '--update' did not have to do anything"
UI_MSG = "[+] you can now use 'lim cafe ui' to start the UI"
UP_MSG = "[+] you can use 'lim cafe containers up' to restart the stack"
MIN_IMAGE_COLUMNS = ('ID', 'Repository', 'Tag')

ON_BRANCH_REGEX = re.compile(r'On branch (\w+) ')
HEAD_POSITION_REGEX = re.compile(
    r"Your branch is (.*) [\w/]+ by (\d+) commit")


def print_output(results=[]):
    for line in results:
        sys.stdout.write(line)
        if '\x1b' not in line:
            sys.stdout.write('\n')


def get_environment(args):
    env = dict(os.environ.copy())
    if args.docker_service_namespace is not None:
        env["SERVICE_NAMESPACE"] = args.docker_service_namespace
    if args.docker_service_version is not None:
        env["SERVICE_VERSION"] = args.docker_service_version
    if args.docker_tool_namespace is not None:
        env["TOOL_NAMESPACE"] = args.docker_tool_namespace
    if args.docker_tool_version is not None:
        env["TOOL_VERSION"] = args.docker_tool_version
    env["REPO_DIR"] = args.packet_cafe_repo_dir
    env["GITHUB_URL"] = args.packet_cafe_github_url
    return env


def ensure_clone(url=None,
                 repo_dir=None,
                 remote='origin',
                 branch='master'):
    """Make sure that a clone of packet_cafe exists in repo_dir."""
    if url is None:
        url = Packet_Cafe.CAFE_GITHUB_URL
    if os.path.exists(repo_dir):
        if not os.path.exists(os.path.join(repo_dir, '.git')):
            raise RuntimeError(f'[-] Directory "{repo_dir}" does not '
                               'look like a Git repository clone')
        elif not os.path.exists(os.path.join(repo_dir, 'docker-compose.yml')):
            raise RuntimeError(f'[-] Directory "{repo_dir}" does not '
                               'contain a docker-compose.yml file')
        try:
            remotes = get_remote(repo_dir)
        except RuntimeError:
            remotes = []
        if remote not in remotes:
            raise RuntimeError(f"[-] directory '{repo_dir}' does not "
                               f"have a remote '{remote}' defined")
    else:
        logger.info(f"[-] directory '{repo_dir}' does not exist")
        return clone(url=url, repo_dir=repo_dir, branch=branch)
    return True


def clone(url=None, repo_dir=None, branch='master'):
    """Clone Git repository."""
    # $ git clone https://github.com/iqtlabs/packet_cafe.git /tmp/packet_cafe
    # Cloning into '/tmp/packet_cafe'...
    # remote: Enumerating objects: 3999, done.
    # remote: Total 3999 (delta 0), reused 0 (delta 0), pack-reused 3999
    # Receiving objects: 100% (3999/3999), 13.71 MiB | 1.67 MiB/s, done.
    # Resolving deltas: 100% (2380/2380), done.
    logger.info(f'[+] cloning from URL {url}')
    sys.stdout.write('[+] ')
    sys.stdout.flush()
    clone_result = execute(cmd=['git', 'clone', url, repo_dir])
    if clone_result != 0:
        try:
            os.rmdir(repo_dir)
        except OSError:
            pass
        raise RuntimeError('[-] cloning failed')
    logger.info(f"[+] checking out '{branch}' branch")
    up_to_date = checkout(repo_dir, branch=branch)
    return up_to_date


def needs_update(
    repo_dir=None,
    branch='master',
    remote='origin',
    ignore_dirty=True
):
    """Check to see if GitHub repo is up to date."""
    remotes = get_remote(repo_dir)
    if len(remotes) > 1:
        others = ','.join(remotes)
        logger.info(f'[-] more than one remote found: {others}')
    if repo_dir is None:
        raise RuntimeError('[-] repo_dir must be specified')
    if not is_clean(repo_dir) and not ignore_dirty:
        raise RuntimeError(
                f'[-] directory {repo_dir} is not clean \n'
                "    (use '--ignore-dirty' if you are testing local changes)")
    fetched_new = fetch(repo_dir, remote=remote)
    if fetched_new:
        logger.info(f"[+] fetch from remote '{remote}' updated {repo_dir}")
    current_branch = get_branch(repo_dir)
    if current_branch != branch:
        raise RuntimeError(f"[-] branch '{current_branch}' is checked out")
    need_checkout, position, commit_delta = get_branch_status(repo_dir,
                                                              branch=branch)
    if commit_delta is not None:
        direction = "away from" if position is None else position
        logging.debug(f"[-] branch '{branch}' is {commit_delta} "
                      f"commit{'s' if commit_delta != 1 else ''} "
                      f"{direction} the remote HEAD")
    up_to_date = checkout(repo_dir, branch=branch)
    if not up_to_date:
        logger.info(f"[!] branch '{branch}' is not up to date!")
    else:
        logger.info(f"[+] branch '{branch}' is up to date")
    # results = pull(repo_dir, remote=remote, branch=branch)
    return not up_to_date


def is_clean(repo_dir):
    """Return boolean reflecting whether repo directory is clean or not."""
    results = [line for line
               in get_output(cmd=['git', 'status', '--porcelain'],
                             cwd=repo_dir)
               if not line.startswith('??')
               ]
    return len(results) == 0


def get_branch(repo_dir):
    """Return the name of the checked out branch."""
    results = get_output(cmd=['git', 'branch'],
                         cwd=repo_dir)
    branches = [row[2:] for row in results if row.startswith('* ')]
    if len(branches) != 1:
        raise RuntimeError('[-] failed to identify checked out branch')
    return branches[0]


def get_branch_status(repo_dir, branch='master'):
    """Return branch status information."""
    # $ git status -b master
    # On branch master
    # Your branch is behind 'origin/master' by 7 commits, and can be fast-forwarded.  # noqa
    #   (use "git pull" to update your local branch)
    #
    # nothing to commit, working tree clean
    cmd = ['git', 'status', '-b', branch]
    logger.debug(f"running: {' '.join(cmd)}")
    results_str = '\n'.join(get_output(cmd=cmd,
                                       cwd=repo_dir))
    need_checkout = False

    # m = ON_BRANCH_REGEX.search(results_str, re.MULTILINE)
    # m = re.search(r'On branch (\w+) ', results_str, re.MULTILINE)
    m = re.search(r'^On branch (\w+)$', results_str, re.MULTILINE)
    need_checkout = True if (m and (m.groups()[0] != branch)) else False
    # m = HEAD_POSITION_REGEX.search(results_str, re.MULTILINE)
    m = re.search(r'^Your branch is (\w+) [\w/\']+ by (\d+)',
                  results_str,
                  re.MULTILINE)
    if m:
        position, commit_delta = m.groups()
    else:
        position, commit_delta = None, None
    return need_checkout, position, commit_delta


def get_remote(repo_dir):
    """Return the remotes for this repo."""
    remotes = get_output(cmd=['git', 'remote'],
                         cwd=repo_dir)
    if not len(remotes):
        raise RuntimeError('[-] failed to get remotes')
    return remotes


def fetch(repo_dir, remote='origin'):
    """Fetch from remote."""
    # $ git fetch upstream
    # remote: Enumerating objects: 2, done.
    # remote: Counting objects: 100% (2/2), done.
    # remote: Compressing objects: 100% (2/2), done.
    # remote: Total 2 (delta 0), reused 0 (delta 0), pack-reused 0
    # Unpacking objects: 100% (2/2), 1.57 KiB | 1.57 MiB/s, done.
    # From https://github.com/iqtlabs/packet_cafe
    #   152ec36..cc895f5  master     -> upstream/master
    results = get_output(cmd=['git', 'fetch', remote],
                         cwd=repo_dir)
    return bool(len(results))


def checkout(repo_dir, branch='master'):
    """Checkout branch."""
    # $ git checkout master
    # Switched to branch 'master'
    # Your branch is up to date with 'origin/master'.
    #
    # $ git checkout master
    # Already on 'master'
    # Your branch is up to date with 'origin/master'.
    #
    # $ git checkout master
    # Switched to branch 'master'
    # Your branch is behind 'origin/master' by 7 commits, and can be fast-forwarded.  # noqa
    #  (use "git pull" to update your local branch)
    #
    # $ git checkout master
    # On branch master
    # Your branch is behind 'origin/master' by 7 commits, and can be fast-forwarded.  # noqa
    #  (use "git pull" to update your local branch)
    #
    # nothing to commit, working tree clean
    #
    results = get_output(cmd=['git', 'checkout', branch],
                         cwd=repo_dir)
    results_str = ' '.join(results)
    # Apparently different versions of ``git`` produce different
    # results. Go figure... :(
    return (
        results_str.find('Your branch is up to date') > 0 or
        results_str.find('Your branch is up-to-date') > 0
    )


def pull(repo_dir, remote='origin', branch='master'):
    """Return the remotes for this repo."""
    # $ git pull upstream master
    # From https://github.com/CyberReboot/packet_cafe
    # * branch            master     -> FETCH_HEAD
    # Successfully rebased and updated refs/heads/master.
    # $ git pull upstream master
    # From https://github.com/CyberReboot/packet_cafe
    # * branch            master     -> FETCH_HEAD
    # Already up to date.
    results = get_output(cmd=['git',
                              'pull',
                              f"{remote}",
                              f"{branch}"
                              ],
                         cwd=repo_dir)
    results_str = ' '.join(results)
    if not (
        results_str.find('Successfully') or
        results_str.find('Already up to date')
    ):
        raise RuntimeError(
            f'[-] pull from "{remote}" to branch "{branch}" had problems')
    return True


class ContainersBuild(Command):
    """Build Packet Café Docker containers."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        update = parser.add_mutually_exclusive_group(required=False)
        update.add_argument(
            '-u', '--update',
            action='store_true',
            dest='update',
            default=False,
            help=('Update the repository contents before rebuilding '
                  '(default: False)')
        )
        update.add_argument(
            '--ignore-dirty',
            action='store_true',
            dest='ignore_dirty',
            default=False,
            help=('Ignore a dirty repository (default: False)')
        )
        # Text here also copied to docs/packet_cafe.rst
        parser.epilog = textwrap.dedent("""
            Build images from source locally rather than pulling them from Docker Hub.
            This is used for local deployment or development and testing locally. If
            you wish to use images from Docker Hub, use ``lim cafe containers pull``
            instead.

            You will be notified if the GitHub repo has newer content and the program
            will exit. Use the ``--update`` flag to update the repo before building.
            """)  # noqa
        return add_docker_global_options(parser)

    def take_action(self, parsed_args):
        logger.debug('[+] locally build Packet Café Docker containers')
        if containers_are_running():
            if bool(self.app_args.verbose_level):
                logger.info(RUNNING_MSG)
            sys.exit(1)
        repo_dir = parsed_args.packet_cafe_repo_dir
        remote = parsed_args.packet_cafe_repo_remote
        branch = parsed_args.packet_cafe_repo_branch
        ensure_clone(url=parsed_args.packet_cafe_github_url,
                     repo_dir=repo_dir,
                     remote=remote,
                     branch=branch)
        if needs_update(repo_dir,
                        remote=remote,
                        branch=branch,
                        ignore_dirty=parsed_args.ignore_dirty):
            if parsed_args.update:
                pull(repo_dir, remote=remote, branch=branch)
            else:
                if parsed_args.ignore_dirty:
                    logger.info(UPDATE_MSG)
                else:
                    raise RuntimeError(UPDATE_MSG)
        elif parsed_args.update:
            logger.info(NO_UPDATE_MSG)
        # Ensure VOL_PREFIX environment variable is set
        os.environ['VOL_PREFIX'] = self.app_args.packet_cafe_data_dir
        env = get_environment(parsed_args)
        #
        # ERROR: for messenger  Get https://registry-1.docker.io/v2/davedittrich/packet_cafe_messenger/manifests/sha256:...: proxyconnect tcp: dial tcp 192.168.65.1:3129: i/o timeout  # noqa
        #
        env['COMPOSE_HTTP_TIMEOUT'] = '200'
        cmd = [
            'docker-compose',
            'up'
        ]
        if self.app_args.verbose_level <= 1 and not self.app_args.debug:
            cmd.append('-d')
        cmd.append('--build')
        if self.app_args.verbose_level > 0:
            logger.info(
                f"[+] running '{' '.join(cmd)}' in {repo_dir}")
        result = execute(cmd=cmd, cwd=repo_dir, env=env)
        if result != 0:
            raise RuntimeError('[-] docker-compose build failed')
        else:
            logger.info(UI_MSG)


class ContainersDown(Command):
    """Bring down Packet Café Docker containers."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        # Text here also copied to docs/packet_cafe.rst
        parser.epilog = textwrap.dedent("""
            Bring down the container stack associated with Packet Café services.

            .. code-block:: none

                $ lim cafe containers down
                [+] running 'docker-compose down' in /Users/dittrich/packet_cafe
                Stopping packet_cafe_redis_1     ... done
                Stopping packet_cafe_web_1       ... done
                Stopping packet_cafe_workers_1   ... done
                Stopping packet_cafe_ui_1        ... done
                Stopping packet_cafe_admin_1     ... done
                Stopping packet_cafe_messenger_1 ... done
                Stopping packet_cafe_lb_1        ... done
                Removing packet_cafe_redis_1         ... done
                Removing packet_cafe_web_1           ... done
                Removing packet_cafe_workers_1       ... done
                Removing packet_cafe_mercury_1       ... done
                Removing packet_cafe_ui_1            ... done
                Removing packet_cafe_pcap-dot1q_1    ... done
                Removing packet_cafe_admin_1         ... done
                Removing packet_cafe_messenger_1     ... done
                Removing packet_cafe_pcap-splitter_1 ... done
                Removing packet_cafe_ncapture_1      ... done
                Removing packet_cafe_pcapplot_1      ... done
                Removing packet_cafe_lb_1            ... done
                Removing packet_cafe_networkml_1     ... done
                Removing packet_cafe_pcap-stats_1    ... done
                Removing packet_cafe_snort_1         ... done
                Removing network packet_cafe_default
                Removing network admin
                Removing network frontend
                Removing network results
                Removing network backend
                Removing network analysis
                Removing network preprocessing
                [+] you can use 'lim cafe containers up' to restart the stack

            ..

            After bringing the containers down, you can generally bring them
            back up without having to rebuild them.

            If you are just standing things up for the first time, are
            doing local development editing files in your clone, or are
            updating the repository with ``--update``, you will need to
            rebuild the containers.
            """)  # noqa
        return add_docker_global_options(parser)

    def take_action(self, parsed_args):
        logger.debug('[+] bring down Packet Café Docker containers')
        if not containers_are_running():
            if bool(self.app_args.verbose_level):
                logger.info(NOT_RUNNING_MSG)
            sys.exit(1)
        repo_dir = parsed_args.packet_cafe_repo_dir
        ensure_clone(url=parsed_args.packet_cafe_github_url,
                     repo_dir=repo_dir,
                     branch=parsed_args.packet_cafe_repo_branch)
        cmd = ['docker-compose']
        if self.app_args.verbose_level > 1:
            cmd.append('--verbose')
        cmd.append('down')
        if self.app_args.verbose_level > 0:
            logger.info(f"[+] running '{' '.join(cmd)}' in {repo_dir}")
        env = get_environment(parsed_args)
        result = execute(cmd=cmd, cwd=repo_dir, env=env)
        if result != 0:
            raise RuntimeError('[-] docker-compose down failed')
        else:
            logger.info(UP_MSG)


class ContainersImages(Lister):
    """List Packet Café related Docker images."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            '--rm',
            action='store_true',
            dest='rm_images',
            default=False,
            help='Remove the images from Docker (default: False)'
        )
        # Enable all columns if user requests specific columns that
        # might not be in MIN_IMAGE_COLUMNS with ``-c``.
        parser.add_argument(
            '-a', '--all-columns',
            action='store_true',
            dest='all_columns',
            default=('-c' in sys.argv),
            help='Include all available columns (default: False)'
        )
        # Text here also copied to docs/packet_cafe.rst
        parser.epilog = textwrap.dedent("""
            List the images associated with Packet Café services and workers.

            .. code-block:: console

                [+] listing images for service namespace "iqtlabs", tool namespace "iqtlabs"
                +--------------+-------------------------------+--------+
                | ID           | Repository                    | Tag    |
                +--------------+-------------------------------+--------+
                | 7808ad5f74f5 | iqtlabs/packet_cafe_workers   | latest |
                | 83fdfb8db32d | iqtlabs/packet_cafe_redis     | latest |
                | 93fc21bf376a | iqtlabs/packet_cafe_messenger | latest |
                | 11bb63d0c705 | iqtlabs/packet_cafe_lb        | latest |
                | d9194c6daf5f | iqtlabs/packet_cafe_web       | latest |
                | 9fc447bc9fa4 | iqtlabs/packet_cafe_ui        | latest |
                | 8fe33a5eec27 | iqtlabs/packet_cafe_admin     | latest |
                | 1a5cec5e1dab | iqtlabs/tcprewrite_dot1q      | latest |
                | 39c6e9ac53a9 | iqtlabs/pcap_to_node_pcap     | latest |
                | adcc5b1f4213 | iqtlabs/pcap_stats            | latest |
                | 6732f33c5b25 | iqtlabs/ncapture              | latest |
                | 251346bde2eb | iqtlabs/networkml             | v0.6.1 |
                | 6d2d5d790715 | iqtlabs/mercury               | latest |
                | cedfd83f10dc | iqtlabs/snort                 | latest |
                | b56a25f62851 | iqtlabs/pcapplot              | v0.1.7 |
                +--------------+-------------------------------+--------+

            By default, only three columns are shown. If you wish to see all
            available columns, use the ``-a`` option.

            You can remove all of these images from Docker's image storage
            by using the ``--rm`` option.

            If you are doing development and have pushed images to your own
            namespace on Docker Hub, use the namespace and version selection
            options or environment variables.
            ..
            """)  # noqa
        return add_docker_global_options(parser)

    def take_action(self, parsed_args):
        logger.debug('[+] list Packet Café Docker images')
        # cmd = [
        #     'docker',
        #     'images',
        #     f'--filter=reference="{parsed_args.docker_service_namespace}/*"',
        #     f'--filter=reference="{parsed_args.docker_tool_namespace}/*"',
        #     '--format',
        #     '"table {{.ID}}\t{{.Repository}}\t{{.Tag}}"'
        # ]
        # if result != 0:
        #     raise RuntimeError('[-] failed to list containers')
        service_namespace = parsed_args.docker_service_namespace \
            if parsed_args.docker_service_namespace is not None else 'iqtlabs'
        tool_namespace = parsed_args.docker_tool_namespace \
            if parsed_args.docker_tool_namespace is not None else 'iqtlabs'
        workers_definitions = get_workers_definitions(
            parsed_args.packet_cafe_repo_dir)
        images = get_images(service_namespace=service_namespace,
                            tool_namespace=tool_namespace,
                            workers_definitions=workers_definitions)
        image_set = (
            f'service namespace "{service_namespace}", '
            f'tool namespace "{tool_namespace}"'
        )
        if not len(images):
            raise RuntimeError(f'[-] no images found for {image_set}')
        if self.app_args.verbose_level > 0:
            action = 'removing' if parsed_args.rm_images else 'listing'
            logger.info(f'[+] {action} images for {image_set}')
        columns = MIN_IMAGE_COLUMNS
        if parsed_args.rm_images:
            data = (
                    tuple(i[c] for c in columns)
                    for i in rm_images(images)
                   )
        else:
            if parsed_args.all_columns:
                columns = images[0].keys()
            data = (
                    tuple(i[c] for c in columns)
                    for i in images
                   )
        return columns, data


class ContainersPull(Command):
    """Pull Packet Café Docker containers."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        update = parser.add_mutually_exclusive_group(required=False)
        update.add_argument(
            '-u', '--update',
            action='store_true',
            dest='update',
            default=False,
            help=('Update the repository contents before pulling '
                  '(default: False)')
        )
        update.add_argument(
            '--ignore-dirty',
            action='store_true',
            dest='ignore_dirty',
            default=False,
            help=('Ignore a dirty repository (default: False)')
        )
        # Text here also copied to docs/packet_cafe.rst
        parser.epilog = textwrap.dedent("""
            Pull the containers associated with Packet Café services and workers from
            Docker Hub to cache them locally.
            """)  # noqa
        return add_docker_global_options(parser)

    def take_action(self, parsed_args):
        logger.debug('[+] pull Packet Café Docker containers')
        if containers_are_running():
            if bool(self.app_args.verbose_level):
                logger.info(RUNNING_MSG)
            sys.exit(1)
        env = get_environment(parsed_args)
        repo_dir = parsed_args.packet_cafe_repo_dir
        # TODO(dittrich): Fix this
        remote = "origin"
        branch = parsed_args.packet_cafe_repo_branch
        ensure_clone(url=parsed_args.packet_cafe_github_url,
                     repo_dir=repo_dir,
                     branch=branch)
        if needs_update(repo_dir,
                        remote=remote,
                        branch=branch,
                        ignore_dirty=parsed_args.ignore_dirty):
            if parsed_args.update:
                pull(repo_dir, remote=remote, branch=branch)
            else:
                if parsed_args.ignore_dirty:
                    logger.info(UPDATE_MSG)
                else:
                    raise RuntimeError(UPDATE_MSG)
        # Ensure VOL_PREFIX environment variable is set
        os.environ['VOL_PREFIX'] = self.app_args.packet_cafe_data_dir
        env = get_environment(parsed_args)
        #
        # ERROR: for messenger  Get https://registry-1.docker.io/v2/davedittrich/packet_cafe_messenger/manifests/sha256:...: proxyconnect tcp: dial tcp 192.168.65.1:3129: i/o timeout  # noqa
        #
        env['COMPOSE_HTTP_TIMEOUT'] = '200'
        cmd = ['docker-compose', 'pull']
        if self.app_args.verbose_level > 0:
            logger.info(f"[+] running '{' '.join(cmd)}' in {repo_dir}")
        result = execute(cmd=cmd, cwd=repo_dir, env=env)
        if result != 0:
            raise RuntimeError('[-] failed to pull containers')


class ContainersShow(Lister):
    """Show status of Packet Café Docker containers."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        # Text here also copied to docs/packet_cafe.rst
        parser.epilog = textwrap.dedent("""
            Produces a table listing the Docker containers associated with
            Packet Café (by virtue of the ``com.docker.compose.project``
            label being set to ``packet_cafe``).

            .. code-block:: console

                $ lim cafe containers show
                +-------------------------+------------+--------------------------------------+---------+
                | name                    | short_id   | image                                | status  |
                +-------------------------+------------+--------------------------------------+---------+
                | packet_cafe_messenger_1 | ce4eed9e01 | iqtlabs/packet_cafe_messenger:latest | running |
                | packet_cafe_workers_1   | 43fff494f6 | iqtlabs/packet_cafe_workers:latest   | running |
                | packet_cafe_ui_1        | 794eb87ed6 | iqtlabs/packet_cafe_ui:latest        | running |
                | packet_cafe_web_1       | a1f8f5f7cc | iqtlabs/packet_cafe_web:latest       | running |
                | packet_cafe_mercury_1   | 882b12e31f | iqtlabs/mercury:v0.11.10             | running |
                | packet_cafe_ncapture_1  | 5b1b10f3e0 | iqtlabs/ncapture:v0.11.10            | running |
                | packet_cafe_admin_1     | 73304f16cf | iqtlabs/packet_cafe_admin:latest     | running |
                | packet_cafe_redis_1     | c893c408b5 | iqtlabs/packet_cafe_redis:latest     | running |
                | packet_cafe_lb_1        | 4530125e8e | iqtlabs/packet_cafe_lb:latest        | running |
                +-------------------------+------------+--------------------------------------+---------+

            ..

            To just get a return value (``0`` for "all running" and ``1`` if not),
            use the ``-q`` option.

            .. code-block:: console

                $ lim -q cafe containers show
                $ echo $?
                0
            ..
            """)  # noqa
        parser = add_packet_cafe_global_options(parser)
        return add_docker_global_options(parser)

    def take_action(self, parsed_args):
        logger.debug('[+] show status on Packet Café Docker containers')
        service_namespace = parsed_args.docker_service_namespace \
            if parsed_args.docker_service_namespace is not None else 'iqtlabs'
        if not containers_are_running(
            service_namespace=service_namespace
        ):
            if bool(self.app_args.verbose_level):
                logger.info(NOT_RUNNING_MSG)
            sys.exit(1)
        elif not bool(self.app_args.verbose_level):
            sys.exit(0)
        # client = docker.from_env()
        # container_ids = [getattr(c, 'id') for c in client.containers.list()]
        columns = ['name', 'short_id', 'image', 'status']
        data = get_containers(columns=columns)
        return columns, data


class ContainersUp(Command):
    """Bring up Packet Café Docker containers."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        update = parser.add_mutually_exclusive_group(required=False)
        update.add_argument(
            '-u', '--update',
            action='store_true',
            dest='update',
            default=False,
            help=('Update the repository contents before rebuilding '
                  '(default: False)')
        )
        update.add_argument(
            '--ignore-dirty',
            action='store_true',
            dest='ignore_dirty',
            default=False,
            help=('Ignore a dirty repository (default: False)')
        )
        # Text here also copied to docs/packet_cafe.rst
        parser.epilog = textwrap.dedent("""
            Brings up the container and network stack associated with Packet Café
            services and workers if they are not yet running. Messages from
            ``docker-compose`` will be output to show progress. This can be
            suppressed with the ``-q`` flag.

            Prior to running ``docker-compose``, the repository directory will
            be created (if it does not yet exist) or a ``git fetch`` will be
            attempted to check for updates.

            .. code-block:: console

                $ lim cafe containers up
                [+] branch 'master' is up to date
                [+] running 'docker-compose up -d --no-build' in /Users/dittrich/packet_cafe
                Creating network "packet_cafe_default" with the default driver
                Creating network "admin" with the default driver
                Creating network "frontend" with the default driver
                Creating network "results" with the default driver
                Creating network "backend" with the default driver
                Creating network "analysis" with the default driver
                Creating network "preprocessing" with the default driver
                Creating packet_cafe_admin_1         ... done
                Creating packet_cafe_ncapture_1      ... done
                Creating packet_cafe_networkml_1     ... done
                Creating packet_cafe_pcap-dot1q_1    ... done
                Creating packet_cafe_pcap-splitter_1 ... done
                Creating packet_cafe_snort_1         ... done
                Creating packet_cafe_pcap-stats_1    ... done
                Creating packet_cafe_ui_1            ... done
                Creating packet_cafe_web_1           ... done
                Creating packet_cafe_messenger_1     ... done
                Creating packet_cafe_lb_1            ... done
                Creating packet_cafe_redis_1         ... done
                Creating packet_cafe_mercury_1       ... done
                Creating packet_cafe_workers_1       ... done
                Creating packet_cafe_pcapplot_1      ... done
                [+] you can now use 'lim cafe ui' to start the UI

            ..

            With either ``-q`` or normal verbosity, the containers will be run in
            deamon mode (i.e., run in the background) and the command will immediately
            return.

            Adding ``-v`` or ``--debug`` will run the containers in the foreground and
            produce a stream of log output from all of the containers. This assists in
            debugging and development testing. If you interrupt with CTRL-C, the
            containers will be halted and you will need to bring them back up.

            If new updates are available in the remote repository, you will see
            messages about this and ``lim`` will suggest using the ``--update``
            option and exit before starting the containers.  You can skip the
            update and bring the containers up with the ``--ignore-dirty``
            option.

            Note that if you are building containers locally, you may not be
            able to use the ``--update`` option with ``up``. It depends on what
            was changed during the update. In some cases, the local containers
            will not need to be rebuilt. In other cases, they will. Docker will
            let you know if a rebuild is necessary.
            """)  # noqa
        # TODO(dittrich): Add a debugging section to docs and reference here.
        return add_docker_global_options(parser)

    def take_action(self, parsed_args):
        logger.debug('[+] bring up Packet Café Docker stack')
        if containers_are_running():
            if bool(self.app_args.verbose_level):
                logger.info(RUNNING_MSG)
            sys.exit(1)
        repo_dir = parsed_args.packet_cafe_repo_dir
        # TODO(dittrich): Fix this
        remote = "origin"
        branch = parsed_args.packet_cafe_repo_branch
        ensure_clone(url=parsed_args.packet_cafe_github_url,
                     repo_dir=repo_dir,
                     branch=parsed_args.packet_cafe_repo_branch)
        if needs_update(repo_dir,
                        remote=remote,
                        branch=branch,
                        ignore_dirty=parsed_args.ignore_dirty):
            if parsed_args.update:
                pull(repo_dir, remote=remote, branch=branch)
            else:
                if parsed_args.ignore_dirty:
                    logger.info(UPDATE_MSG)
                else:
                    raise RuntimeError(UPDATE_MSG)
        elif parsed_args.update:
            logger.info(NO_UPDATE_MSG)
        cmd = [
            'docker-compose',
            'up'
        ]
        if self.app_args.verbose_level <= 1 and not self.app_args.debug:
            cmd.append('-d')
        cmd.append('--no-build')
        # Ensure VOL_PREFIX environment variable is set
        os.environ['VOL_PREFIX'] = self.app_args.packet_cafe_data_dir
        env = get_environment(parsed_args)
        #
        # ERROR: for messenger  Get https://registry-1.docker.io/v2/davedittrich/packet_cafe_messenger/manifests/sha256:...: proxyconnect tcp: dial tcp 192.168.65.1:3129: i/o timeout  # noqa
        #
        env['COMPOSE_HTTP_TIMEOUT'] = '200'
        if self.app_args.verbose_level > 0:
            logger.info(f"[+] running '{' '.join(cmd)}' in {repo_dir}")
        result = execute(cmd=cmd, cwd=repo_dir, env=env)
        if result != 0:
            raise RuntimeError(
                '[-] docker-compose failed to bring containers up'
            )
        else:
            logger.info(UI_MSG)


# vim: set ts=4 sw=4 tw=0 et :
