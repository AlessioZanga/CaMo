from ..structure import SCM

# TODO: figure_1_7_a = None
# TODO: figure_1_7_b = None
# TODO: figure_1_8 = None
# TODO: figure_1_9 = None
# TODO: figure_1_10 = None

figure_2_1 = SCM.from_structure(
    V={"X", "Y", "Z"},
    E={
        ("$U_X$", "X"),
        ("$U_Y$", "Y"),
        ("$U_Z$", "Z"),
        ("X", "Y"),
        ("Y", "Z")
    }
)

figure_2_2 = SCM.from_structure(
    V={"X", "Y", "Z"},
    E={
        ("$U_X$", "X"),
        ("$U_Y$", "Y"),
        ("$U_Z$", "Z"),
        ("X", "Y"),
        ("X", "Z")
    }
)

figure_2_3 = SCM.from_structure(
    V={"X", "Y", "Z"},
    E={
        ("$U_X$", "X"),
        ("$U_Y$", "Y"),
        ("$U_Z$", "Z"),
        ("X", "Z"),
        ("Y", "Z")
    }
)

# TODO: figure_2_4 = None
# TODO: figure_2_5 = None
# TODO: figure_2_6 = None

figure_2_7 = SCM.from_structure(
    V={"X", "Y", "Z", "W", "U"},
    E={
        ("$U_X$", "X"),
        ("$U_Y$", "Y"),
        ("$U_Z$", "Z"),
        ("$U_W$", "W"),
        ("$U_U$", "U"),
        ("X", "Y"),
        ("X", "W"),
        ("Z", "W"),
        ("W", "U")
    }
)

figure_2_8 = SCM.from_structure(
    V={"X", "Y", "Z", "W", "U", "T"},
    E={
        ("$U_X$", "X"),
        ("$U_Y$", "Y"),
        ("$U_Z$", "Z"),
        ("$U_W$", "W"),
        ("$U_U$", "U"),
        ("$U_T$", "T"),
        ("X", "Y"),
        ("X", "W"),
        ("Z", "W"),
        ("W", "U"),
        ("T", "Y"),
        ("T", "Z")
    }
)

# TODO: figure_2_9 = None

figure_3_1 = SCM.from_structure(
    V={"X", "Y", "Z"},
    E={
        ("$U_X$", "X"),
        ("$U_Y$", "Y"),
        ("$U_Z$", "Z"),
        ("Z", "X"),
        ("Z", "Y")
    }
)

figure_3_2 = SCM.from_structure(
    V={"X", "Y", "Z"},
    E={
        ("$U_Y$", "Y"),
        ("$U_Z$", "Z"),
        ("Z", "Y")
    }
)

# TODO: figure_3_3 = None
# TODO: figure_3_4 = None
# TODO: figure_3_5 = None

figure_3_6 = SCM.from_structure(
    V={"X", "Y", "W"},
    E={
        ("Z", "X"),
        ("Z", "W"),
        ("X", "Y"),
        ("W", "Y")
    }
)

figure_3_7 = SCM.from_structure(
    V={"A", "E", "X", "Y", "Z"},
    E={
        ("A", "Y"),
        ("A", "Z"),
        ("E", "X"),
        ("E", "Z"),
        ("X", "Y"),
        ("Z", "X"),
        ("Z", "Y")
    }
)

# TODO: figure_3_8 = None

figure_3_10_a = SCM.from_structure(
    V={"Smoking", "LungCancer"},
    E={
        ("Genotype", "Smoking"),
        ("Genotype", "LungCancer"),
        ("Smoking", "LungCancer")
    }
)

figure_3_10_b = SCM.from_structure(
    V={"Smoking", "LungCancer", "TarDeposits"},
    E={
        ("Genotype", "Smoking"),
        ("Genotype", "LungCancer"),
        ("Smoking", "TarDeposits"),
        ("TarDeposits", "LungCancer")
    }
)

# TODO: figure_3_11 = None
# TODO: figure_3_12 = None
# TODO: figure_3_13 = None
# TODO: figure_3_14 = None
# TODO: figure_3_15 = None
# TODO: figure_3_16 = None
# TODO: figure_3_17 = None
# TODO: figure_3_18 = None

# TODO: figure_4_1 = None
# TODO: figure_4_2 = None
# TODO: figure_4_3 = None
# TODO: figure_4_4_a = None
# TODO: figure_4_4_b = None
# TODO: figure_4_6_a = None
# TODO: figure_4_6_b = None
