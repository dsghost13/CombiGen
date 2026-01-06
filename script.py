import random

from scriptgen.chemtools import SmirksGenerator


# <insert mechanism>
# Notes on mechanism:
# [1]
# [2]

# Get NUCLEOPHILE SOURCE and substituents in SMILES format
source_cores = ["[*:101][C-:10]([*:102])[*:103]"]
source_subs = [
	["[H][*:102]", "C[*:102]", "CC[*:102]", "C(C)(C)[*:102]", "C(C)(C)(C)[*:102]", "c7ccccc7[*:102]"],
	["C[N+](C)(C)[*:103]", "[*:103][P+](c1ccccc1)(c2ccccc2)c3ccccc3", "C[S+](C)(=O)[*:103]", "[*:103][S+](C)(C)"]
]

# Get ELECTROPHILE SINK and substituents in SMILES format
sink_cores = ["[*:201][B:20]([*:202])[*:203]"]
sink_subs = [
	["[H][*:202]", "I[*:202]", "Br[*:202]", "Cl[*:202]", "F[*:202]", "CC[*:202]", "c9ccccc9[*:202]"],
	["[H][*:203]", "I[*:203]", "Br[*:203]", "Cl[*:203]", "F[*:203]", "CC[*:203]", "c9ccccc9[*:203]"]
]

# Get LINKER in SMILES format
linkers = ["[*:101]CCC[*:201]", "[*:101]CC(C)(C)C[*:201]", "[*:101]CC(C)(C)CC[*:201]", "[*:101]CCC(C)(C)C[*:201]", "[*:101]CCCC[*:201]"]

# Get ARROW PUSHING in RP format
arrow_pushing = "10=20"

# Generate and print SMIRKS
smirks_gen = SmirksGenerator(source_cores, sink_cores, arrow_pushing,
			 source_subs=source_subs, sink_subs=sink_subs, linkers=linkers, pareto_fronts=None)
smirks_list = smirks_gen.generate_smirks()
for smirks in smirks_list:
	if random.random() < 0.01:
		print(smirks)
print(str(len(smirks_list)) + " Total SMIRKS")