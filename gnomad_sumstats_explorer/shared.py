"""Shared constants and functions for the gnomAD summary statistics explorer."""

from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_csv(
    app_dir / "../data/gnomad.exomes.v4.1.per_sample_variant_counts.csv",
    keep_default_na=False,
)

metrics = [
    "n_non_ref",
    "n_non_ref_alleles",
    "n_het",
    "n_hom_var",
    "n_hemi_var",
    "n_snp",
    "n_indel",
    "n_insertion",
    "n_deletion",
    "n_transition",
    "n_transversion",
    "n_singleton",
    "n_singleton_ti",
    "n_singleton_tv",
    "n_over_gq_60",
    "n_over_dp_20",
    "n_over_dp_30",
    "r_ti_tv",
    "r_ti_tv_singleton",
    "r_het_hom_var",
    "r_insertion_deletion",
    "n_high_ab_het_ref",
]
gen_anc_order = [
    "global",
    "afr",
    "amr",
    "asj",
    "eas",
    "fin",
    "mid",
    "nfe",
    "sas",
    "remaining",
]

GEN_ANC_NAMES = {
    "afr": "African/African-American",
    "ami": "Amish",
    "amr": "Admixed American",
    "asj": "Ashkenazi Jewish",
    "eas": "East Asian",
    "eur": "European",
    "fin": "Finnish",
    # NOTE: mde is kept for historical purposes, in gnomAD v3.1 mid was used instead
    "mde": "Middle Eastern",
    "mid": "Middle Eastern",
    "nfe": "Non-Finnish European",
    "oth": "Other",
    "remaining": "Remaining individuals",
    "sas": "South Asian",
    "uniform": "Uniform",
    "sas_non_consang": "South Asian (F < 0.05)",
    "consanguineous": "South Asian (F > 0.05)",
    "exac": "ExAC",
    "bgr": "Bulgarian (Eastern European)",
    "est": "Estonian",
    "gbr": "British",
    "nwe": "North-Western European",
    "seu": "Southern European",
    "swe": "Swedish",
    "kor": "Korean",
    "sgp": "Singaporean",
    "jpn": "Japanese",
    "oea": "Other East Asian",
    "oeu": "Other European",
    "onf": "Other Non-Finnish European",
    "unk": "Unknown",
    "global": "All",
}

GEN_ANC_COLORS = {
    "afr": "#941494",
    "ami": "#FFC0CB",
    "amr": "#ED1E24",
    "asj": "#FF7F50",
    "eas": "#108C44",
    "eur": "#6AA5CD",
    "fin": "#002F6C",
    "mde": "#33CC33",
    "nfe": "#6AA5CD",
    "oth": "#ABB9B9",
    "sas": "#FF9912",
    "uniform": "pink",
    "consanguineous": "pink",
    "sas_non_consang": "orange",
    "exac": "gray",
    "bgr": "#66C2A5",
    "est": "black",
    "gbr": "#C60C30",
    "nwe": "#C60C30",
    "seu": "#3CA021",
    "swe": "purple",
    "kor": "#4891D9",
    "sgp": "darkred",
    "jpn": "#BC002D",
    "oea": "#108C44",
    "oeu": "#6AA5CD",
    "onf": "#6AA5CD",
    "unk": "#ABB9B9",
    "remaining": "#ABB9B9",
    "": "#ABB9B9",
    "mid": "#33CC33",
    "global": "#000000",
}
color_map = {GEN_ANC_NAMES[x]: GEN_ANC_COLORS[x] for x in gen_anc_order}
gen_anc_order_mapped = [GEN_ANC_NAMES[x] for x in gen_anc_order]

# Used Paul Tol's muted palette with added colors:
# white, #000000, #004488
# This still isn't accessible for monochromacy/achromatopsia
GEN_ANC_COLORS_ACCESSIBLE = {
    "afr": "#CC6677",
    "ami": "#332288",
    "amr": "#DDCC77",
    "asj": "#117733",
    "eas": "#88CCEE",
    "eur": "#882255",
    "fin": "#44AA99",
    "nfe": "#999933",
    "sas": "#AA4499",
    "remaining": "white",
    "mid": "#004488",
    "global": "#000000",
}
accessible_color_map = {
    GEN_ANC_NAMES[x]: GEN_ANC_COLORS_ACCESSIBLE[x] for x in gen_anc_order
}
