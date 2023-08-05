# -*- coding: utf-8 -*-
import logging
import os
import yaml

from sarge import run


try:
    import appdirs
except ModuleNotFoundError:
    print(
        "appdirs missing - should the issue persists post install, "
        "run `pip install appdirs` manually"
    )

try:
    from pyfiglet import Figlet
except ModuleNotFoundError:
    Figlet = None


class Balic(object):
    """Balic is a toolset for working with LXC containers.
    It creates, builds and destroys LXC containers.
    """

    __version__ = "0.0.4"

    __config__ = """
---
# Log level: debug, info, warning, error, critical
log_level: info

# LXC directory
lxc_dir: ~/.local/share/lxc

# subuid subgid
subuid: 100000
subgid: 100000
        """

    def __init__(self, name):
        """Initializes Balic object with its configuration.
        """
        self.log_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        self.local_path = os.getcwd()
        self.global_path = os.path.join(appdirs.user_config_dir(), "balic")

        self.config_file = "balic.yml"
        self.config_dot_file = ".balic.yml"

        self.loaded_config_file = None

        self.config = None
        self.configure()

        self.name = name
        self.lxc_dir = os.path.expanduser(self.config["lxc_dir"])
        self.rootfs = os.path.abspath(
            f"{self.lxc_dir}/{self.name}/rootfs"
        )
        self.balic_dir = os.path.abspath(
            f"{self.rootfs}/tmp/balic"
        )
        self.build_dir = os.path.abspath(
            f"/tmp/balic"
        )
        self.build_script = os.path.abspath(
            f"{self.build_dir}/build.sh"
        )

    def configure(self):
        """Tries to load Balic configuration from current working directory
        then user config directory and if none found it defaults to internal
        configuration stored in ``Balic.__config__``.
        """

        def loadrc(config_file):
            self.config = yaml.safe_load(open(config_file, "r"))
            self.loaded_config_file = config_file

        try:
            loadrc(self.config_dot_file)
        except FileNotFoundError:
            try:
                loadrc(self.config_file)
            except FileNotFoundError:
                try:
                    loadrc(
                        os.path.join(self.global_path, self.config_dot_file)
                    )
                except FileNotFoundError:
                    try:
                        loadrc(
                            os.path.join(self.global_path, self.config_file)
                        )
                    except FileNotFoundError:
                        self.config = yaml.safe_load(self.__config__)
                        self.loaded_config_file = "default"

        self.get_logger()

    def get_logger(self):
        """Sets up logger
        """
        logging.basicConfig()

        self.log = logging.getLogger(__name__)

        log_level = self.log_levels["INFO"]
        if "log_level" in self.config:
            log_level = self.log_levels[self.config["log_level"].upper()]
            self.log.debug(
               f"Set logging to {self.config['log_level'].upper()}"
            )

        self.log.setLevel(log_level)

    @staticmethod
    def get_parser(parser):
        """Returns parser with base Balic's arguments:

        * ``-n`` ``--name`` container name
        """
        parser.add_argument("-n", "--name")
        return parser

    def ls(self, list_all=False):
        """List linux containers.
        """
        if list_all is True:
            run(f"lxc-ls -f")
        else:
            run(f"lxc-ls -n {self.name} -f")

    def create(self):
        """Creates base Debian Buster (amd64) container.
        """
        run(
            f"lxc-create -n {self.name} -t download -- "
            f"--dist debian --release buster --arch amd64"
        )

    def build(self, build_dir):
        """Runs build.sh that must be present in the given
        build_dir which is copied over into the Linux container.

        The process firstly starts the container and waits for 3 seconds
        for the networking being established.

        build_dir can contain any number of files and directories
        to be copied into the container.

        Once the build directory is copied inside the container
        build.sh is run from inside the container.

        Once the process is finished the container is stopped.
        """
        run(f"lxc-start -n {self.name} && sleep 3")

        run(f"lxc-attach -n {self.name} -- rm -r {self.build_dir}")

        run(f"sudo cp -rv {build_dir} {self.balic_dir}")
        run(f"sudo chown "
            f"{self.config['subuid']}:{self.config['subgid']} "
            f"{self.balic_dir} -Rv")

        run(f"lxc-attach -n {self.name} -- /bin/sh {self.build_script}")

        run(f"lxc-stop -n {self.name}")

    def pack(self, output_file):
        """Packs Linux container to given output file.

        Output file format is .tar.gz
        """
        cmd = (
            f"cd {self.rootfs} && "
            f"sudo tar czf {output_file} *"
        )
        run(cmd, shell=True)

    def destroy(self):
        """Destroys container.
        """
        run(f"lxc-destroy -n {self.name}")
