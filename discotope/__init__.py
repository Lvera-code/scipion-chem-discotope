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

from pwchem import Plugin as pwchemPlugin

from .constants import DISCOTOPE_DIC, NOINSTALL_WARNING

_references = ['Hoie2024']


class Plugin(pwchemPlugin):
    """DiscoTope-3.0 is never installed automatically: not a license
    restriction (Creative Commons, free academic use, installable directly
    via git+pip), but the bundled XGBoost weights (models.zip) need manual
    unpacking and ESM-IF1 needs a one-time cached weight download -- a
    setup sequence Scipion's conda installer cannot express as a single
    step. See ``validateInstallation`` for what is checked and
    ``README.rst`` for the manual setup steps."""

    @classmethod
    def _defineVariables(cls):
        cls._defineVar(DISCOTOPE_DIC['python_bin'], '')
        cls._defineVar(DISCOTOPE_DIC['install_path'], '')
        cls._defineVar(DISCOTOPE_DIC['models_dir'], '')
        cls._defineVar(DISCOTOPE_DIC['weights_cache_dir'], '')

    @classmethod
    def defineBinaries(cls, env):
        """No-op: see class docstring."""
        pass

    @classmethod
    def validateInstallation(cls):
        """Check that this plugin's requirements are met. Returns a list of
        actionable error messages, empty if the installation is correct."""
        errors = []

        pythonBin = cls.getVar(DISCOTOPE_DIC['python_bin'])
        if not pythonBin or not os.path.isfile(pythonBin):
            errors.append(f"DISCOTOPE_PYTHON_BIN is not set or does not exist: '{pythonBin}'.")

        mainScript = cls.getMainScriptPath()
        if not mainScript or not os.path.isfile(mainScript):
            errors.append(f"Could not find 'discotope3/main.py' under DISCOTOPE_INSTALL_PATH: '{mainScript}'.")

        modelsDir = cls.getVar(DISCOTOPE_DIC['models_dir'])
        if not modelsDir or not os.path.isdir(modelsDir):
            errors.append(f"DISCOTOPE_MODELS_DIR is not set or does not exist: '{modelsDir}'.")

        if errors:
            errors.append(NOINSTALL_WARNING)
        return errors

    # ---------------------------------- Utils -----------------------------------

    @classmethod
    def getMainScriptPath(cls):
        installPath = cls.getVar(DISCOTOPE_DIC['install_path'])
        if not installPath:
            return None
        return os.path.join(installPath, 'discotope3', 'main.py')
