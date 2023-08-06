
import numpy as np
from simtk.openmm import unit


aa_residues = ["ALA", "CYS", "ASP", "GLU", "PHE", "GLY", "HIS", "ILE", "LYS", "LEU", "MET", "ASN", "PRO", "GLN", "ARG", "SER", "THR", "VAL", "TRP", "TYR"]

water_residues = ['HOH', 'TIP3', 'TIP3P', 'SPCE', 'SPC', 'TIP4PEW', 'WAT', 'OH2', 'TIP']

lipid_residues = ['AR', 'CHL', 'DHA', 'LA', 'MY', 'OL', 'PA', 'PC', 'PE', 'PGR', 'PH-', 'PS', 'SA', 'SM', 'ST']


def select_atoms(parmed_structure, keyword_selection=None, ligand_resname=None, resid_selection=None):

    lig_residues = ['LIG', 'UNL']

    if ligand_resname:
        lig_residues.append(ligand_resname)

    if keyword_selection == None and resid_selection == None:
        raise ValueError('Must specify either keyword selection or resid_selection')

    final_list = []

    if resid_selection:
        # split up the selection syntax
        resid_list = resid_selection.split()
        chain_selection = resid_list[0]
        resid_list = resid_list[1:]
        # convert the resids to integers
        resid_list = [int(i) for i in resid_list]
        # TODO check the order of chains in multichain proteins
        # TODO Currently assuming alphabet designation matches parmed order
        protein_chains = [i for i in parmed_structure.topology.chains() if next(i.residues()).name in aa_residues]
        for k, chain in enumerate(protein_chains):
            # convert letter rep of chain to ordinal number rep
            if ord(chain_selection.lower()) - 96 == k + 1:
                residues = [i for i in chain.residues()]
                selected_residues = [i for i in residues if i.index in resid_list]

                if len(selected_residues) == 0:
                    raise ValueError('Could not find one of the residues {} on protein chain.'.format(resid_list))

                for i in selected_residues:
                    for k in i.atoms():
                        final_list.append(k.index)
    if keyword_selection:
        selection_keywords = keyword_selection.split()

        # if selection keywords contain noh or not make sure they're at the end of the list
        if 'noh' in selection_keywords:
            selection_keywords.remove('noh')
            selection_keywords.append('noh')
        if 'not' in selection_keywords:
            selection_keywords.remove('not')
            selection_keywords.append('not')

        for keyword in selection_keywords:

            if keyword not in ['ligand', 'protein', 'lipids', 'water', 'noh', 'not']:
                raise ValueError(
                    'Keyword selection could syntax could not be parsed. Options are noh; not; protein; ligand; lipids; water.')

            if keyword == 'protein':
                protein_list = [i.idx for i in parmed_structure.atoms if i.residue.name in aa_residues]
                for i in protein_list:
                    final_list.append(i)

            if keyword == 'water':
                water_list = [i.idx for i in parmed_structure.atoms if i.residue.name in water_residues]
                for i in water_list:
                    final_list.append(i)

            if keyword == 'ligand':
                ligand_list = [i.idx for i in parmed_structure.atoms if i.residue.name in lig_residues]
                for i in ligand_list:
                    final_list.append(i)


            if keyword == 'lipid':
                lipid_list=[i.idx for i in parmed_structure.atoms if i.residue.name in lipid_residues]
                for i in lipid_list:
                    final_list.append(i)

            if keyword == 'noh':
                remove_list = []
                for i in final_list:
                    if 'H' in parmed_structure[i].name:
                        remove_list.append(i)
                final_list = list(set(final_list) - set(remove_list))

            if keyword == 'not':
                all_atoms = [i for i in parmed_structure.topology.atoms()]
                all_atoms_indeces_set = set([i.index for i in all_atoms])
                inverted_set = all_atoms_indeces_set - set(final_list)
                final_list = list(inverted_set)

    if len(final_list) == 0:
        print('warning, failed to select any atoms')
    return final_list

def find_center_of_mass(coord, masses):
    masses = np.array(masses)
    weights = masses/masses.sum()
    com = np.average(np.array(coord/unit.nanometer), weights = weights, axis=0)
    return com

