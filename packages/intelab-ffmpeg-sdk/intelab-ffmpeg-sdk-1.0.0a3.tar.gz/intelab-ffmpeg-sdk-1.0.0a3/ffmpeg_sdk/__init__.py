import subprocess
import errno

try:
    from intelab_python_sdk.logger import log
except ImportError:
    import logging
    log = logging.getLogger('ffmpeg')
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.DEBUG)


def run_shell(cmd, name='ffmpeg'):
    """
    运行ffmpeg shell
    :param cmd:
    :param name:
    :return:
    """
    try:
        log.info(cmd)
        ffmpeg_proc = subprocess.Popen(cmd, shell=True,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, bufsize=1)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise "Executable '{0}' not found".format('ffmpeg')
        else:
            raise

    # 实时打印ffmpeg日志
    return_code = ffmpeg_proc.poll()
    log_buffer = error_log = ''

    while return_code is None:
        # 这里会阻塞,所以不用获取所有的日志才返回，获取81个字节就可以返回了！
        line = ffmpeg_proc.stdout.readline(81)
        log_buffer += line.decode()

        if r'\n' in str(line):
            if 'Impossible to open' in log_buffer:
                error_log = log_buffer
            log.debug('%s:%s', name, log_buffer.strip())
            log_buffer = ''

        return_code = ffmpeg_proc.poll()
    return error_log
