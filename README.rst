================================
DiscoTope-3.0 Scipion plugin
================================

Scipion framework plugin wrapping DiscoTope-3.0 (Hoie et al. 2024, DTU
Health Tech, Creative Commons free academic use) for structure-based
(conformational) B-cell epitope prediction.

The plugin implements a single protocol, ``ProtDiscoTopePrediction``, which
takes a SINGLE-CHAIN PDB structure (``AtomStruct``) and maps DiscoTope-3.0's
per-residue ``calibrated_score`` into contiguous linear epitope regions
(one ``SetOfSequenceROIs``) via a gap-tolerant sliding window. Uses
``calibrated_score`` (not the raw ``DiscoTope-3.0_score``): the authors
publish reference thresholds with expected recall for this normalized
column (~0.40 "low", ~0.90 "moderate"/default, ~1.51 "higher").

DiscoTope-3.0 is installable directly via git+pip (no academic-request
form, unlike BepiPred/NetMHCpan/NetMHCIIpan/SignalP) but is **not**
installed automatically: the bundled XGBoost weights need manual
unpacking and ESM-IF1 needs a one-time cached weight download, a setup
sequence Scipion's conda installer cannot express as a single step.

================================
Manual setup
================================

.. code-block::

      git clone https://github.com/Magnushhoie/DiscoTope-3.0
      python3 -m venv .venv-discotope
      .venv-discotope/bin/pip install -r DiscoTope-3.0/requirements.txt
      .venv-discotope/bin/pip install DiscoTope-3.0
      cd DiscoTope-3.0 && unzip models.zip

Then, in ``scipion.conf``, set:

.. code-block::

      DISCOTOPE_PYTHON_BIN = <path to .venv-discotope's python>
      DISCOTOPE_INSTALL_PATH = <path to the DiscoTope-3.0 clone>
      DISCOTOPE_MODELS_DIR = <path to DiscoTope-3.0/models>
      DISCOTOPE_WEIGHTS_CACHE_DIR = <path to cache ESM-IF1 weights, outside the repo>

===================
Install this plugin
===================

**Developer's version**

.. code-block::

            git clone https://github.com/Lvera-code/scipion-chem-discotope.git
            cd scipion-chem-discotope
            scipion3 installp -p . --devel
