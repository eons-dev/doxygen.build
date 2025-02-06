import os
import logging
import jsonpickle
from pathlib import Path
from distutils.file_util import copy_file
from distutils.dir_util import copy_tree
from ebbs import Builder
from ebbs import OtherBuildError

# Class name is what is used at cli, so we defy convention here in favor of ease-of-use.
class doxygen(Builder):
    def __init__(this, name="Doxygen Documentation Builder"):
        super().__init__(name)

        this.clearBuildPath = True

        this.optionalKWArgs["doxygen_conf"] = "doxygen.conf"
        this.optionalKWArgs["style"] = ""

        this.supportedProjectTypes = [] #all


    # Required Builder method. See that class for details.
    def DidBuildSucceed(this):
        result = this.outputPath
        logging.debug(f"Checking if build was successful; output should be {result}")
        return os.listdir(result)

    # Required Builder method. See that class for details.
    def Build(this):

        this.outputPath = os.path.join(this.buildPath, "out")
        Path(this.outputPath).mkdir(parents=True, exist_ok=True)

        logging.debug(f"Building in {this.buildPath}")
        logging.debug(f"Packaging in {this.outputPath}")

        this.GetStyle()
        this.Configure()
        this.GenerateDocs()

    def GetStyle(this):
        if (not len(this.style)):
            # Assume we're already in the styled directory.
            return

        #TODO: Make it so that the repo_store is not cluttered with configuration files.
        styleSourcePath = this.executor.args.repo_store

        if (not os.path.exists(os.path.join(styleSourcePath, this.doxygen_conf))):
            logging.debug(f"{this.doxygen_conf} not found in {styleSourcePath}; attempting to download style.")
            this.executor.DownloadPackage(f"style_{this.style}", registerClasses=False)

        if (not os.path.exists(styleSourcePath)):
            raise OtherBuildError(f"Could not find style_{this.style}")

        # This nonsense is required because we need `cp incPath/* buildpath/` behavior instead of `cp incPath buildpath/`
        # TODO: is there a better way?
        # FIXME: distutils has been removed from python 3.12
        for thing in os.listdir(styleSourcePath):
            thingPath = os.path.join(styleSourcePath, thing)
            destPath = os.path.join(this.buildPath, thing)
            if os.path.isfile(thingPath):
                if (Path(thingPath).suffix == ".py"):
                    continue #TODO: See above todo about cluttering repo_store.
                copy_file(thingPath, destPath)
            elif os.path.isdir(thingPath):
                copy_tree(thingPath, destPath)

    def Configure(this):
        if (not os.path.isfile(this.doxygen_conf)):
            raise OtherBuildError(f"Could not find {this.doxygen_conf}")

        confFile = open(this.doxygen_conf, 'r')
        confData = confFile.read()
        confFile.close()

        confFile = open(this.doxygen_conf, 'w')
        for line in confData:
            if (line.startswith("PROJECT_NAME")):
                confFile.write(f"PROJECT_NAME = {this.projectName}")
                continue
            confFile.write(line)
        confFile.close()

    def GenerateDocs(this):
        this.RunCommand(f"doxygen {this.doxygen_conf}")
