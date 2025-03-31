import pathlib
path = pathlib.Path().resolve()
import yaml 


config = yaml.load(open(str(path)+"/booleansearch/config.yaml",'r'), Loader=yaml.FullLoader)