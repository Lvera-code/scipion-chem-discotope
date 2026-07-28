=========
CHANGES
=========

0.2.0
=====
- Automatic installation: the plugin now clones the upstream repository,
  unpacks the bundled XGBoost ensemble weights and pre-warms the ESM-IF1
  weight cache through ``scipion3 installb DiscoTope``, using
  ``InstallHelper``. No manual setup or ``scipion.conf`` variables are
  required any longer.

0.1.0
=====
- Initial release: DiscoTope-3.0 structure-based (conformational) epitope
  prediction protocol (``ProtDiscoTopePrediction``), single-chain PDB per
  run. Uses the authors' own calibrated_score column and published
  reference thresholds instead of a hand-calibrated raw score.
