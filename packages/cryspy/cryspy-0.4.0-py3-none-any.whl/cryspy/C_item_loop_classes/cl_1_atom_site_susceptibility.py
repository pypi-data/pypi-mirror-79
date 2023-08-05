"""Describe AtomSiteSusceptibility, AtomSiteSusceptibilityL."""
from typing import NoReturn
from cryspy.A_functions_base.function_1_atomic_vibrations import \
    vibration_constraints
from cryspy.B_parent_classes.cl_1_item import ItemN
from cryspy.B_parent_classes.cl_2_loop import LoopN


class AtomSiteSusceptibility(ItemN):
    """
    AtomSiteSusceptibility class.

    Data items in the ATOM_SITE_MAGNETISM_ANISO category record details about
    magnetic properties of the atoms that occupy the atom sites.

    Mandatory attributes:
        - label
        - type_symbol
        - fract_x
        - fract_y
        - fract_z

    Optional attributes:
        - occupancy
        - adp_type
        - u_iso_or_equiv
        - u_equiv_geom_mean
        - b_iso_or_equiv
        - multiplicity
        - wyckoff_symbol
        - cartn_x
        - cartn_y
        - cartn_z

    Internal attributes:
        - scat_length_neutron

    Internal protected attributes:
        - space_group_wyckoff
        - constr_number
    """

    ATTR_MANDATORY_NAMES = ("label", )
    ATTR_MANDATORY_TYPES = (str, )
    ATTR_MANDATORY_CIF = ("label", )

    ATTR_OPTIONAL_NAMES = (
        "chi_type", "moment_type", "chi_11", "chi_22", "chi_33", "chi_12",
        "chi_13", "chi_23", "moment_11", "moment_22", "moment_33", "moment_12",
        "moment_13", "moment_23")
    ATTR_OPTIONAL_TYPES = (str, str, float, float, float, float, float, float,
                           float, float, float, float, float, float)
    ATTR_OPTIONAL_CIF = (
        "chi_type", "moment_type", "chi_11", "chi_22", "chi_33", "chi_12",
        "chi_13", "chi_23", "moment_11", "moment_22", "moment_33", "moment_12",
        "moment_13", "moment_23")

    ATTR_NAMES = ATTR_MANDATORY_NAMES + ATTR_OPTIONAL_NAMES
    ATTR_TYPES = ATTR_MANDATORY_TYPES + ATTR_OPTIONAL_TYPES
    ATTR_CIF = ATTR_MANDATORY_CIF + ATTR_OPTIONAL_CIF

    ATTR_INT_NAMES = ()
    ATTR_INT_PROTECTED_NAMES = ()

    # parameters considered are refined parameters
    ATTR_REF = ("chi_11", "chi_22", "chi_33", "chi_12", "chi_13", "chi_23",
                "moment_11", "moment_22", "moment_33", "moment_12",
                "moment_13", "moment_23")
    ATTR_SIGMA = tuple([f"{_h:}_sigma" for _h in ATTR_REF])
    ATTR_CONSTR_FLAG = tuple([f"{_h:}_constraint" for _h in ATTR_REF])
    ATTR_REF_FLAG = tuple([f"{_h:}_refinement" for _h in ATTR_REF])

    # formats if cif format
    D_FORMATS = {"chi_11": "{:.5f}", "chi_22": "{:.5f}", "chi_33": "{:.5f}",
                 "chi_12": "{:.5f}", "chi_13": "{:.5f}", "chi_23": "{:.5f}",
                 "moment_11": "{:.5f}", "moment_22": "{:.5f}",
                 "moment_33": "{:.5f}", "moment_12": "{:.5f}",
                 "moment_13": "{:.5f}", "moment_23": "{:.5f}"}

    # constraints on the parameters
    D_CONSTRAINTS = {"chi_type": ["Ciso", "Cani"],
                     "moment_type": ["Miso", "Mani"]}

    # default values for the parameters
    D_DEFAULT = {}
    for key in ATTR_SIGMA:
        D_DEFAULT[key] = 0.
    for key in (ATTR_CONSTR_FLAG + ATTR_REF_FLAG):
        D_DEFAULT[key] = False

    PREFIX = "atom_site_susceptibility"

    def __init__(self, **kwargs) -> NoReturn:
        super(AtomSiteSusceptibility, self).__init__()

        # defined for any integer and float parameters
        D_MIN = {}

        # defined for ani integer and float parameters
        D_MAX = {}

        self.__dict__["D_MIN"] = D_MIN
        self.__dict__["D_MAX"] = D_MAX
        for key, attr in self.D_DEFAULT.items():
            setattr(self, key, attr)
        for key, attr in kwargs.items():
            setattr(self, key, attr)

    def apply_space_group_constraint(self, atom_site, space_group):
        """
        Space group constraints.

        According to table 1 in Peterse, Palm, Acta Cryst.(1966), 20, 147
        """
        l_numb = atom_site.calc_constr_number(space_group)
        label_aniso = self.label
        label = atom_site.label
        index = label.index(label_aniso)

        flag_chi = (self.chi_type is not None)
        if flag_chi:
            flag_chi = self.chi_type.lower().startswith("cani")
        flag_moment = (self.moment_type is not None)
        if flag_moment:
            flag_moment = self.moment_type.lower().startswith("mani")
        if flag_chi:
            self.__dict__["chi_11_constraint"] = False
            self.__dict__["chi_22_constraint"] = False
            self.__dict__["chi_33_constraint"] = False
            self.__dict__["chi_12_constraint"] = False
            self.__dict__["chi_13_constraint"] = False
            self.__dict__["chi_23_constraint"] = False
        if flag_moment:
            self.__dict__["moment_11_constraint"] = False
            self.__dict__["moment_22_constraint"] = False
            self.__dict__["moment_33_constraint"] = False
            self.__dict__["moment_12_constraint"] = False
            self.__dict__["moment_13_constraint"] = False
            self.__dict__["moment_23_constraint"] = False
        numb = l_numb[index]

        if flag_chi:
            chi_i = (self.chi_11, self.chi_22, self.chi_33, self.chi_12,
                     self.chi_13, self.chi_23)
            chi_sigma_i = (self.chi_11_sigma, self.chi_22_sigma,
                           self.chi_33_sigma, self.chi_12_sigma,
                           self.chi_13_sigma, self.chi_23_sigma)
            chi_ref_i = (self.chi_11_refinement, self.chi_22_refinement,
                         self.chi_33_refinement, self.chi_12_refinement,
                         self.chi_13_refinement, self.chi_23_refinement)

            chi_i, chi_sigma_i, chi_ref_i, chi_constr_i = \
                vibration_constraints(numb, chi_i, chi_sigma_i, chi_ref_i)

            self.__dict__["chi_11"], self.__dict__["chi_22"], \
                self.__dict__["chi_33"], self.__dict__["chi_12"], \
                self.__dict__["chi_13"], self.__dict__["chi_23"] = chi_i

            self.__dict__["chi_11_sigma"], self.__dict__["chi_22_sigma"], \
                self.__dict__["chi_33_sigma"], self.__dict__["chi_12_sigma"], \
                self.__dict__["chi_13_sigma"], self.__dict__["chi_23_sigma"] =\
                chi_sigma_i

            self.__dict__["chi_11_refinement"], \
                self.__dict__["chi_22_refinement"], \
                self.__dict__["chi_33_refinement"], \
                self.__dict__["chi_12_refinement"], \
                self.__dict__["chi_13_refinement"], \
                self.__dict__["chi_23_refinement"] = chi_ref_i

            self.__dict__["chi_11_constraint"], \
                self.__dict__["chi_22_constraint"], \
                self.__dict__["chi_33_constraint"], \
                self.__dict__["chi_12_constraint"], \
                self.__dict__["chi_13_constraint"], \
                self.__dict__["chi_23_constraint"] = chi_constr_i
        if flag_moment:
            moment_i = (self.moment_11, self.moment_22, self.moment_33,
                        self.moment_12, self.moment_13, self.moment_23)
            moment_sigma_i = (self.moment_11_sigma, self.moment_22_sigma,
                              self.moment_33_sigma, self.moment_12_sigma,
                              self.moment_13_sigma, self.moment_23_sigma)
            moment_ref_i = (
                self.moment_11_refinement, self.moment_22_refinement,
                self.moment_33_refinement, self.moment_12_refinement,
                self.moment_13_refinement, self.moment_23_refinement)

            moment_i, moment_sigma_i, moment_ref_i, moment_constr_i = \
                vibration_constraints(numb, moment_i, moment_sigma_i,
                                      moment_ref_i)

            self.__dict__["moment_11"], self.__dict__["moment_22"], \
                self.__dict__["moment_33"], self.__dict__["moment_12"], \
                self.__dict__["moment_13"], self.__dict__["moment_23"] = \
                moment_i

            self.__dict__["moment_11_sigma"], \
                self.__dict__["moment_22_sigma"], \
                self.__dict__["moment_33_sigma"], \
                self.__dict__["moment_12_sigma"], \
                self.__dict__["moment_13_sigma"], \
                self.__dict__["moment_23_sigma"] = moment_sigma_i

            self.__dict__["moment_11_refinement"], \
                self.__dict__["moment_22_refinement"], \
                self.__dict__["moment_33_refinement"], \
                self.__dict__["moment_12_refinement"], \
                self.__dict__["moment_13_refinement"], \
                self.__dict__["moment_23_refinement"] = moment_ref_i

            self.__dict__["moment_11_constraint"], \
                self.__dict__["moment_22_constraint"], \
                self.__dict__["moment_33_constraint"], \
                self.__dict__["moment_12_constraint"], \
                self.__dict__["moment_13_constraint"], \
                self.__dict__["moment_23_constraint"] = moment_constr_i

    def apply_chi_iso_constraint(self, cell):
        """Isotropic constraint on susceptibility."""
        c_a = cell.cos_a
        s_ib = cell.sin_ib
        s_ig = cell.sin_ig
        c_ib = cell.cos_ib
        c_ig = cell.cos_ig
        # not sure, it is better to check
        chi_type = self.chi_type
        if chi_type is None:
            return
        if chi_type.lower().startswith("ciso"):
            self.__dict__["chi_22"] = self.chi_11
            self.__dict__["chi_33"] = self.chi_11
            self.__dict__["chi_12"] = self.chi_11*c_ig
            self.__dict__["chi_13"] = self.chi_11*c_ib
            self.__dict__["chi_23"] = self.chi_11*(c_ib*c_ig-s_ib*s_ig*c_a)
            self.__dict__["chi_22_sigma"] = self.chi_11_sigma
            self.__dict__["chi_33_sigma"] = self.chi_11_sigma
            self.__dict__["chi_12_sigma"] = self.chi_11_sigma * c_ig
            self.__dict__["chi_13_sigma"] = self.chi_11_sigma * c_ib
            self.__dict__["chi_23_sigma"] = self.chi_11_sigma * \
                (c_ib*c_ig-s_ib*s_ig*c_a)
            self.__dict__["chi_22_refinement"] = False
            self.__dict__["chi_33_refinement"] = False
            self.__dict__["chi_12_refinement"] = False
            self.__dict__["chi_13_refinement"] = False
            self.__dict__["chi_23_refinement"] = False
            self.__dict__["chi_22_constraint"] = True
            self.__dict__["chi_33_constraint"] = True
            self.__dict__["chi_12_constraint"] = True
            self.__dict__["chi_13_constraint"] = True
            self.__dict__["chi_23_constraint"] = True

    def apply_moment_iso_constraint(self, cell):
        """Isotropic constraint on moment."""
        c_a = cell.cos_a
        s_ib = cell.sin_ib
        s_ig = cell.sin_ig
        c_ib = cell.cos_ib
        c_ig = cell.cos_ig
        # not sure, it is better to check
        moment_type = self.moment_type
        if moment_type is None:
            return
        if moment_type.lower().startswith("miso"):
            self.__dict__["moment_22"] = self.moment_11
            self.__dict__["moment_33"] = self.moment_11
            self.__dict__["moment_12"] = self.moment_11 * c_ig
            self.__dict__["moment_13"] = self.moment_11 * c_ib
            self.__dict__["moment_23"] = self.moment_11 * \
                (c_ib*c_ig-s_ib*s_ig*c_a)

            self.__dict__["moment_22_sigma"] = self.moment_11_sigma
            self.__dict__["moment_33_sigma"] = self.moment_11_sigma
            self.__dict__["moment_12_sigma"] = self.moment_11_sigma * c_ig
            self.__dict__["moment_13_sigma"] = self.moment_11_sigma * c_ib
            self.__dict__["moment_23_sigma"] = self.moment_11_sigma * \
                (c_ib*c_ig-s_ib*s_ig*c_a)

            self.__dict__["moment_22_refinement"] = False
            self.__dict__["moment_33_refinement"] = False
            self.__dict__["moment_12_refinement"] = False
            self.__dict__["moment_13_refinement"] = False
            self.__dict__["moment_23_refinement"] = False
            self.__dict__["moment_22_constraint"] = True
            self.__dict__["moment_33_constraint"] = True
            self.__dict__["moment_12_constraint"] = True
            self.__dict__["moment_13_constraint"] = True
            self.__dict__["moment_23_constraint"] = True


