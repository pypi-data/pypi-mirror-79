"""
Create a new Project
"""
import os
import importlib
from pathlib import Path
from json import dumps
from .Base import Base
from inspect import getmembers
import sys
from distutils.dir_util import copy_tree
from ..util.Logger import classLogger, LogLevel

import pyPhases
from pyPhases import Project, Data

@classLogger
class Run(Base):
    """create a Phase-Project"""

    config = None
    projectFileName = "project.yaml"
    projectConfigFileName = "project.yaml"
    packagePath = os.path.dirname(sys.modules["phases"].__file__)
    forceWrite = False
    debug = False
    phaseName = None

    def run(self):
        self.beforeRun()
        self.prepareConfig()

        project = self.createProjectFromConfig(self.config)

        self.runProject(project)

    def parseRunOptions(self):
        if (self.options['-o']):
            self.outputDir = self.options['-o']
            sys.path.insert(0, self.outputDir)
            self.logDebug("Set Outputdir: %s" % (self.outputDir))
        if (self.options['-p']):
            self.projectFileName = self.options['-p']
            self.logDebug("Set Projectfile: %s" % (self.projectFileName))
        if (self.options['-c']):
            self.projectConfigFileName = self.options['-c']
            self.logDebug("Set Config file: %s" % (self.projectFileName))
        if (self.options['-v']):
            self.debug = True
        if "<phaseName>" in self.options:
            self.phaseName = self.options['<phaseName>']

    def beforeRun(self):
        self.parseRunOptions()

    def getPackagePath(self, path):
        d = os.path.dirname(sys.modules["phases"].__file__)
        return os.path.join(d, path)


    def loadClass(self, classOptions, pythonPackage=""):
        name = classOptions["name"]
        path = classOptions["package"]
        options = classOptions["config"] if "config" in classOptions else {}
        leadingDot = "" if classOptions["system"] else "."
        package = None if classOptions["system"] else pythonPackage
        sys.path.insert(0, self.outputDir)
        module = importlib.import_module("%s%s.%s"%(leadingDot, path, name), package=package)
        # module = importlib.import_module("%s.%s"%(path, name), package=None)
        classObj = getattr(module, name)

        if len(options) > 0:
            return classObj(options)
        else:
            return classObj()


    def getDataDefinition(self, dataObj):
        dependsOn = []
        if "dependsOn" in dataObj:
            for dependString in dataObj['dependsOn']:
                dependsOn.append(dependString)

                if dependString not in self.config['config'] and dependString not in Data.dataNames:
                    self.logWarning("Dependency '%s' for Data could not be found in any config or other defined data"%(dependString))


        return Data(dataObj["name"], dependsOn)

    def createProjectFromConfig(self, config):

        dataDefinitions = {}

        project = Project()
        project.debug = self.debug
        project.name = config["name"]
        project.namespace = config["namespace"]
        project.config = config["config"]

        for classObj in self.config["publisher"]:
            obj = self.loadClass(classObj, project.name)
            project.registerPublisher(obj)

        for classObj in self.config["exporter"]:
            obj = self.loadClass(classObj, project.name)
            project.registerExporter(obj)

        for classObj in self.config["storage"]:
            obj = self.loadClass(classObj, project.name)
            project.addStorage(obj)

        for stage in self.config["stages"]:
            project.addStage(stage)

        for dataObj in self.config["data"]:
            data = self.getDataDefinition(dataObj)
            dataDefinitions[dataObj["name"]] = data

        for phase in self.config["phases"]:
            obj = self.loadClass(phase, project.name)

            # add data
            if "exports" in phase:
                for dataName in phase["exports"]:
                    if dataName in dataDefinitions:
                        dataDef = dataDefinitions[dataName]
                    else:
                        dataDef = Data(dataName)

                    obj.exportData.append(dataDef)

            project.addPhase(obj, phase["stage"], phase["description"])

        return project

    def runProject(self, project):
        project.run(self.phaseName)
