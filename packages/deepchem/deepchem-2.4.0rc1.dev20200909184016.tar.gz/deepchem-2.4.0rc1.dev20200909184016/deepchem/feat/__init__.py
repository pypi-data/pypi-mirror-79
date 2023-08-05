"""
Making it easy to import in classes.
"""
# flake8: noqa

# base classes for featurizers
from deepchem.feat.base_classes import Featurizer
from deepchem.feat.base_classes import MolecularFeaturizer
from deepchem.feat.base_classes import MaterialStructureFeaturizer
from deepchem.feat.base_classes import MaterialCompositionFeaturizer
from deepchem.feat.base_classes import ComplexFeaturizer
from deepchem.feat.base_classes import UserDefinedFeaturizer

from deepchem.feat.graph_features import ConvMolFeaturizer
from deepchem.feat.graph_features import WeaveFeaturizer
from deepchem.feat.fingerprints import CircularFingerprint
from deepchem.feat.rdkit_descriptors import RDKitDescriptors
from deepchem.feat.coulomb_matrices import CoulombMatrix
from deepchem.feat.coulomb_matrices import CoulombMatrixEig
from deepchem.feat.coulomb_matrices import BPSymmetryFunctionInput
from deepchem.feat.rdkit_grid_featurizer import RdkitGridFeaturizer
from deepchem.feat.binding_pocket_features import BindingPocketFeaturizer
from deepchem.feat.one_hot import OneHotFeaturizer
from deepchem.feat.raw_featurizer import RawFeaturizer
from deepchem.feat.atomic_coordinates import AtomicCoordinates
from deepchem.feat.atomic_coordinates import NeighborListComplexAtomicCoordinates
from deepchem.feat.adjacency_fingerprints import AdjacencyFingerprint
from deepchem.feat.smiles_featurizers import SmilesToSeq, SmilesToImage

# molecule featurizers
from deepchem.feat.molecule_featurizers import MolGraphConvFeaturizer

# material featurizers
from deepchem.feat.material_featurizers import ElementPropertyFingerprint
from deepchem.feat.material_featurizers import SineCoulombMatrix
from deepchem.feat.material_featurizers import CGCNNFeaturizer

try:
  import transformers
  from transformers import BertTokenizer

  from deepchem.feat.smiles_tokenizer import SmilesTokenizer
  from deepchem.feat.smiles_tokenizer import BasicSmilesTokenizer
except ModuleNotFoundError:
  pass