class AtomSiteSusceptibilityL(LoopN):
    """
    Description of AtomSite in loop.

    Methods
    -------
        - apply_space_group_constraint
        - apply_chi_iso_constraint
        - apply_moment_iso_constraint
    """

    ITEM_CLASS = AtomSiteSusceptibility
    ATTR_INDEX = "label"

    def __init__(self, loop_name=None) -> NoReturn:
        super(AtomSiteSusceptibilityL, self).__init__()
        self.__dict__["items"] = []
        self.__dict__["loop_name"] = loop_name

    def apply_space_group_constraint(self, atom_site, space_group):
        """Apply space group constraint."""
        for item in self.items:
            item.apply_space_group_constraint(atom_site, space_group)

    def apply_chi_iso_constraint(self, cell):
        """Apply isotropic constraint on susceptibility."""
        for item in self.items:
            item.apply_chi_iso_constraint(cell)

    def apply_moment_iso_constraint(self, cell):
        """Apply isotropic constraint on moments."""
        for item in self.items:
            item.apply_moment_iso_constraint(cell)

# s_cont = """
#  loop_
#  _atom_site_susceptibility_label
#  _atom_site_susceptibility_chi_type
#  _atom_site_susceptibility_chi_11
#  _atom_site_susceptibility_chi_12
#  _atom_site_susceptibility_chi_13
#  _atom_site_susceptibility_chi_22
#  _atom_site_susceptibility_chi_23
#  _atom_site_susceptibility_chi_33
#  _atom_site_susceptibility_moment_type
#  _atom_site_susceptibility_moment_11
#  _atom_site_susceptibility_moment_12
#  _atom_site_susceptibility_moment_13
#  _atom_site_susceptibility_moment_22
#  _atom_site_susceptibility_moment_23
#  _atom_site_susceptibility_moment_33
#   Fe3A Cani -3.468(74) 0.0 0.0 -3.468 0.0 -3.468 Mani 0. 0. 0. 0. 0. 0.
#   Fe3B Cani 3.041      0.0 0.0  3.041 0.0  3.041 Mani 0. 0. 0. 0. 0. 0.
#   """

# obj = AtomSiteSusceptibilityL.from_cif(s_cont)
# print(obj, end="\n\n")
# print(obj["Fe3A"], end="\n\n")
