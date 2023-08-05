import numpy
from typing import NoReturn
from cryspy.A_functions_base.function_1_matrices import\
    calc_product_matrices, calc_product_matrix_vector
from cryspy.B_parent_classes.cl_1_item import ItemN
from cryspy.B_parent_classes.cl_2_loop import LoopN
from cryspy.C_item_loop_classes.cl_1_cell import Cell


class PdInstrReflexAsymmetry(ItemN):
    """
    PdInstrReflexAsymmetry describes asymmetry of Bragg reflections for
    1d powder diffractometer.

    Mandatory attributes:
        - ub_11, ub_12, ub_13, ub_21, ub_22, ub_23, ub_31, ub_32, ub_33

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
    ATTR_MANDATORY_NAMES = ("p1", "p2", "p3", "p4")
    ATTR_MANDATORY_TYPES = (float, float, float, float)
    ATTR_MANDATORY_CIF = ("p1", "p2", "p3", "p4")

    ATTR_OPTIONAL_NAMES = ()
    ATTR_OPTIONAL_TYPES = ()
    ATTR_OPTIONAL_CIF = ()

    ATTR_NAMES = ATTR_MANDATORY_NAMES + ATTR_OPTIONAL_NAMES
    ATTR_TYPES = ATTR_MANDATORY_TYPES + ATTR_OPTIONAL_TYPES
    ATTR_CIF = ATTR_MANDATORY_CIF + ATTR_OPTIONAL_CIF

    ATTR_INT_NAMES = ()
    ATTR_INT_PROTECTED_NAMES = ()

    # parameters considered are refined parameters
    ATTR_REF = ("p1", "p2", "p3", "p4")
    ATTR_SIGMA = tuple([f"{_h:}_sigma" for _h in ATTR_REF])
    ATTR_CONSTR_FLAG = tuple([f"{_h:}_constraint" for _h in ATTR_REF])
    ATTR_REF_FLAG = tuple([f"{_h:}_refinement" for _h in ATTR_REF])

    # constraints on the parameters
    D_CONSTRAINTS = {}

    # default values for the parameters
    D_DEFAULT = {}
    for key in ATTR_SIGMA:
        D_DEFAULT[key] = 0.
    for key in (ATTR_CONSTR_FLAG + ATTR_REF_FLAG):
        D_DEFAULT[key] = False

    PREFIX = "pd_instr_reflex_asymmetry"

    def __init__(self, **kwargs) -> NoReturn:
        super(PdInstrReflexAsymmetry, self).__init__()

        # defined for any integer and float parameters
        D_MIN = {"ttheta": 0}

        # defined for ani integer and float parameters
        D_MAX = {}

        self.__dict__["D_MIN"] = D_MIN
        self.__dict__["D_MAX"] = D_MAX
        for key, attr in self.D_DEFAULT.items():
            setattr(self, key, attr)
        for key, attr in kwargs.items():
            setattr(self, key, attr)

    def _func_fa(self, tth):
        """
        For assymmetry correction F_a(z).
        """ 
        return 2*tth*numpy.exp(-tth**2)
        
    def _func_fb(self, tth):
        """
        For assymmetry correction F_b(z)
        """ 
        return 2.*(2.*tth**2-3.)* self._func_fa(tth)
        
    def calc_asymmetry(self, tth, tth_hkl, fwhm):
        """
        Calculate asymmetry coefficients for  on the given list ttheta for 
        bragg reflections flaced on the position ttheta_hkl
        tth and tth_hkl in degrees.

        look page 54 in FullProf Manual
        """
        tth_2d, tth_hkl_2d = numpy.meshgrid(tth, tth_hkl, indexing="ij")
        np_zero = numpy.zeros(tth_2d.shape, dtype = float)
        np_one = numpy.ones(tth_2d.shape, dtype = float)
        val_1, val_2 = np_zero, np_zero
        
        z_2d = (tth_2d - tth_hkl_2d)/fwhm[numpy.newaxis, :]
        
        p1, p2 = float(self.p1), float(self.p2)
        p3, p4 = float(self.p3), float(self.p4)
        flag_1, flag_2 = False, False
        if ((p1!= 0.)|(p3!= 0.)):
            flag_1 = True
            fa = self._func_fa(z_2d)
        if ((p2!= 0.)|(p4!= 0.)):
            flag_2 = True
            fb = self._func_fb(z_2d)
            
        flag_3, flag_4 = False, False
        if ((p1!= 0.)|(p2!= 0.)):
            if flag_1:
                val_1 += p1*fa
                flag_3 = True
            if flag_2:
                val_1 += p2*fb
                flag_3 = True
            if flag_3:
                c1 = 1./numpy.tanh(0.5*tth_hkl)
                val_1 *= c1[numpy.newaxis, :]

        if ((p3!= 0.)|(p4!= 0.)):
            if flag_1:
                val_2 += p3*fa
                flag_4 = True
            if flag_2:
                val_2 += p4*fb
                flag_4 = True
            if flag_4:
                c2 = 1./numpy.tanh(tth_hkl)
                val_2 *= c2[numpy.newaxis, :]

        asymmetry_2d = np_one+val_1+val_2
        return asymmetry_2d


class PdInstrReflexAsymmetryL(LoopN):
    """
    Description of AtomSite in loop.

    """
    ITEM_CLASS = PdInstrReflexAsymmetry
    ATTR_INDEX = None
    def __init__(self, loop_name = None) -> NoReturn:
        super(PdInstrReflexAsymmetryL, self).__init__()
        self.__dict__["items"] = []
        self.__dict__["loop_name"] = loop_name
   

# s_cont = """
#  loop_
#  _pd_instr_reflex_asymmetry_p1
#  _pd_instr_reflex_asymmetry_p2
#  _pd_instr_reflex_asymmetry_p3
#  _pd_instr_reflex_asymmetry_p4
#  0.0 0.0 0.0 0.0
#  1.0 0.1 0.5 0.17(78)
# """

# obj = PdInstrReflexAsymmetryL.from_cif(s_cont)
# print(obj, end="\n\n")

