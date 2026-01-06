import re
from itertools import product, combinations

from rdkit import Chem


class SmirksGenerator:
    def __init__(self, source_cores, sink_cores, arrow_pushing,
                 source_subs=None, sink_subs=None, linkers=None, pareto_fronts=None):
        self.source_cores = source_cores
        self.source_subs = source_subs
        self.sink_cores = sink_cores
        self.sink_subs = sink_subs
        self.linkers = linkers
        self.arrow_pushing = arrow_pushing
        self.pareto_fronts = pareto_fronts

    def generate_smirks(self):
        smirks_list = []
        source_mols = self.connect_dummy_atoms(self.source_cores, self.source_subs)
        sink_mols = self.connect_dummy_atoms(self.sink_cores, self.sink_subs)

        if self.linkers:
            linked_mols = self.connect_linkers(source_mols, sink_mols)
            for linked_mol in linked_mols:
                reactant = Chem.MolToSmiles(linked_mol)
                product = self.generate_product(linked_mol)
                smirks = reactant + ">>" + product + " " + self.arrow_pushing
                smirks_list.append(smirks)
        else:
            for source_mol in source_mols:
                for sink_mol in sink_mols:
                    reactants_mol = Chem.CombineMols(source_mol, sink_mol)
                    reactants = Chem.MolToSmiles(source_mol) + "." + Chem.MolToSmiles(sink_mol)
                    product = self.generate_product(reactants_mol)
                    smirks = reactants + ">>" + product + " " + self.arrow_pushing
                    smirks_list.append(smirks)
        return smirks_list

    def connect_dummy_atoms(self, cores, subs):
        if not subs:
            mols = [Chem.MolFromSmiles(core, sanitize=False) for core in cores]
            return mols

        mols = []
        mapnums = self.get_mapnums(subs)

        for core in cores:
            core_mol = Chem.MolFromSmiles(core, sanitize=False)

            for sub_combo in product(*subs):
                if not self.subs_compatible(sub_combo):
                    continue
                base_mol = Chem.Mol(core_mol)

                for i, mapnum in enumerate(mapnums):
                    sub_mol = Chem.MolFromSmiles(sub_combo[i], sanitize=False)
                    core_atom = self.get_atom_with_mapnum(base_mol, mapnum)
                    sub_atom = self.get_atom_with_mapnum(sub_mol, mapnum)
                    base_mol = self.connect_mols(base_mol, sub_mol, core_atom, sub_atom)
                mols.append(base_mol)
        return mols

    def connect_linkers(self, source_mols, sink_mols):
        linked_mols = []
        mapnums = self.get_mapnums(self.linkers)
        linker_mols = [Chem.MolFromSmiles(linker) for linker in self.linkers]

        for source_mol, sink_mol, linker_mol in product(source_mols, sink_mols, linker_mols):
            source_atom = self.get_atom_with_mapnum(source_mol, mapnums[0])
            linker_atom = self.get_atom_with_mapnum(linker_mol, mapnums[0])
            linked_mol = self.connect_mols(source_mol, linker_mol, source_atom, linker_atom)

            source_linker_atom = self.get_atom_with_mapnum(linked_mol, mapnums[1])
            sink_atom = self.get_atom_with_mapnum(sink_mol, mapnums[1])
            linked_mol = self.connect_mols(linked_mol, sink_mol, source_linker_atom, sink_atom)

            linked_mols.append(linked_mol)
        return linked_mols

    def generate_product(self, reactants):
        self.partial_sanitize(reactants)
        mapping_section_list = self.arrow_pushing.split(';')
        source_list = []
        sink_list = []

        for arrowPush in mapping_section_list:
            split_arrow_push = arrowPush.split('=')
            source_side = split_arrow_push[0].split(',')
            sink_side = split_arrow_push[1].split(',')

            for j in range(0, len(source_side)):
                source_side[j] = int(source_side[j])

            for j in range(0, len(sink_side)):
                sink_side[j] = int(sink_side[j])

            source_list.append(source_side)
            sink_list.append(sink_side)
        reactants_editable = Chem.EditableMol(reactants)

        for j in range(len(source_list)):
            if len(source_list[j]) + len(sink_list[j]) == 2:
                sink_list[j].append(source_list[j][0])

            if len(source_list[j]) == 2:
                index1 = self.get_index_of_mapnum(reactants_editable.GetMol(), source_list[j][0])
                index2 = self.get_index_of_mapnum(reactants_editable.GetMol(), source_list[j][1])
                source_bond = reactants_editable.GetMol().GetBondBetweenAtoms(index1, index2)

                if source_bond is None:
                    print("ERROR, REMOVING A ZERO ORDERED BOND!!!")
                else:
                    if source_bond.GetBondTypeAsDouble() == 1.0:
                        reactants_editable.RemoveBond(index1, index2)
                    elif source_bond.GetBondTypeAsDouble() == 2.0:
                        reactants_editable.RemoveBond(index1, index2)
                        reactants_editable.AddBond(index1, index2, order=Chem.rdchem.BondType.SINGLE)
                    elif source_bond.GetBondTypeAsDouble() == 3.0:
                        reactants_editable.RemoveBond(index1, index2)
                        reactants_editable.AddBond(index1, index2, order=Chem.rdchem.BondType.DOUBLE)
                    elif source_bond.GetBondTypeAsDouble() == 4.0:
                        reactants_editable.RemoveBond(index1, index2)
                        reactants_editable.AddBond(index1, index2, order=Chem.rdchem.BondType.TRIPLE)
                    else:
                        print(" Error - Unaccounted source bond-order!\n")
                        raise RuntimeError("Unaccounted atom mapping source bond order") from None

                index1 = self.get_index_of_mapnum(reactants_editable.GetMol(), source_list[j][0])
                index2 = self.get_index_of_mapnum(reactants_editable.GetMol(), source_list[j][1])

                charge1 = reactants_editable.GetMol().GetAtomWithIdx(index1).GetFormalCharge()
                charge2 = reactants_editable.GetMol().GetAtomWithIdx(index2).GetFormalCharge()

                charge1 += 1
                charge2 += 1

                atom1 = reactants_editable.GetMol().GetAtomWithIdx(index1)
                atom2 = reactants_editable.GetMol().GetAtomWithIdx(index2)

                atom1.SetFormalCharge(charge1)
                atom2.SetFormalCharge(charge2)

                reactants_editable.ReplaceAtom(index1, atom1)
                reactants_editable.ReplaceAtom(index2, atom2)
            elif len(source_list[j]) == 1:
                index1 = self.get_index_of_mapnum(reactants_editable.GetMol(), source_list[j][0])
                charge1 = reactants_editable.GetMol().GetAtomWithIdx(index1).GetFormalCharge()
                charge1 += 2
                atom1 = reactants_editable.GetMol().GetAtomWithIdx(index1)
                atom1.SetFormalCharge(charge1)
                reactants_editable.ReplaceAtom(index1, atom1)
            else:
                print("Error - source atom mapping code has atoms that are not 1 or 2")
                raise RuntimeError("Unaccepted atom mapping source") from None

            if len(sink_list[j]) == 2:
                index1 = self.get_index_of_mapnum(reactants_editable.GetMol(), sink_list[j][0])
                index2 = self.get_index_of_mapnum(reactants_editable.GetMol(), sink_list[j][1])
                sink_bond = reactants_editable.GetMol().GetBondBetweenAtoms(index1, index2)

                if sink_bond is None:
                    reactants_editable.AddBond(index1, index2, order=Chem.rdchem.BondType.SINGLE)
                else:
                    if sink_bond.GetBondTypeAsDouble() == 1.0:
                        reactants_editable.RemoveBond(index1, index2)
                        reactants_editable.AddBond(index1, index2, order=Chem.rdchem.BondType.DOUBLE)
                    elif sink_bond.GetBondTypeAsDouble() == 2.0:
                        reactants_editable.RemoveBond(index1, index2)
                        reactants_editable.AddBond(index1, index2, order=Chem.rdchem.BondType.TRIPLE)
                    elif sink_bond.GetBondTypeAsDouble() == 3.0:
                        reactants_editable.RemoveBond(index1, index2)
                        reactants_editable.AddBond(index1, index2, order=Chem.rdchem.BondType.QUADRUPLE)
                    elif sink_bond.GetBondTypeAsDouble() == 4.0:
                        print("ERROR, TRYING TO ADD A BOND ORDER TO A BOND ORDER OF 4!!!")
                        raise RuntimeError("Error - trying to add to a bond order of 4 for the sink atom") from None
                    else:
                        print("Error - unaccounted for bond order in atom mapping code sink")
                        raise RuntimeError("Error - unaccounted for bond order in atom mapping code sink") from None

                index1 = self.get_index_of_mapnum(reactants_editable.GetMol(), sink_list[j][0])
                index2 = self.get_index_of_mapnum(reactants_editable.GetMol(), sink_list[j][1])

                charge1 = reactants_editable.GetMol().GetAtomWithIdx(index1).GetFormalCharge()
                charge2 = reactants_editable.GetMol().GetAtomWithIdx(index2).GetFormalCharge()

                charge1 -= 1
                charge2 -= 1

                atom1 = reactants_editable.GetMol().GetAtomWithIdx(index1)
                atom2 = reactants_editable.GetMol().GetAtomWithIdx(index2)

                atom1.SetFormalCharge(charge1)
                atom2.SetFormalCharge(charge2)

                reactants_editable.ReplaceAtom(index1, atom1)
                reactants_editable.ReplaceAtom(index2, atom2)
            elif len(sink_list[j]) == 1:
                index1 = self.get_index_of_mapnum(reactants_editable.GetMol(), sink_list[j][0])
                charge1 = reactants_editable.GetMol().GetAtomWithIdx(index1).GetFormalCharge()
                charge1 -= 2
                atom1 = reactants_editable.GetMol().GetAtomWithIdx(index1)
                atom1.SetFormalCharge(charge1)
                reactants_editable.ReplaceAtom(index1, atom1)
            else:
                print("Error - sink atom mapping code has atoms that are not 1 or 2")
                raise RuntimeError("Unaccepted atom mapping sink") from None
        reactants = reactants_editable.GetMol()
        self.partial_sanitize(reactants)
        return Chem.MolToSmiles(reactants)

    def subs_compatible(self, sub_combo):
        if not self.pareto_fronts:
            return True

        for sub1, sub2 in combinations(sub_combo, 2):
            for pf in self.pareto_fronts:
                if sub1 not in pf.index and sub1 not in pf.columns:
                    continue
                if sub2 not in pf.index and sub2 not in pf.columns:
                    continue

                compatible = True
                if sub1 in pf.index and sub2 in pf.columns:
                    compatible = pf.at[sub1, sub2]
                elif sub2 in pf.index and sub1 in pf.columns:
                    compatible = pf.at[sub2, sub1]
                if not compatible:
                    return False
        return True

    def connect_mols(self, mol1, mol2, atom1, atom2):
        combined_mol = Chem.CombineMols(mol1, mol2)
        editable_mol = Chem.EditableMol(combined_mol)

        atom1_idx = atom1.GetIdx()
        atom2_idx = atom2.GetIdx()

        neighbor1_idx = atom1.GetNeighbors()[0].GetIdx()
        neighbor2_idx = atom2.GetNeighbors()[0].GetIdx()

        bond_order = atom2.GetBonds()[0].GetBondType()
        editable_mol.AddBond(neighbor1_idx, neighbor2_idx + mol1.GetNumAtoms(), order=bond_order)
        editable_mol.RemoveAtom(atom2_idx + mol1.GetNumAtoms())
        editable_mol.RemoveAtom(atom1_idx)

        mol = editable_mol.GetMol()
        return mol

    def get_mapnums(self, smiles):
        try:
            if isinstance(smiles[0], str):
                nums = re.findall(r'\d+', smiles[0])
                mapnums = sorted([int(n) for n in nums if int(n) >= 100])
            else:
                mapnums = []
                for sub in smiles:
                    nums = re.findall(r'\d+', sub[0])
                    nums = sorted([int(n) for n in nums if int(n) >= 100])
                    mapnums.extend(nums)
            return mapnums
        except Exception as e:
            print(e)
            print(smiles)

    def get_atom_with_mapnum(self, mol, mapnum):
        for atom in mol.GetAtoms():
            if atom.GetAtomMapNum() == mapnum:
                return atom
        return None

    def get_index_of_mapnum(self, mol, mapnum):
        for atom in mol.GetAtoms():
            if atom.GetAtomMapNum() == mapnum:
                return atom.GetIdx()
        return None

    def partial_sanitize(self, mol):
        Chem.SanitizeMol(mol, sanitizeOps=Chem.SANITIZE_ALL ^
                                          Chem.SANITIZE_KEKULIZE ^
                                          Chem.SANITIZE_SETAROMATICITY ^
                                          Chem.SANITIZE_CLEANUP ^
                                          Chem.SANITIZE_CLEANUPCHIRALITY ^
                                          Chem.SANITIZE_SYMMRINGS)
        mol.UpdatePropertyCache()