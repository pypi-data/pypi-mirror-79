from .base import Base

from json import dumps

import batik.remote.deployment 

import os 
import tarfile

from pprint import pprint

class Deployment(Base):
    """Deployment"""

    def run(self):
        id = self.options.get("<deployId>")
        res = batik.remote.deployment.get_deployment(id)
        print("Deployment")
        pprint(res)

        if(self.options["download"]):
            batik.remote.deployment.download(id, res.manifest)