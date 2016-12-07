from createSamples import CreateSamples
from trainer import Trainer
import ConfigParser


# #load properties
config = ConfigParser.RawConfigParser()
config.read('../properties/main_config.properties')

# print config.get('samples', "rootPath")

# 1. create new train positive samples
a = CreateSamples("test", 10, 0.3, 0.3, 1.0, 40, 20, 40)
a.start()
t = Trainer('test', 100, 200, 10, 1000, 3000, 4, 0.0001, 20, 40, 'RAB', 0.998, 0.35, 0.95, 1, 150, 'LBP')
t.numPos = 10




