# -*- coding: utf-8 -*-
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

DEFAULT_VERSION = '3.0'

# DiscoTope-3.0 (DTU Health Tech, Creative Commons free academic use) is
# installable directly via git+pip (no academic-request form, unlike
# BepiPred/NetMHCpan/NetMHCIIpan/SignalP) -- still not auto-installed here,
# since it also needs the bundled XGBoost ensemble weights (models.zip)
# unpacked manually and a one-time ESM-IF1 weight download cached outside
# the repo, a setup sequence Scipion's conda installer cannot express
# cleanly as a single defineBinaries step.
DISCOTOPE_DIC = {
    'name': 'DiscoTope',
    'version': DEFAULT_VERSION,
    'python_bin': 'DISCOTOPE_PYTHON_BIN',
    'install_path': 'DISCOTOPE_INSTALL_PATH',
    'models_dir': 'DISCOTOPE_MODELS_DIR',
    'weights_cache_dir': 'DISCOTOPE_WEIGHTS_CACHE_DIR',
}

READ_URL = 'https://github.com/Lvera-code/scipion-chem-discotope'
UPSTREAM_URL = 'https://github.com/Magnushhoie/DiscoTope-3.0'

NOINSTALL_WARNING = (
    'Installation could not be completed because the local DiscoTope-3.0 '
    f'installation has not been found. Clone {UPSTREAM_URL} manually, build a '
    'dedicated venv, unzip its bundled models.zip, and set '
    'DISCOTOPE_PYTHON_BIN/DISCOTOPE_INSTALL_PATH/DISCOTOPE_MODELS_DIR in '
    f'scipion.conf. Please check the scipion-chem-discotope README file for '
    f'more details: {READ_URL}'
)

# ADR: 'calibrated_score', not the raw 'DiscoTope-3.0_score' -- the raw
# column (0.00-1.00) would need a threshold hand-calibrated against a
# reference structure, with no backing from the authors. 'calibrated_score'
# is a SEPARATE column DiscoTope-3.0 itself already computes (normalized by
# chain length and accessible surface), for which the authors DO publish
# reference thresholds with expected recall (Frontiers in Immunology 2024,
# Hoie et al.): ~0.40 (70th percentile, ~70% recall, "low"), ~0.90
# ("moderate", the CLI flag's own default), ~1.51 (30th percentile, higher
# precision/lower recall, "higher"). Using this column replaces a
# home-grown calibration with the authors' own.
RAW_RESIDUE_COLUMN = 'residue'
RAW_SCORE_COLUMN = 'calibrated_score'

DEFAULT_THRESHOLD = 0.90
