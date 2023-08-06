import os
import sys
from jinja2 import Template


def install(name, **kwargs):
    cliche_path = os.path.dirname(os.path.realpath(__file__))
    cwd = os.getcwd()
    bin_path = os.path.dirname(sys.argv[0])
    bin_name = os.path.join(bin_path, name)
    if os.path.exists(bin_name):
        raise FileExistsError(bin_name)
    template_path = os.path.join(cliche_path, "install_generator.py")
    with open(template_path) as f:
        template = Template(f.read())
    with open(bin_name, "w") as f:
        f.write(template.render(cwd=cwd, bin_name=bin_name, bin_path=bin_path))
    os.system("chmod +x " + bin_name)


def uninstall(name, **kwargs):
    bin_path = os.path.dirname(sys.argv[0])
    bin_name = os.path.join(bin_path, name)
    with open(bin_name) as f:
        txt = f.read()
        if "from cliche" not in txt:
            raise ValueError("This executable does not seem installed by cliche")
    os.remove(bin_name)
    os.remove(bin_name + ".cache")
