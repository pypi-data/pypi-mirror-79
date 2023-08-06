import argparse
import concurrent.futures
import contextlib
import itertools
import os
import pathlib
import subprocess
import threading
from logging import getLogger
from typing import *

import onlinejudge_command.format_utils as fmtutils
import onlinejudge_command.pretty_printers as pretty_printers
import onlinejudge_command.utils as utils

logger = getLogger(__name__)


@contextlib.contextmanager
def BufferedExecutor(lock: Optional[threading.Lock]):
    buf: List[Tuple[Callable, List[Any], Dict[str, Any]]] = []

    def submit(f, *args, **kwargs):
        nonlocal buf
        if lock is None:
            f(*args, **kwargs)
        else:
            buf += [(f, args, kwargs)]

    result = yield submit

    if lock is not None:
        with lock:
            for f, args, kwargs in buf:
                f(*args, **kwargs)
    return result


def write_result(input_data: bytes, output_data: Optional[bytes], *, input_path: pathlib.Path, output_path: pathlib.Path, print_data: bool, lock: Optional[threading.Lock] = None) -> None:
    # acquire lock to print logs properly, if in parallel
    nullcontext = contextlib.ExitStack()
    with lock or nullcontext:

        if not input_path.parent.is_dir():
            os.makedirs(str(input_path.parent), exist_ok=True)

        if print_data:
            logger.info(utils.NO_HEADER + 'input:')
            logger.info(utils.NO_HEADER + '%s', pretty_printers.make_pretty_large_file_content(input_data, limit=40, head=20, tail=10, bold=True))
        with input_path.open('wb') as fh:
            fh.write(input_data)
        logger.info(utils.SUCCESS + 'saved to: %s', input_path)

        if output_data is not None:
            if print_data:
                logger.info(utils.NO_HEADER + 'output:')
                logger.info(pretty_printers.make_pretty_large_file_content(output_data, limit=40, head=20, tail=10, bold=True))
            with output_path.open('wb') as fh:
                fh.write(output_data)
            logger.info(utils.SUCCESS + 'saved to: %s', output_path)


def check_status(info: Dict[str, Any], proc: subprocess.Popen, *, submit: Callable[..., None]) -> bool:
    submit(logger.info, 'time: %f sec', info['elapsed'])
    if proc.returncode is None:
        submit(logger.info, utils.FAILURE + utils.red('TLE'))
        submit(logger.info, 'skipped.')
        return False
    elif proc.returncode != 0:
        submit(logger.info, utils.FAILURE + utils.red('RE') + ': return code %d', proc.returncode)
        submit(logger.info, 'skipped.')
        return False
    assert info['answer'] is not None
    return True


def generate_input_single_case(generator: str, *, input_path: pathlib.Path, output_path: pathlib.Path, command: Optional[str], tle: Optional[float], name: str, lock: Optional[threading.Lock] = None) -> None:
    with BufferedExecutor(lock) as submit:

        # print the header
        submit(logger.info, '')
        submit(logger.info, '%s', name)

        # generate input
        submit(logger.info, 'generate input...')
        info, proc = utils.exec_command(generator, timeout=tle)
        input_data: bytes = info['answer']
        if not check_status(info, proc, submit=submit):
            return None

        # generate output
        if command is None:
            output_data: Optional[bytes] = None
        else:
            submit(logger.info, 'generate output...')
            info, proc = utils.exec_command(command, input=input_data, timeout=tle)
            output_data = info['answer']
            if not check_status(info, proc, submit=submit):
                return None

        # write result
        submit(write_result, input_data=input_data, output_data=output_data, input_path=input_path, output_path=output_path, print_data=True)


def simple_match(a: str, b: str) -> bool:
    if a == b:
        return True
    if a.rstrip() == b.rstrip():
        logger.warning('WA if no rstrip')
        return True
    return False


