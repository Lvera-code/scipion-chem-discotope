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

# DiscoTope-3.0 (DTU Health Tech, CC BY-NC 4.0 free academic use) is
# installed automatically: it is installable directly via git+pip (no
# academic-request form, unlike BepiPred/NetMHCpan/NetMHCIIpan/SignalP).
# The setup sequence -- clone, pip install, unzip the bundled XGBoost
# ensemble weights (models.zip, committed in the upstream repo), and
# pre-warm the ESM-IF1 weight cache -- is fully scripted in defineBinaries,
# confirmed against the real upstream source
# (github.com/Magnushhoie/DiscoTope-3.0): models.zip ships in the repo
# root, and ESM-IF1 weights are fetched by
# discotope3.esm.pretrained.esm_if1_gvp4_t16_142M_UR50() via
# torch.hub.load_state_dict_from_url (a public, unauthenticated download
# from dl.fbaipublicfiles.com, respecting TORCH_HOME) -- calling that
# function once during install, with TORCH_HOME pointed at our own cache
# dir, downloads and caches it exactly like a real first protocol run
# would, without having to hardcode/guess the checkpoint URL(s) by hand.
DISCOTOPE_DIC = {
    'name': 'DiscoTope',
    'version': DEFAULT_VERSION,
    'home': 'DISCOTOPE_HOME',
    'activation': 'DISCOTOPE_ACTIVATION_CMD',
}

READ_URL = 'https://github.com/Lvera-code/scipion-chem-discotope'
UPSTREAM_URL = 'https://github.com/Magnushhoie/DiscoTope-3.0'

NOINSTALL_WARNING = (
    'Installation could not be completed because the local DiscoTope-3.0 '
    "installation has not been found or its conda environment could not be "
    "activated. Run 'scipion3 installb DiscoTope' to install it "
    f'automatically. Please check the scipion-chem-discotope README file '
    f'for more details: {READ_URL}'
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
