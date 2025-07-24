import requests
import os
from Bio.PDB.MMCIFParser import MMCIFParser

def download_cif(pdb_id: str, save_dir: str = "./pdb_files") -> str:
    os.makedirs(save_dir, exist_ok=True)
    url = f"https://files.rcsb.org/download/{pdb_id.upper()}.cif"
    save_path = os.path.join(save_dir, f"{pdb_id.upper()}.cif")
    r = requests.get(url)
    if r.status_code != 200:
        raise ValueError(f"Failed to download CIF file for {pdb_id}")
    with open(save_path, "wb") as f:
        f.write(r.content)
    return save_path

def extract_metadata(cif_path: str) -> dict:
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure("structure", cif_path)
    mmcif_dict = parser._mmcif_dict

    def get_field(key_list, default="N/A"):
        for key in key_list:
            val = mmcif_dict.get(key)
            if val:
                return val[0]
        return default

    metadata = {
        "resolution": get_field(["_refine.ls_d_res_high"]),
        "source_organism": get_field([
            "_entity_src_nat.pdbx_organism_scientific",
            "_entity_src_gen.pdbx_gene_src_scientific_name"
        ]),
        "expression_system": get_field([
            "_entity_src_gen.pdbx_host_org_scientific_name",
            "_entity_src_nat.pdbx_host_org_scientific_name"
        ]),
        "deposition_date": get_field(["_pdbx_database_status.recvd_initial_deposition_date"]),
        "release_date": get_field(["_pdbx_database_status.entry_release_date"]),
        "prevenance_details": get_field(["_exptl.method"]),
        "status_code": get_field(["_pdbx_database_status.status_code"]),
        "submitter": get_field(["_audit_author.name"]),
        "citation_title": get_field(["_citation.title"]),
        "citation_journal": get_field(["_citation.journal_abbrev"]),
    }
    return metadata

def query_pdb(pdb_id: str):
    try:
        cif_path = download_cif(pdb_id)
        metadata = extract_metadata(cif_path)
        return metadata
    except Exception as e:
        return {f" Error for {pdb_id}: {e}"}