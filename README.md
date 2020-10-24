# Conda Export Env

* Easy way to export environment file

* I hardcoded the save folder in the script, so if there is a better way please tell me

* Tip: add this script to a folder in path to use it anywhere, or add this folder to path

* Note: you must be activated in the conda environment that you want to export for save mode, and you must be activated in any conda environment for restore mode (in case you are getting HTTP000 error)

## Usage

```
usage: cenv.py [-h] {save,restore} ...

positional arguments:
  {save,restore}  Commands
    save          Export current activated conda env to
                  environment file
    restore       Create conda env from environment file
                  name or path

optional arguments:
  -h, --help      show this help message and exit

save folder: 'c:\Users\R\Documents\CondaEnvironments'
```



### Restore mode
```
usage: cenv.py restore [-h] [--name NAME] env

positional arguments:
  env                  Pass in a path to an environment file or the env name that was saved

optional arguments:
  -h, --help           show this help message and exit
  --name NEW_NAME  Create conda env with new name
```
