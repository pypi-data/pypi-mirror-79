import click
import json
import subprocess
import sys

def load_json(file):
    # FEATURE: hashtag in string is recognized as comment
    with open(file) as f:
        ls=f.readlines()
    
    wo_comments=[]
    for l in ls:
        if '#' in l:
            l=l[:l.index('#')]
        elif l.endswith("\n"):
            l=l[:-1]
        wo_comments.append(l)
    jtd = "\n".join(wo_comments)
    print(jtd)
    j = json.loads(jtd.strip())
    return j
def dump_as_file(j, f):
    if 'json' in j:
        with open(f, "w") as fo:
            json.dump(j["json"], fo)
    else:
        raise ValueError("unrecognized format in {}".format(j))

def process_list(j):
    rval=[]
    if j is None:
        return rval
    
    for k,v in j.items():
        if isinstance(v, dict):
            if "path" in v:
                dump_as_file(v, v['path'])
                rval.append((k,v["path"]))
        else:
            rval.append((k,v))
    return rval

def add(file):
    # FEATURE: hashtag in string is recognized as comment

    j = load_json(file)
    ins = process_list(j.get("input"))
    outs = process_list(j.get("output"))
    args = process_list(j.get("args"))

    target= j["command"]["python"]

    dvc_args=["dvc","run","-f",file[:-4]+"dvc"]

    #add dependency on this file:
    dvc_args.append("-d")
    dvc_args.append(file)

    # Add dependency on invoked file
    dvc_args.append("-d")
    dvc_args.append(target)

    for k,v in ins:
        dvc_args.append("-d")
        dvc_args.append(v)
    
    for k,v in outs:
        dvc_args.append("-o")
        dvc_args.append(v)
    
    python_arguments=[
        "python",
        target]

    for par in [ins, outs,args]:
        for k,v in par:
            python_arguments.append(k)
            if v is not None:
                python_arguments.append(v)
    
    conf =j.get("config",{})
    if "no-jdvc-arg" not in conf:
        python_arguments.append(conf.get("jdvc-arg-name","--jdvc"))
        python_arguments.append(file)
    
    def arg_escape(x):
        if " " in x:
            x='"{}"'.format(x)
        return x

    python_agruments_string = " ".join([arg_escape(x) for x in python_arguments])
    dvc_args.append(python_agruments_string)

    print(dvc_args)
    subprocess.check_call(dvc_args)




@click.command()
@click.argument('file_name', type=click.Path(file_okay=True, exists=True, ))
def main(file_name):
    
    if not file_name.endswith('.jdvc'):
        print("File must end with .jdvc")
        sys.exit(1)
    
    assert(file_name.endswith(".jdvc"))
    print("Processing:",file_name)
    add(file_name)

if __name__ == "__main__":
    
    main() 
