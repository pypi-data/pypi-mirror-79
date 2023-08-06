#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = ['ClientSSH', 'create_arg_parser']

import argparse  # https://docs.python.org/3/library/argparse.html
import os
import platform
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn, Optional, Tuple

import paramiko

from procamora_utils.logger import get_logging, logging

logger: logging = get_logging(False, 'client_ssh')


def create_arg_parser() -> argparse:
    """
    Metodo para establecer los argumentos que necesita la clase
    :return:
    """
    example = "python3 %(prog)s -i 192.168.1.20 -u ubnt -p ubnt -c w"

    my_parser = argparse.ArgumentParser(
        description='%(prog) a is a script to automate the remote execution of commands through ssh',
        usage='{}'.format(example))

    requiered = my_parser.add_argument_group('requiered arguments')
    requiered.add_argument('-i', '--ip', help='IP address.')
    requiered.add_argument('-u', '--user', help='Username')
    requiered.add_argument('-p', '--pwd', help='Password')
    requiered.add_argument('-c', '--cmd', help='command to execute')

    my_parser.add_argument('-k', '--key', help='Path to certificate')
    my_parser.add_argument('-port', '--port', help='SSH port', default=22)
    my_parser.add_argument('-s', '--sudo', action='store_true', help='Run with sudo', default=False)
    my_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose flag (boolean).', default=False)

    if len(sys.argv) == 1:
        my_parser.print_help()
        sys.exit(1)
    return my_parser.parse_args()


@dataclass
class ClientSSH:
    ip: str
    port: int = 22
    debug: bool = False
    client: paramiko.client.SSHClient = paramiko.SSHClient()

    def __post_init__(self) -> NoReturn:
        if not self.is_online():
            logger.critical(f'client: {self.ip} is down!')
            # sys.exit(1)

        if self.debug:
            paramiko.util.log_to_file('paramiko.log')
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def is_online(self) -> int:
        """
        Funcion que comprueba si un equipo esta online o no
        return bool: Retorna 0 si el servidor esta online, 1 en caso contrario
        """
        if platform.uname()[0] == 'Windows':
            cmd: str = f'ping -n 1 {self.ip} | find "TTL=" > NUL'
        else:
            cmd: str = f'ping -c 1 {self.ip} | grep ttl > /dev/null'

        response: int = os.system(cmd)
        # and then check the response...
        if self.debug:
            if response == 0:
                print(f'{self.ip} is up!!')
            else:
                print(f'{self.ip} is down :(')
        return response == 0

    def execute_command(self, user: str, password: str = 'admin', cert: Path = None, command: str = 'w',
                        sudo: bool = False) -> Tuple[str, int]:
        """
        Funcion para establecer una conexion ssh, son necesarios los 4 primeros
        argumentos, depende de la libreria de cosecha propia TestPing

        :return str, int: retorna un int con el codigo y un string con el resultado
            0 : ejecucion de self.command correcta
            -1: server offline
            -2: fallo autenticacion
            -3: self.command invalido
            -4: Error desconocido
        """

        try:

            if cert is None:  # Modo credencial requiere user y pass
                self.client.connect(self.ip, self.port, user, password, allow_agent=False, look_for_keys=False)
            else:  # Modo certificado requiere usuario, certificado y password (opcional)
                key = paramiko.RSAKey.from_private_key_file(str(cert), password=password)
                self.client.connect(hostname=self.ip, username=user, pkey=key)
        except paramiko.AuthenticationException:
            message: str = f'Authentication failed: {user}/{password}'
            logger.critical(message)
            return message, -2
        except Exception as e:
            message: str = f'{e}'
            logger.critical(message)
            return message, -4

        if sudo:
            stdin, stdout, stderr = self.client.exec_command(f'echo {password} | sudo -S {command}')
        else:
            stdin, stdout, stderr = self.client.exec_command(command)

        stdout = stdout.read()[:]
        stderr = stderr.read()[:]
        self.client.close()

        if re.search(r'bash: .*: command not found', str(stderr)):
            message: str = f'command invalid: {command}'
            logger.critical(message)
            return message, -3
        # hago una copia explicita del valor ya que sino cuando cierro
        # la conexion ssh pierdo el valor
        else:
            message: str = f'{self.format_text(stdout)}'
            return message, 0

    @staticmethod
    def format_text(param_text: bytes) -> Optional[str]:
        if param_text is not None:
            text = param_text.decode('utf-8')
            return str(text)
            # return text.replace('\n', '')
        return param_text


def main():
    args = create_arg_parser()

    ssh: ClientSSH = ClientSSH(args.ip, args.port, args.verbose)
    output = ssh.execute_command(user=args.user, password=args.pwd, cert=args.key, sudo=args.sudo)
    print(output)


if __name__ == '__main__':
    main()
