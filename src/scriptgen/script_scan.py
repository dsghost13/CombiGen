import random

import pandas as pd

from scriptgen.chemtools import SmirksGenerator


# <insert mechanism>
# Notes on mechanism:
# [1]
# [2]

# Get NUCLEOPHILE SOURCE and substituents in SMILES format
source_cores = ["CC(C)[NH2:10]", "CC(C)(C)[NH2:10]", "[NH2:10]C1CCCCC1", "CCC[NH2:10]", "CC[NH2:10]", "C[NH2:10]", "CCC[NH:10]CCC", "CC[NH:10]CCC", "C[NH:10]CCC", "CC[NH:10]CC", "C[NH:10]C", "C[NH:10]CC", "C1CC[NH:10]C1", "C1COCC[NH:10]1", "C1CC[NH:10]CC1", "C1CNCC[NH:10]1", "C1C[NH:10]C1", "C1CCC[NH:10]CC1"]

# Get ELECTROPHILE SINK and substituents in SMILES format
sink_cores = ["[*:201][C:20]([*:202])([*:203])[*:211]"]
sink_subs = [
	["c7ccccc7[*:201]", "C/C=C/[*:201]", "CC/C=C/[*:201]", "N#C[*:201]", "CC#C[*:201]", "CCC#C[*:201]", "O=C([*:201])c1ccccc1", "CC(=O)[*:201]", "CCC(=O)[*:201]", "C[*:201]", "CC[*:201]", "CCC[*:201]", "[H][*:201]"],
	["[H][*:202]"],
	["[H][*:203]"],
	["O=S(=O)([O:21][*:211])C(F)(F)F", "Cc1ccc(S(=O)(=O)[O:21][*:211])cc1", "CS(=O)(=O)[O:21][*:211]", "[Cl:21][*:211]"]
]

# Get ARROW PUSHING in RP format
arrow_pushing = "10=20;20,21=21"

# Get PARETO FRONT as T/F table
pareto_rows = ["c7ccccc7[*:201]", "C/C=C/[*:201]", "CC/C=C/[*:201]", "N#C[*:201]", "CC#C[*:201]", "CCC#C[*:201]", "O=C([*:201])c1ccccc1", "CC(=O)[*:201]", "CCC(=O)[*:201]", "C[*:201]", "CC[*:201]", "CCC[*:201]", "[H][*:201]"]
pareto_columns = ["O=S(=O)([O:21][*:211])C(F)(F)F", "Cc1ccc(S(=O)(=O)[O:21][*:211])cc1", "CS(=O)(=O)[O:21][*:211]", "[Cl:21][*:211]"]
pareto_data = [
	[True, True, True, True],
	[True, True, True, True],
	[True, True, True, True],
	[True, True, True, True],
	[True, True, True, True],
	[True, True, True, True],
	[True, True, True, True],
	[True, True, True, True],
	[True, True, True, True],
	[True, False, False, False],
	[True, False, False, False],
	[True, False, False, False],
	[True, False, False, False]
]
pareto_front = pd.DataFrame(pareto_data, index=pareto_rows, columns=pareto_columns)

pareto_fronts = [pareto_front]
