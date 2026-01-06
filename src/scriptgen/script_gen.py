from config.constants import SCRIPT_PATH
from scriptgen.data_fields import TextEntryHandler


class ScriptGenerator:
    @staticmethod
    def generate_script():
        try:
            with open(SCRIPT_PATH, "w") as f:
                ScriptGenerator.write_imports(f)
                ScriptGenerator.write_notes(f)
                ScriptGenerator.write_reactant(f, "source")
                ScriptGenerator.write_reactant(f, "sink")
                ScriptGenerator.write_linkers(f)
                ScriptGenerator.write_arrow_pushing(f)
                ScriptGenerator.write_pareto_fronts(f)
                ScriptGenerator.write_smirks(f)
        except Exception as e:
            print(e)

    @staticmethod
    def write_imports(f):
        f.write("import random\n\n")
        if TextEntryHandler.DATA["pareto_fronts"]:
            f.write("import pandas as pd\n\n")
        f.write("from scriptgen.chemtools import SmirksGenerator\n\n\n")

    @staticmethod
    def write_notes(f):
        f.write("# <insert mechanism>\n")
        f.write("# Notes on mechanism:\n")
        f.write("# [1]\n")
        f.write("# [2]\n\n")

    @staticmethod
    def write_reactant(f, reactant_type):
        if reactant_type == "source":
            f.write(f"# Get NUCLEOPHILE SOURCE and substituents in SMILES format\n")
        elif reactant_type == "sink":
            f.write(f"# Get ELECTROPHILE SINK and substituents in SMILES format\n")
        else:
            raise Exception(f"ScriptGenError: invalid reactant type.")

        cores_field = f"{reactant_type}_cores"
        if not TextEntryHandler.DATA[cores_field]:
            raise Exception(f"ScriptGenError: {reactant_type} cores has no value.")
        cores_smiles = ", ".join(f"\"{core}\"" for core in TextEntryHandler.DATA[cores_field])
        f.write(f"{cores_field} = [{cores_smiles}]\n")

        subs_field = f"{reactant_type}_subs"
        if TextEntryHandler.DATA[subs_field]:
            subs_smiles = []
            for subs in TextEntryHandler.DATA[subs_field]:
                sub_smile = "\t[" + ", ".join(f"\"{sub}\"" for sub in subs) + "]"
                subs_smiles.append(sub_smile)
            sub_smiles = ",\n".join(subs_smiles)
            f.write(f"{subs_field} = [\n{sub_smiles}\n]\n")
        f.write("\n")

    @staticmethod
    def write_linkers(f):
        if TextEntryHandler.DATA["linkers"]:
            f.write("# Get LINKER in SMILES format\n")
            linkers_smiles = ", ".join(f"\"{linker}\"" for linker in TextEntryHandler.DATA["linkers"])
            f.write(f"linkers = [{linkers_smiles}]\n\n")

    @staticmethod
    def write_arrow_pushing(f):
        if not TextEntryHandler.DATA["arrow_pushing"]:
            raise Exception("ScriptGenError: arrow pushing has no value. ")
        f.write("# Get ARROW PUSHING in RP format\n")
        f.write(f"arrow_pushing = \"{TextEntryHandler.DATA["arrow_pushing"]}\"\n\n")

    @staticmethod
    def write_pareto_fronts(f):
        if not TextEntryHandler.DATA["pareto_fronts"]:
            return

        f.write("# Get PARETO FRONT as T/F table\n")
        pareto_fronts = []
        for num, pf in enumerate(TextEntryHandler.DATA["pareto_fronts"]):
            num_tag = f"_{num+1}" if len(TextEntryHandler.DATA["pareto_fronts"]) > 1 else ""

            row_smiles = ", ".join(f"\"{smiles}\"" for smiles in pf.row_subs)
            f.write(f"pareto_rows{num_tag} = [{row_smiles}]\n")

            col_smiles = ", ".join(f"\"{smiles}\"" for smiles in pf.col_subs)
            f.write(f"pareto_columns{num_tag} = [{col_smiles}]\n")

            pareto_bools = []
            for i in range(len(pf.row_subs)):
                row_bools = []
                for j in range(len(pf.col_subs)):
                    row_bools.append(pf.table_layout.itemAtPosition(i+1, j+1).widget().isChecked())
                pareto_bools.append(row_bools)

            pareto_data = []
            for row_bools in pareto_bools:
                row_data = ", ".join(str(b) for b in row_bools)
                pareto_data.append(f"\t[{row_data}]")
            pareto_fronts.append(f"pareto_front{num_tag}")

            f.write(f"pareto_data{num_tag} = [\n")
            f.write(",\n".join(pareto_data))
            f.write("\n]\n")
            f.write(f"pareto_front{num_tag} = pd.DataFrame(pareto_data{num_tag}, "
                    f"index=pareto_rows{num_tag}, columns=pareto_columns{num_tag})\n\n")
        f.write(f"pareto_fronts = [{', '.join(pareto_fronts)}]\n\n")

    @staticmethod
    def write_smirks(f):
        f.write("# Generate and print SMIRKS\n")
        f.write(f"smirks_gen = SmirksGenerator(source_cores, sink_cores, arrow_pushing,\n\t\t\t ")

        for field in ["source_subs", "sink_subs", "linkers"]:
            if TextEntryHandler.DATA[field]:
                f.write(f"{field}={field}, ")
            else:
                f.write(f"{field}=None, ")

        if TextEntryHandler.DATA["pareto_fronts"]:
            f.write("pareto_fronts=pareto_fronts)\n")
        else:
            f.write("pareto_fronts=None)\n")

        f.write("smirks_list = smirks_gen.generate_smirks()\n")
        f.write("for smirks in smirks_list:\n")
        f.write(f"\tif random.random() < {TextEntryHandler.DATA["output_proportion"]}:\n")
        f.write("\t\tprint(smirks)\n")
        f.write("print(str(len(smirks_list)) + \" Total SMIRKS\")")