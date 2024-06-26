Первая часть программы представляет <a href="sshpass_utils/ssh_executer.py">модуль для работы с утилитой
командной строки ‘sshpass’</a>:
- интерфейс предоставляет возможность задания пароля из файла и аргументом
командной строки;
- интерфейс предоставляет возможность для работы с подкомандой “ssh”, но
имеет возможность расширения для работы с подкомандой “scp”;
- таким образом модуль предоставляет возможность выполнения
любой удалённой команды. Результатом выполнения команды будет распаршенный
stdout, stderr, return code.

Используя предыдущий модуль, была разработана <a href="iperf_utils/iperf_executer.py">утилита командной строки, которая
измеряет пропускную способность</a> сети между двумя хостами.
- для измерения пропускной способности используется утилита iperf3;
- построение и парсинг результатов команды iperf3 находится в отдельном
модуле;
- входными параметрами утилиты являются IP/hostname узлов сети и
пароли/пользователи для доступа к ним;
- результатом выполнения команды является следующая структура:
{
 'error': str('Description of error if exist'),
 'result': 'json with hostnames, IPs, Interval, Transfer, Bandwidth',
 'status': int('0 in case of success and ANY in all other cases')
}
- В конце выполнения утилиты осуществляется контроль за отключением сервера
“iperf3” после окончания измерений.

<a href="tests">Тесты</a>
