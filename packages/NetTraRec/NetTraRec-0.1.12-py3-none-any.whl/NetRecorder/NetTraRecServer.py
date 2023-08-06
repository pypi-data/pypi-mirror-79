import os
from argparse import ArgumentParser, RawTextHelpFormatter

from NetRecorder.gear_for_nr import tell_the_datetime


def record_starter_server():
    dp = '    这是一个查看或者返回服务器流量信息的工具，以服务的方式启动，默认使用推 redis 的方式，单位为 bytes/m\n' \
         '    https://github.com/ga1008/net_tracfic_recorder'
    da = ""
    parser = ArgumentParser(description=dp, formatter_class=RawTextHelpFormatter, add_help=True)
    parser.add_argument("-n", "--net_devices", type=str, dest="net_devices", default='eth0,enp2s0',
                        help=f'{da}指定网络设备，默认 eth0。多个值使用英文逗号 "," 隔开\n')
    parser.add_argument("-u", "--unit", type=str, dest="unit", default='bytes',
                        help=f'{da}指定流量单位，auto/bytes/kb/mb/gb，默认bytes\n')
    parser.add_argument("-rf", "--refresh_rate", type=str, dest="refresh_rate", default='m',
                        help=f'{da}统计频率，h/m/s (时/分/秒)，默认m\n')
    parser.add_argument("-pr", "--push_redis", type=str, dest="push_redis", default='y', nargs='?',
                        help=f'{da}y/n。将结果推入指定的redis，默认n。如果设置了此参数，则接下来需要提供目标redis的信息\n')
    parser.add_argument("-kp", "--key_params", type=str, dest="key_params", default='local',
                        help=f'{da}关键参数提供方式，input/local/now，\n'
                             f'input是随后输入，\n'
                             f'local是在本地redis的"NetRec_key_params"内寻找，\n'
                             'now是后面直接跟上>>>>参数字典，例如：now>>>>{"host": "127.0.0.1", "port": ..., "db": ...}，'
                             'now方式仅限测试\n'
                             f'默认input\n')
    args = parser.parse_args()
    unit = args.unit
    refresh_rate = args.refresh_rate.lower()
    push_to_redis = args.push_redis
    key_params_mode = args.key_params
    try:
        log_dir = "~/"
        file_name = "NetTraRec.py"
        args_str = f"-u {unit} -rf {refresh_rate} -pr {push_to_redis} -kp {key_params_mode} -ps"
        run = f"~/miniconda/bin/python {os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name)} {args_str}"
        out_log_path = os.path.join(log_dir, f"{tell_the_datetime(compact_mode=True)}.out")
        run = f"nohup {run} > {out_log_path} &"

        res = os.popen(run).read()

    except KeyboardInterrupt:
        print('\n 退出 \n')
    except Exception as E:
        print(f"Error: {E}")
