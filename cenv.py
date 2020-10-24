import os
import argparse
import subprocess

root_folder = os.path.join("c:" + os.sep, "Users", "R", "Documents", "CondaEnvironments")


def check_environment_filename_or_path(value: str) -> str:
    """[summary]

    Parameters
    ----------
    value : str
        environment yml path like "C:\\Users\\R\\Documents\\CondaEnvironments\\environment_pyt.yml",
        or just the environment name like "pyt"

    Returns
    -------
    str
        environment yml path
    """
    if os.path.exists(value) and value.endswith('.yml'):
        # passed in filename
        return value
    else:
        if os.path.isabs(value):
            # passed in filename but doesn't exist
            raise argparse.ArgumentTypeError(f"'{value}' is not a valid path to an environment yml")
            
        # passed in env name 
        filename = os.path.join(root_folder, f"environment_{value}.yml")
        if os.path.exists(filename):
            return filename
        
        else:
            # env name doesn't match any
            raise argparse.ArgumentTypeError(f"environment_{value}.yml was not found in folder '{root_folder}'")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(epilog=f"save folder: '{root_folder}'")
    
    subparsers = parser.add_subparsers(help="Commands", dest='command')
    
    parser_save = subparsers.add_parser("save", help="Export current activated conda env to environment file")

    parser_restore = subparsers.add_parser("restore", help="Create conda env from environment file name or path")
    parser_restore.add_argument("env", type=check_environment_filename_or_path, help="Pass in a path to an environment file or the env name that was saved")
    parser_restore.add_argument("--new-name", default=None, help="Create conda env with new name")
    # and another argument for new name of env to be created based off of old name
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        exit()
    
    if args.command == "save":
        conda_env = os.environ.get("CONDA_DEFAULT_ENV")
        if conda_env is None:
            raise Exception("Not in a conda environment")
        else:
            filename = os.path.join(root_folder, f"environment_{conda_env}.yml")
            stdout_file = open(filename, "w")
            subprocess.call(["conda", "env", "export", "--from-history"], stdout=stdout_file)
            print(f"Backed up to {filename}")
    elif args.command == "restore":
        if args.new_name is not None:
            all_lines = None
            with open(args.env, "r") as f:
                # change name: to new_name
                all_lines = f.readlines()
                
            # change first line
            colon_idx = all_lines[0].index(':')
            new_first_line = all_lines[0][0:colon_idx + 2] + args.new_name + "\n"
            all_lines[0] = new_first_line
            
            filename, ext = os.path.splitext(args.env)
            mod_filename = f"{filename}_mod{ext}"
            with open(mod_filename, "w") as f:
                f.writelines(all_lines)
                
            subprocess.call(["conda", "env", "create", "-f", mod_filename], shell=True)
            
            os.remove(mod_filename)
        else:   
            subprocess.call(["conda", "env", "create", "-f", args.env], shell=True)
