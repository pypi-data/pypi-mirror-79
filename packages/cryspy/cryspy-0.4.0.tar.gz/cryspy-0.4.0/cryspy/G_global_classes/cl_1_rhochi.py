"""Description of RhoChi class."""
__author__ = 'ikibalin'
__version__ = "2020_08_19"
import os
import os.path
import numpy
from typing import NoReturn
import scipy
import scipy.optimize

from cryspy.A_functions_base.function_1_error_simplex import \
    error_estimation_simplex

from cryspy.B_parent_classes.cl_4_global import GlobalN

from cryspy.E_data_classes.cl_1_crystal import Crystal
from cryspy.E_data_classes.cl_2_diffrn import Diffrn
from cryspy.E_data_classes.cl_2_pd import Pd
from cryspy.E_data_classes.cl_2_pd2d import Pd2d


class RhoChi(GlobalN):
    """
    Class to describe RhoChi class.

    Attributes
    ----------
        - crystal_#name (mandatory)
        - diffrn_#name
        - pd_#name
        - pd2d_#name

    Methods
    -------
        - crystals()
        - experiments()
        - refine()
        - calc_chi_sq
        - params_to_cif
        - data_to_cif
        - calc_to_cif
        - estimate_FM


    """

    CLASSES_MANDATORY = (Crystal, )
    CLASSES_OPTIONAL = (Diffrn, Pd, Pd2d, )
    # CLASSES_INTERNAL = ()

    CLASSES = CLASSES_MANDATORY + CLASSES_OPTIONAL

    PREFIX = "rhochi"

    # default values for the parameters
    D_DEFAULT = {}

    def __init__(self, global_name=None, **kwargs) -> NoReturn:
        super(RhoChi, self).__init__()

        self.__dict__["items"] = []
        self.__dict__["global_name"] = global_name

        for key, attr in self.D_DEFAULT.items():
            setattr(self, key, attr)
        for key, attr in kwargs.items():
            setattr(self, key, attr)

    def form_object(self):
        """Form object."""
        self.apply_constraint()

    def apply_constraint(self):
        """Apply constraints."""
        for item in self.items:
            if isinstance(item, Crystal):
                item.apply_constraint()

    def experiments(self):
        """List of expreiments."""
        return [item for item in self.items if isinstance(item, (Diffrn, Pd,
                                                                 Pd2d))]

    def crystals(self):
        """List of crystals."""
        return [item for item in self.items if isinstance(item, Crystal)]

    def calc_chi_sq(self, flag_internal=True):
        """
        Calculate chi square.

        Keyword Arguments
        -----------------
            - flag_internal: a flag to calculate internal objects
              (default is True)

        Output arguments
        ----------------
            - chi_sq_val: chi square of flip ratio
              (Sum_i ((y_e_i - y_m_i) / sigma_i)**2)
            - n: number of measured reflections
        """
        self.apply_constraint()

        l_crystal = self.crystals()

        chi_sq_res, n_res = 0., 0.
        for experiment in self.experiments():
            chi_sq, n = experiment.calc_chi_sq(l_crystal,
                                               flag_internal=flag_internal)
            experiment.chi_sq = chi_sq
            experiment.n = n
            chi_sq_res += chi_sq
            n_res += n
        return chi_sq_res, n_res

    def refine(self, disp: bool = False, optimization_method: str = "BFGS"):
        """
        Minimization procedure.

        Accesible parameters for optimization_method
        --------------------------------------------
            - "BFGS" (default)
            - "simplex"
            - "basinhopping"
        """
        flag = True

        # self.remove_internal_objs

        self.apply_constraint()
        l_var_name = self.get_variable_names()

        if len(l_var_name) == 0:
            chi_sq, n = self.calc_chi_sq()
            # self._show_message(f"chi_sq/n {chi_sq/n:.2f} (n = {int(n):}).")
            dict_out = {"flag": flag, "res": None, "chi_sq": chi_sq, "n": n}
            return dict_out

        val_0 = numpy.array([self.get_variable_by_name(var_name)
                             for var_name in l_var_name], dtype=float)

        sign = 2*(numpy.array(val_0 >= 0., dtype=int)-0.5)
        param_0 = numpy.log(abs(val_0)*(numpy.e-1.)+1.)*sign
        coeff_norm = numpy.where(val_0 == 0., 1., val_0) / \
            numpy.where(param_0 == 0., 1., param_0)
        hes_coeff_norm = numpy.matmul(coeff_norm[:, numpy.newaxis],
                                      coeff_norm[numpy.newaxis, :])

        chi_sq, n = self.calc_chi_sq(flag_internal=True)

        def tempfunc(l_param):
            for var_name, param, coeff in zip(l_var_name, l_param, coeff_norm):
                self.set_variable_by_name(var_name, param*coeff)
            chi_sq, n_points = self.calc_chi_sq(flag_internal=False)
            if n_points < n:
                res_out = 1.0e+308
            else:
                res_out = (chi_sq*1./float(n_points))
            return res_out

        if optimization_method == "basinhopping":
            # basinhopping
            res = scipy.optimize.basinhopping(
                tempfunc, param_0, niter=10, T=10, stepsize=0.1, interval=20,
                disp=disp)
            _dict_out = {"flag": flag, "res": res}
        elif optimization_method == "simplex":
            # simplex
            res = scipy.optimize.minimize(
                tempfunc, param_0, method='Nelder-Mead',
                callback=lambda x: self._f_callback(disp, coeff_norm, x),
                options={"fatol": 0.01*n})

            m_error, dist_hh = error_estimation_simplex(
                res["final_simplex"][0], res["final_simplex"][1], tempfunc)

            l_sigma = []
            for i, val_2 in zip(range(m_error.shape[0]), dist_hh):
                # slightly change definition, instead of (n-k) here is n
                error = (abs(m_error[i, i])*1./n)**0.5
                if m_error[i, i] < 0.:
                    raise UserWarning("Negative diagonal elements of Hessian")
                if val_2 > error:
                    raise UserWarning("Minimum is not found")

                l_sigma.append(max(error, val_2))

            for var_name, sigma, coeff in \
                    zip(l_var_name, l_sigma, coeff_norm):
                hh = tuple((f"{var_name[-1][0]:}_sigma", ) + var_name[-1][1:])
                var_name_sigma = tuple(var_name[:-1]+(hh, ))
                self.set_variable_by_name(var_name_sigma, sigma*coeff)

            _dict_out = {"flag": flag, "res": res}
        else:
            # BFGS
            res = scipy.optimize.minimize(
                tempfunc, param_0, method='BFGS',
                callback=lambda x: self._f_callback(disp, coeff_norm, x),
                options={"disp": disp})

            _dict_out = {"flag": flag, "res": res}

            hess_inv = res["hess_inv"] * hes_coeff_norm
            l_param = res["x"]
            l_sigma = (abs(numpy.diag(hess_inv)*1./float(n)))**0.5
            for var_name, sigma, param, coeff in \
                    zip(l_var_name, l_sigma, l_param, coeff_norm):
                hh = tuple((f"{var_name[-1][0]:}_sigma", ) + var_name[-1][1:])
                var_name_sigma = tuple(var_name[:-1]+(hh, ))
                self.set_variable_by_name(var_name_sigma, sigma)
                self.set_variable_by_name(var_name, param*coeff)

        chi_sq, n = self.calc_chi_sq(flag_internal=True)

        return _dict_out

    def _f_callback(self, *arg):
        disp = arg[0]
        if disp:
            coeff_norm = arg[1]
            res_x = arg[2]
            ls_out = " ".join(["{:12.5f}".format(_1*_2)
                               for _1, _2 in zip(res_x, coeff_norm)])
            print(ls_out)

    def save_to_file(self, f_name):
        """Save to file."""
        self.file_input = f_name
        if os.path.basename(f_name) == "main.rcif":
            self.save_to_files()
        else:
            with open(f_name, "w") as fid:
                fid.write(self.to_cif())

    def save_to_files(self):
        """Save to files."""
        if self.file_input is None:
            f_dir = "."
        else:
            f_dir = os.path.dirname(self.file_input)
        f_main = os.path.join(f_dir, "main.rcif")
        ls_main = []
        ls_main.append("global_{:}\n".format(self.global_name))
        for experiment in self.experiments():
            ls_main.append(f"_add_url {experiment.data_name:}_data.rcif\n")
            ls_main.append(f"_add_url {experiment.data_name:}_calc.rcif\n")
        for crystal in self.crystals():
            ls_main.append("\n"+crystal.to_cif())
        for experiment in self.experiments():
            ls_main.append("\ndata_{:}".format(experiment.data_name))
            ls_main.append(experiment.params_to_cif())

            f_data = os.path.join(f_dir, f"{experiment.data_name:}_data.rcif")
            ls_data = []
            ls_data.append("\ndata_{:}".format(experiment.data_name))
            ls_data.append(experiment.data_to_cif())
            with open(f_data, 'w') as fid:
                fid.write("\n".join(ls_data))
            f_calc = os.path.join(f_dir, f"{experiment.data_name:}_calc.rcif")
            ls_calc = []
            ls_calc.append("\ndata_{:}".format(experiment.data_name))
            ls_calc.append(experiment.calc_to_cif())
            with open(f_calc, 'w') as fid:
                fid.write("\n".join(ls_calc))
        with open(f_main, 'w') as fid:
            fid.write("\n".join(ls_main))