def find_z_cone_apex(prot_positions, lig_positions, z_padding = 1):

    #this helper function is meant to find the apex of the funnel for use in funnel metaD
    #COORDINATES ARE IN NANOMETERS

    #first find z-coordinate of ligand and z_coordinate of protein
    lig_z_pos = np.mean([i[2] for i in lig_positions])
    prot_z_pos = np.mean([i[2] for i in prot_positions])

    #next find the max z coordinate of the protein on the side it's been oriented

    if lig_z_pos>prot_z_pos:
        max_z_pos = np.max([i[2] for i in prot_positions])
        z_coord = max_z_pos + z_padding
    else:
        min_z_pos = np.min([i[2] for i in prot_positions])
        z_coord = min_z_pos - z_padding

    if np.isnan(z_coord):
        raise ValueError('Could not find z_coord for funnel apex')

    return z_coord

def find_radius_and_center(ligand_pos, radius_scale_factor):

    cog = np.mean(ligand_pos, axis=0)

    distances = []
    #choose the two ligand atoms that are the furthest apart and use as estimate for cone mouth
    for k,i in enumerate(ligand_pos):
        for l,j in enumerate(ligand_pos):
            if k != l:
                distances.append(dist(i,j))

    rcyl = radius_scale_factor * np.max(distances)

    return rcyl,cog

def find_center_atom(center, array_pos):

    distances = []
    for i in array_pos:
        distances.append(dist(i,center))

    chosen = np.argmin(distances)

    return chosen, array_pos[chosen]

def get_angle_particle_coords(ligand_pos, prot_pos):

    distances = []
    indeces= []
    #choose the two ligand atoms that are the furthest apart
    for k,i in enumerate(ligand_pos):
        for l,j in enumerate(ligand_pos):
            if k != l:
                indeces.append([k,l])
                distances.append(dist(i,j))
    chosen_k = indeces[np.argmax(distances)][0]
    chosen_l = indeces[np.argmax(distances)][1]

    #choose the protein atom that is the closest to the chosen_k'th ligand atom
    distances = []
    for z in prot_pos:
        distances.append(dist(ligand_pos[chosen_k],z))
    chosen_z = np.argmin(distances)

    #load the coords and indeces in separate arrays
    three_coords = [ligand_pos[chosen_k],ligand_pos[chosen_l],prot_pos[chosen_z]]
    indeces = [int(chosen_k),int(chosen_l),int(chosen_z)]

    return three_coords, indeces

def dist(a,b):
    return np.linalg.norm(a-b)

def find_contacts(positions1, positions2, cutoff):

    contacts_i = []
    contacts_j = []
    for k,i in enumerate(positions1):
        for l,j in enumerate(positions2):
            if dist(i,j)<=cutoff:
                contacts_i.append(k)
                contacts_j.append(l)

    return contacts_i,contacts_j

def get_bound_site_cog(parmed, cutoff_in_angstroms):
    prot_sel = select_atoms(parmed, keyword_selection='protein')
    lig_sel = select_atoms(parmed, keyword_selection='ligand')
    coords = parmed.coordinates
    prot_coords=coords[prot_sel]
    lig_coords=coords[lig_sel]
    lig_contacts, prot_contacts = find_contacts(lig_coords,prot_coords,cutoff_in_angstroms)
    prot_contact_coords = prot_coords[np.unique(prot_contacts)]
    return np.mean(prot_contact_coords,axis=0)

def get_rotation_matrix(i_v, unit):

    # From http://www.j3d.org/matrix_faq/matrfaq_latest.html#Q38
    i_v /= np.linalg.norm(i_v)
    uvw = np.cross(i_v, unit)
    rcos = np.dot(i_v, unit)
    rsin = np.linalg.norm(uvw)

    if not np.isclose(rsin, 0):
        uvw /= rsin
    u, v, w = uvw

    # Compute rotation matrix
    return (
        rcos * np.eye(3) +
        rsin * np.array([
            [ 0, -w,  v],
            [ w,  0, -u],
            [-v,  u,  0]
        ]) +
        (1.0 - rcos) * uvw[:,None] * uvw[None,:]
    )