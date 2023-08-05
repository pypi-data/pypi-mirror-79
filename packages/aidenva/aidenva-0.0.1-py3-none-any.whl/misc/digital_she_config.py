import yaml
import os
import logging
import service.constants as const

RUNTIME_DEFAULT_PROFILE = 'default'
DEFAULT_CONFIG_PATH = 'conf'
CONFIG_FILE = 'config-%s.yml'

systemlogger = logging.getLogger('system')
trace = logging.getLogger('trace')

class DSConfig():
    def __init__(self, profile, conf_path, display=True):
        if profile is None :
            self.profile = RUNTIME_DEFAULT_PROFILE
        else:
            self.profile = profile

        if conf_path is None:
            config_path = os.path.join(DEFAULT_CONFIG_PATH, (CONFIG_FILE % self.profile))
        else :
            config_path = os.path.join(conf_path, (CONFIG_FILE % self.profile))

            trace.info(' configuration file path : %s', config_path)
        with open(config_path, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
        if display:
            self.print_config()

    # def getvalue(self, section, key):
    #     return self.config[section][key]

    # def getlist(self, section, key, split=','):
    #     return self.config[section][key].split(split)

    def __getvalue(self, key, default=None):
        keys = key.split('.')

        try:
            if len(keys) == 1:
                return self.config[keys[0]]
            elif len(keys) == 2:
                return self.config[keys[0]][keys[1]]
            elif len(keys) == 3:
                return self.config[keys[0]][keys[1]][keys[2]]
            elif len(keys) == 4:
                return self.config[keys[0]][keys[1]][keys[2]][keys[3]]
            elif len(keys) == 5:
                return self.config[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]]
            elif len(keys) == 6:
                return self.config[keys[0]][keys[1]][keys[2]][keys[3]][keys[4]][keys[5]]
        except Exception as e:
            if default is not None:
                return default
            else:
                raise Exception(__name__ + ' DSConfig key not found [%s]' % key, e)

    def __value_function(func):
        def func_2(*args, **kwargs):
            return func(*args, **kwargs)
        return func_2

    def __list_function(func):
        def func_1(*args, **kwargs):
            return [x.strip() for x in func(*args, **kwargs).split(',')]
        return func_1

    def __bool_function(func):
        def func_1(*args, **kwargs):
            b = func(*args, **kwargs)
            if isinstance(b, bool) :
                return b
            else :
                return (b == 'True')
        return func_1

    @__value_function
    def getvalue(self, key, default=None):
        return self.__getvalue(key, default)

    @__list_function
    def getlist(self, key):
        return self.__getvalue(key)

    @__bool_function
    def getbool(self, key):
        return self.__getvalue(key)

    # def get_section(self, section):
    #     def getvalue(key):
    #         return self.config[section][key]
    #
    #     return getvalue


    def print_config(self):
        systemlogger.info('*****************************************************************************')
        systemlogger.info('*  _____   _       _           _       _    _     _ _______    _    _       *')
        systemlogger.info('* (____ \ (_)     (_)_        | |     | |  | |   | (_______)  | |  | |/\    *')
        systemlogger.info('*  _   \ \ _  ____ _| |_  ____| |      \ \ | |__ | |_____     | |  | /  \   *')
        systemlogger.info('* | |   | | |/ _  | |  _)/ _  | |       \ \|  __)| |  ___)     \ \/ / /\ \  *')
        systemlogger.info('* | |__/ /| ( ( | | | |_( ( | | |   _____) ) |   | | |_____     \  / |__| | *')
        systemlogger.info('* |_____/ |_|\_|| |_|\___)_||_|_|  (______/|_|   |_|_______)     \/|______| *')
        systemlogger.info('*           (_____|                                                         *')
        systemlogger.info('*************************************************************************** *')
        systemlogger.info('Activated profiles : [%s]' % self.profile)
        systemlogger.info('GPU memory fraction : [%0.2f]' % self.getvalue('va_engines.gpu_mem_fraction', const._GPU_MEM_FRACTION))
        self.__print_vaengine_enabled()

    def __print_vaengine_enabled(self):
        engines = self.config['va_engines']['engines']

        for key in engines:
            systemlogger.info('VA [%-10s] enabled : %s', key, engines[key]['enabled'])


