import argparse
import ast
import functools
import importlib
from logging import getLogger
import os
from pathlib import Path
from textwrap import dedent
import traceback
import sys
import types
from typing import Dict

import lsp
import trio

from .evaluation import capture_last_expression, aexec
from .resolution import ModuleResolveError, module_name_from_filename


_log = getLogger(__name__)


def main():
    import logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    _log.addHandler(ch)
    _log.setLevel(logging.INFO)

    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('-H', '--host', default=None)
    parser.add_argument('-p', '--port', default=6768, type=int)
    parser.add_argument('-f', '--portfile', default='./.lyre-port')
    args = parser.parse_args()

    sys.path.insert(0, '.')

    trio.run(functools.partial(
        run,
        host=args.host,
        port=args.port,
        portfile=args.portfile,
    ))


async def run(host=None, port=6768, portfile='./.lyre-port'):
    listeners = await trio.open_tcp_listeners(port, host=host)
    if portfile:
        with open(portfile, 'w') as f:
            for listener in listeners:
                host, port, *_ = listener.socket.getsockname()
                f.write(f'{host} {port}\n')
    try:
        await trio.serve_listeners(_handler, listeners)
    finally:
        if portfile:
            os.remove(portfile)


async def _handler(stream: trio.SocketStream):
    _log.info('connected')
    conn = lsp.Connection('server')
    recvsize = 4096
    try:
        while True:
            while True:
                event = conn.next_event()

                if event is lsp.NEED_DATA:
                    data = await stream.receive_some(recvsize)
                    if not data:
                        return
                    conn.receive(data)
                elif isinstance(event, lsp.RequestReceived):
                    ...
                elif isinstance(event, lsp.DataReceived):
                    ...
                elif isinstance(event, lsp.MessageEnd):
                    break

            _, body = conn.get_received_data()
            method = body.get('method', None)
            _log.debug(f'handling: {method}')
            if method == 'initialize':
                send_data = conn.send_json(dict(
                    id=body['id'],
                    result=dict(capabilities=dict()),
                ))
                await stream.send_all(send_data)
            elif method == 'shutdown':
                break
            elif method == 'lyre/eval':
                response = await _eval(body)
                send_data = conn.send_json(response)
                await stream.send_all(send_data)

            conn.go_next_circle()
    finally:
        _log.info('disconnected')


async def _eval(request: Dict) -> Dict:
    response = dict(id=request['id'])

    try:
        params = request['params']
        path = Path(params['path'])
        code = params['code']
        lineno = params.get('lineno', 1)
    except KeyError:
        # TODO: More precise error result.
        response['result'] = _error_result()
        return response

    try:
        modname = module_name_from_filename(path)
    except ModuleResolveError:
        response['result'] = _error_result()
        return response

    try:
        mod = importlib.import_module(modname)
    except Exception:
        print(f'import failed: {modname}')
        mod = sys.modules[modname] = types.ModuleType(
            modname, 'Synthetic module created by Lyre')
        mod.__file__ = str(path)

    # TODO: Would be nice to source map back to the indented version for
    #       SyntaxError exceptions, especially.
    code = dedent(code)

    try:
        node = ast.parse(code, str(path), 'exec')
        ast.increment_lineno(node, lineno - 1)
        capture_last_expression(node, '--lyre-result--')

        await aexec(node, str(path), mod.__dict__, mod.__dict__)
        value = mod.__dict__.pop('--lyre-result--', None)
        response['result'] = dict(status='ok', value=repr(value))
    except BaseException:
        response['result'] = _error_result()
    finally:
        mod.__dict__.pop('--lyre-result--', None)
    return response


def _error_result():
    etype, ex, tb = sys.exc_info()
    fmt_exc = traceback.format_exception_only(etype, ex)
    fmt_tb = traceback.format_tb(tb)

    return dict(
        status='error',
        error=fmt_exc[-1],
        fullError=fmt_exc,
        traceback=fmt_tb,
    )
