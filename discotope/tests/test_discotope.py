from pwem.protocols import ProtImportPdb
from pyworkflow.tests import BaseTest, setupTestProject

from ..protocols import ProtDiscoTopePrediction

# Chain A of 7c4s.pdb, isolated as its own single-chain PDB (DiscoTope-3.0
# only supports single-chain input per run -- a real single-chain PDB
# extracted from the same reference structure used by the netmhcpan/
# scannet test fixtures, not a synthetic one).
_TEST_PDB = '/home/enzo/DiffSBDD/scipion-chem-discotope/tests_data/7c4s_chainA.pdb'


class TestDiscoTopePrediction(BaseTest):
    # Real reference value: from a real local run of the DiscoTope-3.0
    # binary against this exact single-chain PDB (struc_type=solved,
    # threshold=0.90 default), followed by this plugin's own sliding-window
    # mapping (9aa window, max 2 below-threshold residues, min length 9) --
    # not estimated.
    EXPECTED = (241, 249, 'RVQACPILF')
    EXPECTED_MEAN_SCORE = 1.481464
    EXPECTED_MAX_SCORE = 3.68022

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        setupTestProject(cls)

        cls.protImportPdb = cls.newProtocol(ProtImportPdb, inputPdbData=1, pdbFile=_TEST_PDB)
        cls.proj.launchProtocol(cls.protImportPdb, wait=True)

    def test(self):
        protDiscoTope = self.newProtocol(ProtDiscoTopePrediction)
        protDiscoTope.inputStructure.set(self.protImportPdb)
        protDiscoTope.inputStructure.setExtended('outputPdb')
        self.launchProtocol(protDiscoTope, wait=True)

        outROIs = getattr(protDiscoTope, 'outputROIs', None)
        self.assertIsNotNone(outROIs)
        self.assertEqual(len(outROIs), 1)

        roi = list(outROIs)[0]
        self.assertEqual((roi.getROIIdx(), roi.getROIIdx2(), roi.getROISequence()), self.EXPECTED)
        self.assertAlmostEqual(roi._meanScore.get(), self.EXPECTED_MEAN_SCORE, places=4)
        self.assertAlmostEqual(roi._maxScore.get(), self.EXPECTED_MAX_SCORE, places=4)