# s_cont = """
# global_
#  data_Fe3O4
#  _cell_angle_alpha 90.0
#  _cell_angle_beta 90.0
#  _cell_angle_gamma 90.0
#  _cell_length_a 8.56212()
#  _cell_length_b 8.56212
#  _cell_length_c 8.56212
#  _space_group_it_coordinate_system_code 2
#  _space_group_IT_number    227
#  loop_
#  _atom_site_adp_type
#  _atom_site_B_iso_or_equiv
#  _atom_site_fract_x
#  _atom_site_fract_y
#  _atom_site_fract_z
#  _atom_site_label
#  _atom_site_occupancy
#  _atom_site_type_symbol
#   Uani 0.0 0.125 0.125 0.125 Fe3A 1.0 Fe3+
#   Uani 0.0 0.5 0.5 0.5 Fe3B 1.0 Fe3+
#   Uiso 0.0 0.25521 0.25521 0.25521 O1 1.0 O2-
#  loop_
#  _atom_type_scat_length_neutron
#  _atom_type_symbol
#    0.945 Fe3+
#   0.5803 O2-
#  loop_
#  _atom_site_aniso_U_11
#  _atom_site_aniso_U_12
#  _atom_site_aniso_U_13
#  _atom_site_aniso_U_22
#  _atom_site_aniso_U_23
#  _atom_site_aniso_U_33
#  _atom_site_aniso_label
#   0.0 0.0 0.0 0.0 0.0 0.0 Fe3A
#   0.0 0.0 0.0 0.0 0.0 0.0 Fe3B
#  loop_
#  _atom_site_scat_label
#  _atom_site_scat_lande
#  Fe3A 2.0
#  Fe3B 2.0
#  loop_
#  _atom_site_susceptibility_label
#  _atom_site_susceptibility_chi_type
#  _atom_site_susceptibility_chi_11
#  _atom_site_susceptibility_chi_12
#  _atom_site_susceptibility_chi_13
#  _atom_site_susceptibility_chi_22
#  _atom_site_susceptibility_chi_23
#  _atom_site_susceptibility_chi_33
#   Fe3A Cani -3.468(74) 0.0 0.0 -3.468 0.0 -3.468
#   Fe3B Cani 3.041      0.0 0.0  3.041 0.0  3.041
#  data_mono
#  _setup_wavelength     0.840
#  _setup_field          1.000
#  _diffrn_radiation_polarization 1.0
#  _diffrn_radiation_efficiency   1.0
#  _extinction_mosaicity 100.0
#  _extinction_radius    50.0
#  _extinction_model     gauss
#  _diffrn_orient_matrix_UB_11 6.59783
#  _diffrn_orient_matrix_UB_12 -6.99807
#  _diffrn_orient_matrix_UB_13 3.3663
#  _diffrn_orient_matrix_UB_21 2.18396
#  _diffrn_orient_matrix_UB_22 -2.60871
#  _diffrn_orient_matrix_UB_23 -9.5302
#  _diffrn_orient_matrix_UB_31 7.4657
#  _diffrn_orient_matrix_UB_32 6.94702
#  _diffrn_orient_matrix_UB_33 -0.18685
#  _phase_label  Fe3O4
#  loop_
#  _diffrn_refln_index_h
#  _diffrn_refln_index_k
#  _diffrn_refln_index_l
#  _diffrn_refln_fr
#  _diffrn_refln_fr_sigma
#  0 0 8 0.64545 0.01329
#  2 0 6 1.75682 0.04540
#  0 2 6 1.67974 0.03711
# """
# obj = RhoChi.from_cif(s_cont)
# print(obj.diffrn_mono.diffrn_orient_matrix.cell)
# for var_name in obj.get_variable_names():
#     print(var_name)
#     obj.set_variable_by_name(var_name, 4)
# obj.form_object()
# print(obj.crystal_fe3o4)
