import inflection


class Device:
    def __init__(self, addr, id):
        super().__init__()
        self.addr = addr
        self.id = id

    def __repr__(self):
        addr = f'w:{self.addr}:' if self.addr is not None else ''
        name = self.__class__.__name__.split('Device')[0]
        id = f':{self.id}' if self.id is not None else ''
        return addr + inflection.underscore(name) + id


class AnyDevice(Device):
    pass


class CpuDevice(Device):
    pass


class CudaDevice(Device):
    def __init__(self, addr, id):
        super().__init__(addr, id)


_MAP_DEVICES = {
    ':any': AnyDevice,
    'cpu': CpuDevice,
    'cuda': CudaDevice,
}


def parse_device(device):
    if isinstance(device, (list, set)):
        if len(device) == 0:
            return [AnyDevice(None, None)]
        return [parse_device(d) for d in device]

    tokens = device.split(':')

    if tokens[0] == 'w':
        addr = tokens[1]
        tokens = tokens[2:]
    else:
        addr = None

    id = None

    if len(tokens) == 0:
        name = ':any'
    elif len(tokens) == 1:
        name = tokens[0]
    elif len(tokens) == 2:
        name = tokens[0]
        id = int(tokens[1])
    else:
        raise Exception(f'unparsable device: {device}')

    if name not in _MAP_DEVICES:
        raise Exception(f'no such device type: {name}')
    return _MAP_DEVICES[name](addr, id)