def try_hack_once(generator: str, command: str, hack: str, *, tle: Optional[float], attempt: int, lock: Optional[threading.Lock] = None) -> Optional[Tuple[bytes, bytes]]:
    with BufferedExecutor(lock) as submit:

        # print the header
        submit(logger.info, '')
        submit(logger.info, '%d-th attempt', attempt)

        # generate input
        submit(logger.info, 'generate input...')
        info, proc = utils.exec_command(generator, stdin=None, timeout=tle)
        input_data: Optional[bytes] = info['answer']
        if not check_status(info, proc, submit=submit):
            return None
        assert input_data is not None

        # generate output
        submit(logger.info, 'generate output...')
        info, proc = utils.exec_command(command, input=input_data, timeout=tle)
        output_data: Optional[bytes] = info['answer']
        if not check_status(info, proc, submit=submit):
            return None
        assert output_data is not None

        # hack
        submit(logger.info, 'hack...')
        info, proc = utils.exec_command(hack, input=input_data, timeout=tle)
        answer: str = (info['answer'] or b'').decode()
        elapsed: float = info['elapsed']
        memory: Optional[float] = info['memory']

        # compare
        status = 'AC'
        if proc.returncode is None:
            submit(logger.info, 'FAILURE: ' + utils.red('TLE'))
            status = 'TLE'
        elif proc.returncode != 0:
            logger.info(utils.FAILURE + '' + utils.red('RE') + ': return code %d', proc.returncode)
            status = 'RE'
        expected = output_data.decode()
        if not simple_match(answer, expected):
            logger.info(utils.FAILURE + '' + utils.red('WA'))
            logger.info(utils.NO_HEADER + 'input:\n%s', pretty_printers.make_pretty_large_file_content(input_data, limit=40, head=20, tail=10, bold=True))
            logger.info(utils.NO_HEADER + 'output:\n%s', pretty_printers.make_pretty_large_file_content(answer.encode(), limit=40, head=20, tail=10, bold=True))
            logger.info(utils.NO_HEADER + 'expected:\n%s', pretty_printers.make_pretty_large_file_content(output_data, limit=40, head=20, tail=10, bold=True))
            status = 'WA'

        if status == 'AC':
            return None
        else:
            return (input_data, output_data)


def generate_input(args: argparse.Namespace) -> None:
    if args.hack and not args.command:
        raise RuntimeError('--hack must be used with --command')

    if args.name is None:
        if args.hack:
            args.name = 'hack'
        else:
            args.name = 'random'

    if args.count is None:
        if args.hack:
            args.count = 1
        else:
            args.count = 100

    def iterate_path():
        for i in itertools.count():
            name = '{}-{}'.format(args.name, str(i).zfill(args.width))
            input_path = fmtutils.path_from_format(args.directory, args.format, name=name, ext='in')
            output_path = fmtutils.path_from_format(args.directory, args.format, name=name, ext='out')
            if not input_path.exists() and not output_path.exists():
                yield (name, input_path, output_path)

    # generate cases
    if args.jobs is None:
        for name, input_path, output_path in itertools.islice(iterate_path(), args.count):
            if not args.hack:
                # generate serially
                generate_input_single_case(args.generator, input_path=input_path, output_path=output_path, command=args.command, tle=args.tle, name=name)

            else:
                # hack serially
                for attempt in itertools.count(1):
                    data = try_hack_once(args.generator, command=args.command, hack=args.hack, tle=args.tle, attempt=attempt)
                    if data is not None:
                        write_result(*data, input_path=input_path, output_path=output_path, print_data=False)
                        break
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
            lock = threading.Lock()
            futures: List[concurrent.futures.Future] = []

            if not args.hack:
                # generate concurrently
                for name, input_path, output_path in itertools.islice(iterate_path(), args.count):
                    futures += [executor.submit(generate_input_single_case, args.generator, input_path=input_path, output_path=output_path, command=args.command, tle=args.tle, name=name, lock=lock)]
                for future in futures:
                    future.result()

            else:
                # hack concurrently
                attempt = 0
                for _ in range(args.jobs):
                    attempt += 1
                    futures += [executor.submit(try_hack_once, args.generator, command=args.command, hack=args.hack, tle=args.tle, attempt=attempt, lock=lock)]
                for _, input_path, output_path in itertools.islice(iterate_path(), args.count):
                    data = None
                    while data is None:
                        concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
                        for i in range(len(futures)):
                            if not futures[i].done():
                                continue
                            data = futures[i].result()
                            attempt += 1
                            futures[i] = executor.submit(try_hack_once, args.generator, command=args.command, hack=args.hack, tle=args.tle, attempt=attempt, lock=lock)
                            if data is not None:
                                break
                    write_result(*data, input_path=input_path, output_path=output_path, print_data=False, lock=lock)
