class IncompleteMessageError(Exception):
    pass


def message_to_rpms(message):
    durations = parse_durations(message=message)
    rpms = [duration2rpm(duration) for duration in durations]
    return rpms


def parse_durations(message):
    # if there is a line break in the message, parse the longest part
    if False and '\r' in message:
        sub_messages = message.split('\r')
        message = ''
        for sub_message in sub_messages:
            if message.count(':') == 0:
                message = sub_message
            if message.count(';') < sub_message.count(';'):
                message = sub_message

    if False and message.count(':') > 1:
        messages = message.split(':')
        if len(messages[0]) > len(messages[1]):
            message = message[0]
        else:
            message = message[1]

    if False and not message.count(";") >= 3:
        raise IncompleteMessageError(message)

    if not message.count(":") >= 1:
        raise IncompleteMessageError(message)

    if False and not message.startswith(':'):
        message = message.split(':')[1]

    message = message.lstrip(':')
    rpms = message.split(';')

    rpms = rpms[:-1] if rpms[-1] == '' else rpms
    return rpms


def duration2rpm(duration):
    duration = int(duration)
    if duration == 0:
        return duration
    rpm = 1000000 / duration / 2 * 60
    rpm = int(rpm)
    return rpm


def signum(int):
    if (int < 0):
        return -1
    elif (int > 0):
        return 1
    else:
        return 0


def format_fans(fans):
    return format_line(prefix='fans'.rjust(12), values=fans)


def format_rpms(rpms):
    return format_line(prefix='rpms'.rjust(12), values=rpms)


def format_pwms(pwms):
    return format_line(prefix='pwms'.rjust(12), values=pwms)


def format_tmps(tmps):
    return format_line(prefix='temps'.rjust(12), values=tmps)


def format_names(names):
    return format_line(prefix='names'.rjust(12), values=names)


def format_ports(ports):
    return format_line(prefix='ports'.rjust(12), values=ports)


def format_temps(temps):
    # temps = [round(temp, 1) for temp in temps]
    return format_line(prefix='temps'.rjust(12), values=temps)


def format_limits(limits):
    return format_line(prefix='limits'.rjust(12), values=limits)


def format_buffers(buffers):
    return format_line(prefix='buffers'.rjust(12), values=buffers)


def format_hysteresises(hysteresises):
    return format_line(prefix='hysteresises'.rjust(12), values=hysteresises)


def format_decisions(decisions):
    return format_line(prefix='decisions'.rjust(12), values=decisions)


def format_directions(directions):
    return format_line(prefix='directions'.rjust(12), values=directions)


def format_differences(differences):
    return format_line(prefix='differences'.rjust(12), values=differences)


def format_pwms_new(pwms_new):
    return format_line(prefix='new pwms'.rjust(12), values=pwms_new)


def format_line(prefix, values):
    string = ''
    string += prefix
    string += ': '
    string += '['
    for value in values:
        value = str(value) if value is not None else ''
        string += value.rjust(6)
        string += ', '
    string = string[:-len(', ')]
    string += ']'

    return string


def clip_pwm(pwm):
    return clip(pwm, 0, 255)


def clip(value, minimum, maximum):
    value = sorted([minimum, value, maximum])[1]
    return value


def pwms_to_message(pwms):
    '''
    pwms = [90, 180, 180, None, 180, None, None, None]
    message = '090;180;180;123;180;123;123;123'
    '''
    pwms = [pwm if pwm is not None else 123 for pwm in pwms]
    pwms = [str(pwm) for pwm in pwms]
    message = ';'.join(pwms)
    return message
