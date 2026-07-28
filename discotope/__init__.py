# **************************************************************************
# *
# * Authors:     Enzo Sierra (enzogael57@gmail.com)
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************
"""
This package contains a protocol for structure-based (conformational)
B-cell epitope prediction using a local DiscoTope-3.0 installation.
"""

import os
import subprocess

from scipion.install.funcs import InstallHelper

from pwchem import Plugin as pwchemPlugin

from .constants import DISCOTOPE_DIC, NOINSTALL_WARNING, UPSTREAM_URL

_references = ['Hoie2024']


class Plugin(pwchemPlugin):
    """DiscoTope-3.0 is installable directly via git and pip (CC BY-NC 4.0
    license, free for academic use, no academic-request form required):
    installed automatically by cloning the upstream repository, unpacking
    its bundled XGBoost ensemble weights (models.zip), and pre-warming its
    ESM-IF1 weight cache during installation."""

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(DISCOTOPE_DIC['home'], cls.getEnvName(DISCOTOPE_DIC))
        cls._defineVar(DISCOTOPE_DIC['activation'], cls.getEnvActivationCommand(DISCOTOPE_DIC))

    @classmethod
    def defineBinaries(cls, env):
        cls.addDiscoTopePackage(env)

    @classmethod
    def addDiscoTopePackage(cls, env, default=True):
        # Python is pinned to 3.14, per the upstream project's own README
        # (github.com/Magnushhoie/DiscoTope-3.0#installation-guide), not
        # the stale 'Python :: 3.9' classifier in its setup.py.
        home = cls.getVar(DISCOTOPE_DIC['home'])
        weightsCacheDir = cls.getWeightsCacheDir()
        installedMarker = f"{DISCOTOPE_DIC['name']}_installed"

        installer = InstallHelper(DISCOTOPE_DIC['name'], packageHome=home,
                                  packageVersion=DISCOTOPE_DIC['version'])

        installer.getCondaEnvCommand(
            DISCOTOPE_DIC['name'], binaryVersion=DISCOTOPE_DIC['version'], pythonVersion='3.14'
        ).addCommand(
            f"git clone --depth 1 {UPSTREAM_URL} {home}",
            'DISCOTOPE_CLONED'
        ).addCommand(
            f"{cls.getEnvActivationCommand(DISCOTOPE_DIC)} && "
            f"cd {home} && pip install -r requirements.txt && pip install . && unzip -q models.zip",
            'DISCOTOPE_DEPS_INSTALLED'
        ).addCommand(
            f"mkdir -p {weightsCacheDir} && "
            f"{cls.getEnvActivationCommand(DISCOTOPE_DIC)} && "
            f"TORCH_HOME={weightsCacheDir} python -c "
            f"\"from discotope3.esm.pretrained import esm_if1_gvp4_t16_142M_UR50; "
            f"esm_if1_gvp4_t16_142M_UR50()\"",
            'DISCOTOPE_WEIGHTS_CACHED'
        ).addCommand(
            f'touch {installedMarker}', installedMarker
        ).addPackage(env, dependencies=['conda', 'git', 'unzip'], default=default)

    @classmethod
    def validateInstallation(cls):
        """Check that this plugin's requirements are met. Returns a list of
        actionable error messages, empty if the installation is correct."""
        errors = []

        mainScript = cls.getMainScriptPath()
        modelsDir = cls.getModelsDir()
        if not os.path.isfile(mainScript):
            errors.append(f"Could not find 'discotope3/main.py' under DISCOTOPE_HOME: '{cls.getDiscoTopeDir()}'.")
        elif not os.path.isdir(modelsDir):
            errors.append(f"Could not find the unzipped 'models/' folder under DISCOTOPE_HOME: '{modelsDir}'.")
        elif not cls.checkCallEnv(DISCOTOPE_DIC):
            errors.append("Activation of the DiscoTope-3.0 conda environment failed.")

        if errors:
            errors.append(NOINSTALL_WARNING)
        return errors

    @classmethod
    def checkCallEnv(cls, packageDic):
        actCommand = cls.getVar(packageDic['activation'])
        try:
            if 'conda' in actCommand and 'shell.bash hook' not in actCommand:
                actCommand = f'{cls.getCondaActivationCmd()}{actCommand}'
            subprocess.check_output(f'{actCommand} && python -c "import discotope3"', shell=True)
            return True
        except subprocess.CalledProcessError:
            return False

    # ---------------------------------- Utils -----------------------------------

    @classmethod
    def getDiscoTopeDir(cls):
        return cls.getVar(DISCOTOPE_DIC['home'])

    @classmethod
    def getMainScriptPath(cls):
        return os.path.join(cls.getDiscoTopeDir(), 'discotope3', 'main.py')

    @classmethod
    def getModelsDir(cls):
        return os.path.join(cls.getDiscoTopeDir(), 'models')

    @classmethod
    def getWeightsCacheDir(cls):
        return os.path.join(cls.getDiscoTopeDir(), '.torch_cache')

    # ---------------------------------- Protocol functions-----------------------

    @classmethod
    def runDiscoTope(cls, protocol, args, cwd=None):
        # runJob's 'env' kwarg expects a pyworkflow Environ object, not a
        # plain dict (AttributeError: 'dict' object has no attribute
        # 'getPrepend' otherwise, confirmed by actually running this) --
        # TORCH_HOME is set on os.environ directly instead, which a
        # subprocess launched with no explicit 'env' override inherits.
        os.environ['TORCH_HOME'] = cls.getWeightsCacheDir()
        activation = cls.getVar(DISCOTOPE_DIC['activation'])
        fullProgram = f'{activation} && python {cls.getMainScriptPath()}'
        protocol.runJob(fullProgram, args, cwd=cwd)
