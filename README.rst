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
form, unlike BepiPred/NetMHCpan/NetMHCIIpan/SignalP), so it is installed
automatically: ``scipion3 installb DiscoTope`` clones the upstream repo,
installs it into a dedicated conda env (Python 3.14, per upstream's own
README), unzips its bundled XGBoost ensemble weights (``models.zip``,
committed in the upstream repo), and pre-warms the ESM-IF1 weight cache
by calling ``discotope3.esm.pretrained.esm_if1_gvp4_t16_142M_UR50()``
once with ``TORCH_HOME`` pointed at a dedicated cache dir -- the same
public, unauthenticated download (``dl.fbaipublicfiles.com``) a first
protocol run would trigger anyway, just done at install time instead. No
manual setup or ``scipion.conf`` variables needed.

Output ROIs expose ``_meanScore``/``_maxScore`` (project-wide convention
formalized 2026-07-24, see ``scipion-chem-epitope-construct``): any
B-cell prediction protocol must expose these so the construct-assembly
protocol can rank candidates consistently across tools.

===================
Install this plugin
===================

**Developer's version**

.. code-block::

            git clone https://github.com/Lvera-code/scipion-chem-discotope.git
            cd scipion-chem-discotope
            scipion3 installp -p . --devel
            scipion3 installb DiscoTope
