#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

# Django and native Python packages
import warnings

# 3rd party packages
import numpy as np

# Project imports
from groundhog.general.validation import Validator


VERTICALCAPACITY_UNDRAINED_API = {
    'effective_length': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'effective_width': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'su_base': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'su_increase': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'su_above_base': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'base_depth': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'skirted': {'type': 'bool', },
    'base_sigma_v_eff': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'roughness': {'type': 'float', 'min_value': 0.0, 'max_value': 1.0},
    'horizontal_load': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'foundation_inclination': {'type': 'float', 'min_value': -90.0, 'max_value': 90.0},
    'ground_surface_inclination': {'type': 'float', 'min_value': -90.0, 'max_value': 90.0},
    'bearing_capacity_factor': {'type': 'float', 'min_value': 3.0, 'max_value': 12.0},
    'factor_f_override': {'type': 'float', 'min_value': 0.0, 'max_value': 2.0}
}

VERTICALCAPACITY_UNDRAINED_API_ERRORRETURN = {
    'vertical_capacity [kN]': np.nan,
    'Su2 [kPa]': np.nan,
    'K_c [-]': np.nan,
    's_c [-]': np.nan,
    'd_c [-]': np.nan,
    'i_c [-]': np.nan,
    'b_c [-]': np.nan,
    'g_c [-]': np.nan,
    'F [-]': np.nan,
}

@Validator(VERTICALCAPACITY_UNDRAINED_API, VERTICALCAPACITY_UNDRAINED_API_ERRORRETURN)
def verticalcapacity_undrained_api(effective_length, effective_width, su_base, su_increase=0.0, su_above_base=np.nan,
                                   base_depth=0.0, skirted=True, base_sigma_v_eff=0.0, roughness=0.67, horizontal_load=0.0, foundation_inclination=0.0,
                                   ground_surface_inclination=0.0, bearing_capacity_factor=5.14,
                                   factor_f_override=np.nan, **kwargs):
    """
    Calculates the vertical capacity for a shallow foundation in clay with constant or linearly increasing undrained shear strength according to API RP 2GEO.

    The correction factor consists of a shape factor, a depth factor and three inclination factors. In the case of linearly increasing shear strenght, an additional factor F is used which can either be calculated from the foundation roughness (default) or specified directly.

    NOTE:  The relevancy of using the depth factor (:math:`d_c`) should be evaluated in each case. If the installation procedure and/or other foundation aspects, such as scour, do not allow for the required mobilization of shear stresses in the soil above foundation base level, it is recommended that (:math:`d_c`) = 0. In particular, it is recommended that (:math:`d_c`) = 0 if the horizontal load leads to mobilization of significant passive earth pressure between seafloor and foundation base level.

    NOTE: (:math:`H^{\prime}`) in the equation for inclination factor refers to the load applied to the effective area component of the base only. This corresponds to the total lateral load applied to the foundation minus any soil resistance acting on the foundation above skirt tip level as outlined in A.7.2.1, and minus any lateral resistance that may be carried by shearing at skirt tip level outside the effective area. This value is an input to the function.

    NOTE: For embedded foundations, the eccentricity is affected by the load inclination and increases with embedment. The modified eccentricity is found by calculating the intersection between the loading direction and the base depth level.

    NOTE: For skirted foundations, a separate assessment is required to check whether the skirt spacing is small enough to rely on the undrained shear strenght at skirt tip level.

    NOTE: In the assessment for non-skirted, base embedded foundation, the overburden pressure needs to be included in the vertical capacity assessment

    :param effective_length: Effective length of the foundation (:math:`L^{\\prime}`) [:math:`m`]  - Suggested range: 0.0<=effective_length
    :param effective_width: Minimum effective lateral dimension (:math:`B^{\\prime}`) [:math:`m`]  - Suggested range: 0.0<=effective_width
    :param su_base: Undrained shear strength at foundation base level (:math:`S_{uo}`) [:math:`kPa`]  - Suggested range: 0.0<=su_base
    :param su_increase: Linear increase in undrained shear strength (:math:`\\kappa`) [:math:`kPa/m`] (optional, default=0.0) - Suggested range: 0.0<=su_increase
    :param su_above_base: Average undrained shear strength above base level (:math:`s_{u,ave}`) [:math:`kPa`] (optional, default=np.nan) - Suggested range: 0.0<=su_above_base
    :param base_depth: Depth to the base of the foundation (:math:`D`) [:math:`m`] (optional, default=0.0) - Suggested range: 0.0<=base_depth
    :param skirted: Determines whether a foundation is skirted or base-embedded without skirts (optional, default=True)
    :param base_sigma_v_eff: Vertical effective stress at base level. Only used for non-skirted base-embedded foundations (:math:`\\sigma_{vo}^{\\prime}`) [:math:`kPa`] (optional, default=0.0)
    :param roughness: Value for roughness (0.0 for fully smooth, 1.0 for fully rough) (:math:`-`) [:math:`-`] (optional, default=0.67) - Suggested range: 0.0<=roughness<=1.0
    :param horizontal_load: Horizontal load acting on effective area of foundation (:math:`H^{\\prime}`) [:math:`kN`] (optional, default=0.0) - Suggested range: 0.0<=horizontal_load
    :param foundation_inclination: Foundation inclination as defined in figure (:math:`\\nu`) [:math:`deg`] (optional, default=0.0) - Suggested range: -90.0<=foundation_inclination<=90.0
    :param ground_surface_inclination: Ground surface inclination as defined in figure (:math:`\\beta`) [:math:`deg`] (optional, default=0.0) - Suggested range: -90.0<=ground_surface_inclination<=90.0
    :param bearing_capacity_factor: Bearing capacity factor (:math:`N_c`) [:math:`-`] (optional, default=5.14) - Suggested range: 3.0<=bearing_capacity_factor<=12.0
    :param factor_f_override: Direct specification of the factor F (:math:`F`) [:math:`-`] (optional, default=np.nan) - Suggested range: 0.0<=factor_f_override<=2.0

    .. math::
        Q_d = (s_u \\cdot N_c \\cdot K_c) \\cdot A^{\\prime} + \\sigma_{vo}^{\\prime} \\quad \\text{ (constant)}

        Q_d = F \\cdot \\left( s_{uo} \\cdot N_c + \\frac{\\kappa \\cdot B^{\\prime}}{4} \\right) \\cdot K_c \\cdot A^{\\prime}  + \\sigma_{vo}^{\\prime} \\quad \\text{ (linearly increasing) }

        \\text{Exclude the }  \\sigma_{vo}^{\\prime} \\text{ term for skirted foundations}

        K_c = 1 + s_c + d_c  - i_c - b_c - g_c

        \\text{Correction factors constant undrained shear strength}

        s_c = 0.18 \\cdot (1 - 2 \\cdot i_c) \\cdot (B^{\\prime} / L^{\\prime})

        d_c = 0.3 \\cdot \\arctan ( D / B^{\\prime})

        i_c = 0.5 - 0.5 \\cdot [1 - H^{\\prime} / (A^{\\prime} \\cdot s_u)]^{0.5}

        b_c = 2 \\cdot \\nu / (\\pi + 2) \\approx 0.4 \\cdot \\nu

        g_c = 2 \\cdot \\beta / (\\pi + 2) \\approx 0.4 \\cdot \\beta

        \\text{Correction factors linearly increasing undrained shear strength}

        F \\approx a + b \\cdot x - ((c + b \\cdot x)^2 + d^2)^{0.5}

        x = \\frac{\\kappa \\cdot B^{\\prime}}{s_{uo}}

        s_c = s_{cv} (1 - 2 \\cdot i_c) (B^{\\prime} / L^{\\prime})

        d_c = 0.3 \\cdot (s_{u,ave} / s_{u,2}) \\cdot \\arctan( D / B^{\\prime})

        s_{u,2} = F \\cdot (N_c \\cdot s_{uo} + \\kappa \\cdot B^{\\prime} / 4) / N_c

        i_c = 0.5 - 0.5 \\cdot [1 -H^{\\prime}/(A^{\\prime} \\cdot s_u)]^{0.5}

        b_c = 2 \\cdot \\nu / (\\pi + 2) \\approx 0.4 \\cdot \\nu

        g_c = 2 \\cdot \\beta / (\\pi + 2) \\approx 0.4 \\cdot \\beta

        \\text{Correction for horizontal load}

        H^{\\prime} = H_{total} - H_{d,outside} / \\gamma_{sliding} - \\Delta H / \\gamma_{sliding}

    :returns:   Vertical capacity (:math:`Q_d`) [:math:`kN`], Combined correction factor (:math:`K_c`) [:math:`-`], Shape factor (:math:`s_c`) [:math:`-`], Depth factor (:math:`d_c`) [:math:`-`], Load inclination factor (:math:`i_c`) [:math:`-`], Foundation inclination factor (:math:`b_c`) [:math:`-`], Ground inclination factor (:math:`g_c`) [:math:`-`], Correction factor for shear strength increase (:math:`F`) [:math:`-`]

    :rtype: Python dictionary with keys ['vertical_capacity [kN]','K_c [-]','s_c [-]','d_c [-]','i_c [-]','b_c [-]','g_c [-]','F [-]']

    .. figure:: images/api_correction_factor_undrained_linear.png
        :figwidth: 500
        :width: 400
        :align: center

        API correction factors for linear shear strength increase

    .. figure:: images/api_inclination_factors.png
        :figwidth: 500
        :width: 400
        :align: center

        API inclination factor definition

    Reference - API RP 2GEO, 2011. API RP 2GEO Geotechnical and Foundation Design Considerations

    """
    if su_increase == 0.0:
        # Correction factors for constant su
        if horizontal_load > su_base * effective_width * effective_length:
            raise ValueError("Horizontal load exceeds horizontal capacity")
        i_c = 0.5 - 0.5 * max(0.0, 1.0 - horizontal_load / (su_base * effective_length * effective_width)) ** 0.5
        s_c = 0.18 * (1.0 - 2.0 * i_c) * (effective_width / effective_length)
        d_c = 0.3 * np.arctan(base_depth / effective_width)
        b_c = 2.0 * np.radians(foundation_inclination) / (np.pi + 2.0)
        g_c = 2.0 * np.radians(ground_surface_inclination) / (np.pi + 2.0)
        F_factor = np.nan
        su2 = np.nan
    else:
        # Correction factors for linearly increasing su
        dimensionless_increase = su_increase * effective_width / su_base
        if not np.math.isnan(factor_f_override):
            F_factor = factor_f_override
        else:
            if 0.0 <= dimensionless_increase <= 25.0:
                F_smooth = 1.372 + 0.07 * dimensionless_increase - \
                           np.sqrt(((-0.128 + 0.07 * dimensionless_increase) ** 2.0) + ((0.342) ** 2.0))
                F_rough = 2.56 + 0.457 * dimensionless_increase - \
                           np.sqrt(((0.713 + 0.457 * dimensionless_increase) ** 2.0) + ((1.38) ** 2.0))
            else:
                warnings.warn("kB/Suo outside interpolation range, value for kB/Suo=25 is used", Warning)
                F_smooth = 1.372 + 0.07 * 10.0 - \
                           np.sqrt(((-0.128 + 0.07 * 10.0) ** 2.0) + ((0.342) ** 2.0))
                F_rough = 2.56 + 0.457 * 10.0 - \
                           np.sqrt(((0.713 + 0.457 * 10.0) ** 2.0) + ((1.38) ** 2.0))

            F_factor = np.interp(roughness, [0.0, 1.0], [F_smooth, F_rough])

        if 0.0 <= dimensionless_increase <= 10.0:
            s_cv = 0.18 - 0.155 * ((dimensionless_increase)**0.5) + 0.021 * dimensionless_increase
        else:
            warnings.warn("kB/Suo outside interpolation range, value for kB/Suo=10 is used", Warning)
            s_cv = 0.18 - 0.155 * ((10.0)**0.5) + 0.021 * 10.0
        i_c = 0.5 - 0.5 * (1.0 - horizontal_load / (su_base * effective_length * effective_width)) ** 0.5
        s_c = s_cv * (1.0 - 2.0 * i_c) * (effective_width / effective_length)
        su2 = F_factor * (bearing_capacity_factor * su_base + 0.25 * su_increase * effective_width) / bearing_capacity_factor
        if np.math.isnan(su_above_base):
            raise ValueError("Undrained shear strength above base (su_above_base) must be specified for linearly increasing undrained shear strength cases")
        d_c = 0.3 * (su_above_base / su2) * np.arctan(base_depth / effective_width)
        b_c = 2.0 * np.radians(foundation_inclination) / (np.pi + 2.0)
        g_c = 2.0 * np.radians(ground_surface_inclination) / (np.pi + 2.0)

    K_c = 1.0 + s_c + d_c - i_c - b_c - g_c

    if not skirted and base_sigma_v_eff == 0.0:
        warnings.warn("Vertical effective stress at base for base embedded foundation is zero. Specify base_sigma_v_eff"
                      " to take a non-zero value into account")

    if su_increase == 0.0:
        vertical_capacity = su_base * bearing_capacity_factor * K_c * effective_width * effective_length
        if not skirted:
            vertical_capacity += base_sigma_v_eff
    else:
        vertical_capacity = F_factor * (su_base * bearing_capacity_factor + \
                                        0.25 * su_increase * effective_width) * \
                            K_c * effective_length * effective_width
        if not skirted:
            vertical_capacity += base_sigma_v_eff

    return {
        'vertical_capacity [kN]': vertical_capacity,
        'Su2 [kPa]': su2,
        'K_c [-]': K_c,
        's_c [-]': s_c,
        'd_c [-]': d_c,
        'i_c [-]': i_c,
        'b_c [-]': b_c,
        'g_c [-]': g_c,
        'F [-]': F_factor,
    }


VERTICALCAPACITY_DRAINED_API = {
    'vertical_effective_stress': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'effective_friction_angle': {'type': 'float', 'min_value': 20.0, 'max_value': 50.0},
    'effective_unit_weight': {'type': 'float', 'min_value': 3.0, 'max_value': 12.0},
    'effective_length': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'effective_width': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'base_depth': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'skirted': {'type': 'bool', },
    'load_inclination': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'foundation_inclination': {'type': 'float', 'min_value': -90.0, 'max_value': 90.0},
    'ground_surface_inclination': {'type': 'float', 'min_value': -90.0, 'max_value': 90.0},
}

VERTICALCAPACITY_DRAINED_API_ERRORRETURN = {
    'vertical_capacity [kN]': np.nan,
    'N_q [-]': np.nan,
    'N_gamma [-]': np.nan,
    'K_q [-]': np.nan,
    'K_gamma [-]': np.nan,
    's_q [-]': np.nan,
    's_gamma [-]': np.nan,
    'd_q [-]': np.nan,
    'd_gamma [-]': np.nan,
    'i_q [-]': np.nan,
    'i_gamma [-]': np.nan,
    'b_q [-]': np.nan,
    'b_gamma [-]': np.nan,
    'g_q [-]': np.nan,
    'g_gamma [-]': np.nan
}

@Validator(VERTICALCAPACITY_DRAINED_API, VERTICALCAPACITY_DRAINED_API_ERRORRETURN)
def verticalcapacity_drained_api(vertical_effective_stress, effective_friction_angle, effective_unit_weight,
                                 effective_length, effective_width, base_depth=0.0, skirted=True, load_inclination=0.0,
                                 foundation_inclination=0.0, ground_surface_inclination=0.0,
                                 **kwargs):
    """
    Calculates the vertical capacity for a shallow foundation in sand with effective friction angle characterized from drained triaxial tests. For constructing an envelope, this value needs to be multiplied by the tangent of the inclination to obtain the H-coordinate of the envelope point.

    The correction factor consists of a shape factor, a depth factor and three inclination factors for both :math:`K_q` and :math:`K_gamma`.

    NOTE: :math:`H/Q` corresponds to the tangent of the load inclination. For constructing an envelope, load inclinations should be varied from 0.0 to 90.0

    NOTE:  The relevancy of using the depth factors should be evaluated in each case. If the installation procedure and/or other foundation aspects, such as scour, do not allow for the required mobilization of shear stresses in the soil above foundation base level, it is recommended that depth factors are set to zero. In particular, it is recommended that d = 0 if the horizontal load leads to mobilization of significant passive earth pressure between seafloor and foundation base level.

    NOTE: :math:`H` in the equation for inclination factor refers to the load applied to the effective area component of the base only. This corresponds to the total lateral load applied to the foundation minus any soil resistance acting on the foundation above skirt tip level as outlined in A.7.2.1, and minus any lateral resistance that may be carried by shearing at skirt tip level outside the effective area.

    NOTE: For embedded foundations, the eccentricity is affected by the load inclination and increases with embedment. The modified eccentricity is found by calculating the intersection between the loading direction and the base depth level.

    NOTE: For non-skirted, base embedded foundations, the contribution of overburden pressure needs to be taken into account. In the equations in the standard, (Nq - 1) needs to be replaced by Nq

    :param vertical_effective_stress: Vertical effect stress at depth corresponding to foundation base (:math:`p_o^{\\prime}`) [:math:`kPa`]  - Suggested range: 0.0<=vertical_effective_stress
    :param effective_friction_angle: Effective friction angle (for appropriate stress level at foundatoin base) (:math:`\\phi^{\\prime}`) [:math:`deg`]  - Suggested range: 20.0<=effective_friction_angle<=50.0
    :param effective_unit_weight: Effective unit weight at foundation base (:math:`\\gamma^{\\prime}`) [:math:`kN/m3`]  - Suggested range: 3.0<=effective_unit_weight<=12.0
    :param effective_length: Effective length of the footing (:math:`L^{\\prime}`) [:math:`m`]  - Suggested range: 0.0<=effective_length
    :param effective_width: Minimum effective lateral dimension (:math:`B^{\\prime}`) [:math:`m`]  - Suggested range: 0.0<=effective_width
    :param base_depth: Depth of the foundation base (:math:`D`) [:math:`m`] (optional, default=0.0) - Suggested range: 0.0<=base_depth
    :param skirted: Determines whether a foundation is skirted or base-embedded without skirts (optional, default=True)
    :param load_inclination: Inclination of the load taking into account horizontal load on effective area of base only (:math:`H^{\\prime}`) [:math:`deg`] (optional, default=0.0) - Suggested range: 0.0<=load_inclination
    :param foundation_inclination:  Foundation inclination as defined in figure (:math:`\\nu`) [:math:`deg`] (optional, default=0.0) - Suggested range: -90.0<=foundation_inclination<=90.0
    :param ground_surface_inclination: Ground surface inclination as defined in figure  (:math:`\\beta`) [:math:`deg`] (optional, default=0.0) - Suggested range: -90.0<=ground_surface_inclination<=90.0

    .. math::
        Q_d^{\\prime} = \\left [ p_o^{\\prime} (N_q - 1) K_q + 0.5 \\gamma^{\\prime} B^{\\prime} N_{\\gamma} K_{\\gamma} \\right ] A^{\\prime}

        \\text{Use }  N_q \\text{ instead of } (N_q - 1) \\text{ for non-skirted, base embedded foundations}

        N_q = \\exp \\left [ \\pi \\tan \\phi^{\\prime} \\right ] (\\tan^2 (45^{\\circ} + \\phi^{\\prime}/2))

        N_{\\gamma} = 1.5 \\left ( N_q - 1 \\right) \\tan \\phi^{\\prime}

        K_q = i_q \\cdot s_q \\cdot d_q \\cdot b_q \\cdot g_q

        K_{\\gamma} = i_{\\gamma} \\cdot s_{\\gamma} \\cdot d_{\\gamma} \\cdot b_{\\gamma} \\cdot g_{\\gamma}

        i_q = \\left [ 1 -0.5 (H/Q) \\right]^5

        i_{\\gamma} = \\left[ 1-0.7 (H/Q) \\right]^5

        s_q = 1+i_q ( B^{\\prime} / L^{\\prime} ) \\sin \\phi^{\\prime}

        s_{\\gamma} = 1 - 0.4 i_{\\gamma} ( B^{\\prime} / L^{\\prime} )

        d_q = 1 + 1.2 (D/B^{\\prime}) \\tan \\phi^{\\prime} (1 - \\sin \\phi^{\\prime})^2

        d_{\\gamma} = 1

        b_q = e^{-2 \\nu \\tan \\phi^{\\prime}}

        b_{\\gamma} = e^{-2.7 \\nu \\tan \\phi^{\\prime}}

        g_q = g_{\\gamma} = (1 - 0.5 \\tan \\beta)^5

    :returns:   Vertical capacity of the footing (:math:`Q_d`) [:math:`kN`], Bearing capacity factor for frictional resistance (:math:`N_q`) [:math:`-`], Bearing capacity factor for unit weight (:math:`N_{\\gamma}`) [:math:`-`], Combined correction factor for frictional resistance (:math:`K_q`) [:math:`-`], Combined correction factor for unit weight (:math:`K_{\\gamma}`) [:math:`-`], Shape factor frictional (:math:`s_q`) [:math:`-`], Shape factor unit weight (:math:`s_{\\gamma}`) [:math:`-`], Depth factor frictional (:math:`d_q`) [:math:`-`], Depth factor unit weight (:math:`d_{\\gamma}`) [:math:`-`], Inclination factor frictional (:math:`i_q`) [:math:`-`], Inclination factor unit weight (:math:`i_{\\gamma}`) [:math:`-`], Foundation inclination factor frictional (:math:`b_q`) [:math:`-`], Foundation inclination factor unit weight (:math:`b_{\\gamma}`) [:math:`-`], Soil surface inclination factor frictional (:math:`g_q`) [:math:`-`], Soil surface inclination factor unit weight (:math:`g_gamma`) [:math:`-`]

    :rtype: Python dictionary with keys ['vertical_capacity [kN]','N_q [-]','N_gamma [-]','K_q [-]','K_gamma [-]','s_q [-]','s_gamma [-]','d_q [-]','d_gamma [-]','i_q [-]','i_gamma [-]','b_q [-]','b_gamma [-]','g_q [-]','g_gamma [-]']


    Reference - API RP 2GEO, 2011. API RP 2GEO Geotechnical and Foundation Design Considerations

    """
    if load_inclination != 0.0:
        effective_width = effective_width - 2.0 * (np.tan(np.radians(load_inclination)) *  base_depth)

    i_q = (1.0 - 0.5 * np.tan(np.radians(load_inclination))) ** 5.0
    i_gamma = (1.0 - 0.7 * np.tan(np.radians(load_inclination))) ** 5.0
    s_q = 1.0 + i_q * (effective_width / effective_length) * np.sin(np.radians(effective_friction_angle))
    s_gamma = 1.0 - 0.4 * i_gamma * (effective_width / effective_length)
    d_q = 1.0 + 1.2 * (base_depth / effective_width) * np.tan(np.radians(effective_friction_angle)) * \
                ((1.0 - np.sin(np.radians(effective_friction_angle))) ** 2.0)
    d_gamma = 1.0
    b_q = np.exp(-2.0 * np.radians(foundation_inclination) * np.tan(np.radians(effective_friction_angle)))
    b_gamma = np.exp(-2.7 * np.radians(foundation_inclination) * np.tan(np.radians(effective_friction_angle)))
    g_q = (1.0 - 0.5 * np.tan(np.radians(ground_surface_inclination))) ** 5.0
    g_gamma = g_q

    K_q = i_q * s_q * d_q * b_q * g_q
    K_gamma = i_gamma * s_gamma * d_gamma * b_gamma * g_gamma

    N_q = (np.exp(np.pi * np.tan(np.radians(effective_friction_angle)))) * \
         ((np.tan(np.radians(45.0 + 0.5 * effective_friction_angle))) ** 2.0)
    N_gamma = 1.5 * (N_q - 1.0) * np.tan(np.radians(effective_friction_angle))
    if skirted:
        vertical_capacity = (vertical_effective_stress * (N_q - 1.0) * K_q + \
                             0.5 * effective_unit_weight * effective_width * N_gamma * K_gamma) * \
                            (effective_width * effective_length)
    else:
        vertical_capacity = (vertical_effective_stress * (N_q) * K_q + \
                             0.5 * effective_unit_weight * effective_width * N_gamma * K_gamma) * \
                            (effective_width * effective_length)
    return {
        'vertical_capacity [kN]': vertical_capacity,
        'N_q [-]': N_q,
        'N_gamma [-]': N_gamma,
        'K_q [-]': K_q,
        'K_gamma [-]': K_gamma,
        's_q [-]': s_q,
        's_gamma [-]': s_gamma,
        'd_q [-]': d_q,
        'd_gamma [-]': d_gamma,
        'i_q [-]': i_q,
        'i_gamma [-]': i_gamma,
        'b_q [-]': b_q,
        'b_gamma [-]': b_gamma,
        'g_q [-]': g_q,
        'g_gamma [-]': g_gamma,
    }

SLIDINGCAPACITY_UNDRAINED_API = {
    'su_base': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'foundation_area': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'su_above_base': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'embedded_section_area': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'soil_reaction_coefficient': {'type': 'float', 'min_value': 1.0, 'max_value': 6.0},
}

SLIDINGCAPACITY_UNDRAINED_API_ERRORRETURN = {
    'sliding_capacity [kN]': np.nan,
    'base_resistance [kN]': np.nan,
    'skirt_resistance [kN]': np.nan
}

@Validator(SLIDINGCAPACITY_UNDRAINED_API, SLIDINGCAPACITY_UNDRAINED_API_ERRORRETURN)
def slidingcapacity_undrained_api(su_base, foundation_area, su_above_base=0.0, embedded_section_area=0.0,
                                  soil_reaction_coefficient=4.0, **kwargs):
    """
    Calculates the undrained sliding capacity for a shallow foundation on clay, the contribution of skirt resistance is taken into account.

    :param su_base: Undrained shear strength at foundation base level (:math:`S_{uo}`) [:math:`kPa`]  - Suggested range: 0.0<=su_base
    :param foundation_area: Actual foundation area (not the effective area!) (:math:`A`) [:math:`m2`]  - Suggested range: 0.0<=foundation_area
    :param su_above_base: Average undrained shear strength along the skirt depth (:math:`S_{u,ave}`) [:math:`kPa`] (optional, default=0.0) - Suggested range: 0.0<=su_skirts
    :param embedded_section_area: Embedded vertical cross-sectional area of foundation (:math:`A_h`) [:math:`m2`] (optional, default=0.0) - Suggested range: 0.0<=embedded_section_area
    :param soil_reaction_coefficient: Soil reaction coefficient Kru. A value of 4 is recommended for full contact. If active soil resistance cannot be relied upon, the factor should be reduced to 2 (:math:`K_{ru}`) [:math:`-`] (optional, default=4.0) - Suggested range: 1.0<=soil_reaction_coefficient<=6.0

    .. math::
        H_d = S_{uo} \\cdot A

        \\Delta H = K_{ru} \\cdot (S_{u,ave}) \\cdot A_h

    :returns:   Sliding capacity (combined) (:math:`H_d + \\Delta H`) [:math:`kN`], Sliding resistance on the foundation base (:math:`H_d`) [:math:`kN`], Sliding resistance due to active and passive resistance of the skirts (:math:`\\Delta H`) [:math:`kN`]

    :rtype: Python dictionary with keys ['sliding_capacity [kN]','base_resistance [kN]','skirt_resistance [kN]']


    Reference - API RP 2GEO, 2011. API RP 2GEO Geotechnical and Foundation Design Considerations

    """
    base_resistance = su_base * foundation_area
    skirt_resistance = soil_reaction_coefficient * su_above_base * embedded_section_area
    sliding_capacity = base_resistance + skirt_resistance

    return {
        'sliding_capacity [kN]': sliding_capacity,
        'base_resistance [kN]': base_resistance,
        'skirt_resistance [kN]': skirt_resistance,
    }


SLIDINGCAPACITY_DRAINED_API = {
    'vertical_load': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'effective_friction_angle': {'type': 'float', 'min_value': 20.0, 'max_value': 50.0},
    'effective_unit_weight': {'type': 'float', 'min_value': 3.0, 'max_value': 12.0},
    'embedded_section_area': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'depth_to_base': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'reaction_factor_override': {'type': 'float', 'min_value': 0.0, 'max_value': None},
}

SLIDINGCAPACITY_DRAINED_API_ERRORRETURN = {
    'sliding_capacity [kN]': np.nan,
    'base_capacity [kN]': np.nan,
    'skirt_capacity [kN]': np.nan,
    'K_rd [-]': np.nan,
    'K_p [-]': np.nan
}

@Validator(SLIDINGCAPACITY_DRAINED_API, SLIDINGCAPACITY_DRAINED_API_ERRORRETURN)
def slidingcapacity_drained_api(vertical_load, effective_friction_angle, effective_unit_weight,
                                embedded_section_area=0.0, depth_to_base=0.0, reaction_factor_override=np.nan,
                                **kwargs):
    """
    Calculates the drained sliding capacity for a shallow foundation. The base resistance is increased for passive and active soil resistance derived from skirts.

    :param vertical_load: Actual vertical load during relevant loading condition (:math:`Q`) [:math:`kN`]  - Suggested range: 0.0<=vertical_load
    :param effective_friction_angle: Effective friction angle (for appropriate stress level at foundation base) (:math:`\\phi^{\\prime}`) [:math:`deg`]  - Suggested range: 20.0<=effective_friction_angle<=50.0
    :param effective_unit_weight: Effective unit weight (:math:`\\gamma^{\\prime}`) [:math:`kN/m3`]  - Suggested range: 3.0<=effective_unit_weight<=12.0
    :param embedded_section_area: Embedded vertical cross-sectional area of foundation (:math:`A_h`) [:math:`m2`] (optional, default=0.0) - Suggested range: 0.0<=embedded_section_area
    :param depth_to_base: Depth below seafloor to base level (:math:`D_b`) [:math:`m`] (optional, default=0.0) - Suggested range: 0.0<=depth_to_base
    :param reaction_factor_override: Drained horizontal reaction factor (:math:`K_{rd}`) [:math:`-`] (optional, default=np.nan) - Suggested range: 0.0<=reaction_factor_override

    .. math::
        H_d^{\\prime} = Q \\cdot \\tan \\phi^{\\prime}

        \\Delta H = 0.5 \\cdot K_{rd} \\cdot \\gamma^{\\prime} \\cdot D_b \\cdot A_h

        K_{rd} = K_p - (1/K_p)

        K_p = \\tan^2 (45^{\\circ} + 0.5 \\phi^{\\prime})

    :returns:   Combined sliding capacity due to base and skirt resistance (:math:`H_d + \\Delta H`) [:math:`kN`], Sliding resistance due to base friction (:math:`H_d`) [:math:`kN`], Sliding resistance due to active and passive resistance of the skirts (:math:`\\Delta H`) [:math:`kN`], Reaction factor (:math:`K_{rd}`) [:math:`-`], Passive resistance factor (:math:`K_p`) [:math:`-`]

    :rtype: Python dictionary with keys ['sliding_capacity [kN]','base_capacity [kN]','skirt_capacity [kN]','K_rd [-]','K_p [-]']


    Reference - API RP 2GEO, 2011. API RP 2GEO Geotechnical and Foundation Design Considerations
    
    """
    base_capacity = vertical_load * np.tan(np.radians(effective_friction_angle))
    K_p = (np.tan(np.radians(45.0 + 0.5 * effective_friction_angle))) ** 2.0
    if np.math.isnan(reaction_factor_override):
        K_rd = K_p - (1.0 / K_p)
    else:
        K_rd = reaction_factor_override
    skirt_capacity = 0.5 * K_rd * effective_unit_weight * depth_to_base * embedded_section_area
    sliding_capacity = base_capacity + skirt_capacity

    return {
        'sliding_capacity [kN]': sliding_capacity,
        'base_capacity [kN]': base_capacity,
        'skirt_capacity [kN]': skirt_capacity,
        'K_rd [-]': K_rd,
        'K_p [-]': K_p,
    }

EFFECTIVEAREA_RECTANGLE_API = {
    'length': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'width': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'vertical_load': {'type': 'float', 'min_value': 0.001, 'max_value': None},
    'moment_length': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'moment_width': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'eccentricity_length': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'eccentricity_width': {'type': 'float', 'min_value': 0.0, 'max_value': None},
}

EFFECTIVEAREA_RECTANGLE_API_ERRORRETURN = {
    'effective_area [m2]': np.nan,
    'effective_length [m]': np.nan,
    'effective_width [m]': np.nan,
    'eccentricity_length [m]': np.nan,
    'eccentricity_width [m]': np.nan
}

@Validator(EFFECTIVEAREA_RECTANGLE_API, EFFECTIVEAREA_RECTANGLE_API_ERRORRETURN)
def effectivearea_rectangle_api(length, width, vertical_load=np.nan, moment_length=np.nan, moment_width=np.nan,
                                eccentricity_length=np.nan, eccentricity_width=np.nan, **kwargs):
    """
    Calculates the reduced area of a rectangular footing to account for eccentricty of the load. Eccentricities can either be specified from a moment or defined directly.

    NOTE: In the assessment of eccentricity for shallow foundations on undrained soil, the V can include the weight of soil plug inside the skirts

    :param length: Longest foundation dimension (:math:`L`) [:math:`m`]  - Suggested range: 0.0<=length
    :param width: Shortest foundation dimension (:math:`B`) [:math:`m`]  - Suggested range: 0.0<=width
    :param vertical_load: Actual vertical load during relevant loading condition (:math:`Q`) [:math:`kN`] (optional, default=np.nan) - Suggested range: 0.001<=vertical_load
    :param moment_length: Overturning moment aligned with longest foundation dimension (:math:`M_1`) [:math:`kNm`] (optional, default=np.nan) - Suggested range: 0.0<=moment_length
    :param moment_width: Overturning moment aligned with shortest foundation dimension (:math:`M_2`) [:math:`kNm`] (optional, default=np.nan) - Suggested range: 0.0<=moment_width
    :param eccentricity_length: Eccentricity (direct specification) in the longest foundation direction (:math:`e_1`) [:math:`m`] (optional, default=np.nan) - Suggested range: 0.0<=eccentricity_length
    :param eccentricity_width: Eccentricity (direct specification) in the shortest foundation direction (:math:`e_2`) [:math:`m`] (optional, default=np.nan) - Suggested range: 0.0<=eccentricity_width

    .. math::
        e_1 = \\frac{M_1}{Q}

        e_2 = \\frac{M_2}{Q}

        L^{\\prime} = L - 2 \\cdot e_1

        B^{\\prime} = B - 2 \\cdot e_2

        A^{\\prime} = B^{\\prime} \\cdot L^{\\prime}


    :returns:   Effective area used to calculate mudmat capacity (:math:`A^{\\prime}`) [:math:`m2`], Effective length (:math:`L^{\\prime}`) [:math:`m`], Effective width (:math:`B^{\\prime}`) [:math:`m`], Eccentricity in the length direction (:math:`e_1`) [:math:`m`], Eccentricity in the width direction (:math:`e_2`) [:math:`m`]

    :rtype: Python dictionary with keys ['effective_area [m2]','effective_length [m]','effective_width [m]','eccentricity_length [m]','eccentricity_width [m]']

    .. figure:: images/api_reduced_area_rectangle.png
        :figwidth: 500
        :width: 400
        :align: center

        Effective area of a rectangular mudmat

    Reference - API RP 2GEO, 2011. API RP 2GEO Geotechnical and Foundation Design Considerations
    
    """
    if (not np.math.isnan(vertical_load)) and (not np.math.isnan(moment_length)) and \
            (not np.math.isnan(moment_width)) and np.math.isnan(eccentricity_length) and \
            np.math.isnan(eccentricity_width):
        e1 = moment_length / vertical_load
        e2 = moment_width / vertical_load
    elif (not np.math.isnan(eccentricity_length)) and (not np.math.isnan(eccentricity_width)) and \
            np.math.isnan(moment_length) and np.math.isnan(moment_width) and \
            np.math.isnan(vertical_load):
        e1 = eccentricity_length
        e2 = eccentricity_width
    else:
        raise ValueError("Eccentricity needs to be defined through moments or direct specification")
    effective_length = length - 2.0 * e1
    effective_width = width - 2.0 * e2
    effective_area = effective_length * effective_width

    return {
        'effective_area [m2]': effective_area,
        'effective_length [m]': effective_length,
        'effective_width [m]': effective_width,
        'eccentricity_length [m]': eccentricity_length,
        'eccentricity_width [m]': eccentricity_width,
    }

EFFECTIVEAREA_CIRCLE_API = {
    'foundation_radius': {'type': 'float', 'min_value': 0.01, 'max_value': None},
    'vertical_load': {'type': 'float', 'min_value': 0.01, 'max_value': None},
    'overturning_moment': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'eccentricity': {'type': 'float', 'min_value': 0.0, 'max_value': None},
}

EFFECTIVEAREA_CIRCLE_API_ERRORRETURN = {
    'effective_area [m2]': np.nan,
    'effective_length [m]': np.nan,
    'effective_width [m]': np.nan,
    's [m2]': np.nan,
    'eccentricity [m]': np.nan
}

@Validator(EFFECTIVEAREA_CIRCLE_API, EFFECTIVEAREA_CIRCLE_API_ERRORRETURN)
def effectivearea_circle_api(foundation_radius, vertical_load=np.nan, overturning_moment=np.nan, eccentricity=np.nan,
                             **kwargs):
    """
    Calculates the reduced area for a circular foundation to account for load eccentricity. Eccentricity can either be specified through an overturning moment or with direct specification of eccentricity.

    NOTE: In the assessment of eccentricity for shallow foundations on undrained soil, the V can include the weight of soil plug inside the skirts

    :param foundation_radius: Radius of the circular foundation (:math:`R`) [:math:`m`]  - Suggested range: 0.01<=foundation_radius
    :param vertical_load: Actual vertical load during relevant loading condition (:math:`Q`) [:math:`kN`] (optional, default=np.nan) - Suggested range: 0.01<=vertical_load
    :param overturning_moment: Overturning moment acting on the foundation (:math:`M`) [:math:`kNm`] (optional, default=np.nan) - Suggested range: 0.0<=overturning_moment
    :param eccentricity: Eccentricity (direct specification) (:math:`e_2`) [:math:`m`] (optional, default=np.nan) - Suggested range: 0.0<=eccentricity

    .. math::
        A^{\\prime} = 2s=B^{\\prime} L^{\\prime}

        L^{\\prime}=(2s \\sqrt{\\frac{R+e_2}{R-e_2}})^{1/2}

        B^{\\prime} = L^{\\prime} \\sqrt{\\frac{R-e_2}{R+e_2}}

        s = \\frac{\\pi R^2}{2}-[e_2 \\cdot (\\sqrt{R^2-e_2^2}) + R^2 \\arcsin(\\frac{e_2}{R})]

    :returns:   Effective area used for capacity calculation (:math:`A^{\\prime}`) [:math:`m2`], Effective length  (:math:`L^{\\prime}`) [:math:`m`], Effective width (:math:`B^{\\prime}`) [:math:`m`], Parameter s (:math:`s`) [:math:`m2`], Eccentricity used for the calculation (:math:`e_2`) [:math:`m`]

    :rtype: Python dictionary with keys ['effective_area [m2]','effectve length [m]','effective_width [m]','s [m2]','eccentricity [m]']

    .. figure:: images/api_reduced_area_circle.png
        :figwidth: 500
        :width: 400
        :align: center

        Reduced area for a circular foundation

    Reference - API RP 2GEO, 2011. API RP 2GEO Geotechnical and Foundation Design Considerations

    """
    if not np.math.isnan(overturning_moment) and (not np.math.isnan(vertical_load)) and \
            np.math.isnan(eccentricity):
        e2 = overturning_moment / vertical_load
    elif np.math.isnan(overturning_moment) and np.math.isnan(vertical_load) and \
            not np.math.isnan(eccentricity):
        e2 = eccentricity
    else:
        raise ValueError("Eccentricity needs to be specified either through moment or direct specification")
    s_ecc = 0.5 * np.pi * (foundation_radius ** 2.0) - \
            (e2 * (np.sqrt((foundation_radius ** 2.0) - (e2 ** 2.0))) + \
             (foundation_radius ** 2.0) * np.arcsin(e2 / foundation_radius))
    effective_length = (2.0 * s_ecc * np.sqrt((foundation_radius + e2) / (foundation_radius - e2))) ** 0.5
    effective_width = effective_length * np.sqrt((foundation_radius - e2) / (foundation_radius + e2))
    effective_area = effective_length * effective_width

    return {
        'effective_area [m2]': effective_area,
        'effective_length [m]': effective_length,
        'effective_width [m]': effective_width,
        's [m2]': s_ecc,
        'eccentricity [m]': eccentricity,
    }


ENVELOPE_DRAINED_API = {
    'vertical_effective_stress': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'effective_friction_angle_bearing': {'type': 'float', 'min_value': 20.0, 'max_value': 50.0},
    'effective_friction_angle_sliding': {'type': 'float', 'min_value': 15.0, 'max_value': 45.0},
    'effective_unit_weight': {'type': 'float', 'min_value': 3.0, 'max_value': 12.0},
    'effective_length': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'effective_width': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'length': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'width': {'type': 'float', 'min_value': 0.0, 'max_value': None}
}

ENVELOPE_DRAINED_API_ERRORRETURN = {
    'envelope_v [kN]': None,
    'envelope_h [kN]': None,
    'envelope_h_unchanged [kN]': None,
    'sliding_cuttoff [kN]': None
}

@Validator(ENVELOPE_DRAINED_API, ENVELOPE_DRAINED_API_ERRORRETURN)
def envelope_drained_api(vertical_effective_stress,
                         effective_friction_angle_bearing, effective_friction_angle_sliding, effective_unit_weight,
                         effective_length, effective_width,
                         length, width, **kwargs):
    """
    Calculates a drained failure envelope for shallow foundations according to API RP 2GEO. Note that optional keyword arguments can be specified as documented in the function verticalcapacity_drained_api.

    The envelope is calculated be varying the inclination of the load. Note that the equation for inclination factor will become negative for large inclinations. These values are filtered from the envelope.

    We derive the ultimate horizontal load in bearing from the equation for inclination but need to remember that this should only account for the horizontal capacity on the effective area.

    :param vertical_effective_stress: Vertical effect stress at depth corresponding to foundation base (:math:`p_o^{\\prime}`) [:math:`kPa`]  - Suggested range: 0.0<=vertical_effective_stress
    :param effective_friction_angle_bearing: Effective friction angle for bearing failure (for appropriate stress level at foundation base) (:math:`\\phi^{\\prime}`) [:math:`deg`]  - Suggested range: 20.0<=effective_friction_angle<=50.0
    :param effective_friction_angle_sliding: Effective friction angle for sliding failure (for appropriate stress level at foundatoin base) (:math:`\\delta^{\\prime}`) [:math:`deg`]  - Suggested range: 15.0<=effective_friction_angle<=45.0
    :param effective_unit_weight: Effective unit weight at foundation base (:math:`\\gamma^{\\prime}`) [:math:`kN/m3`]  - Suggested range: 3.0<=effective_unit_weight<=12.0
    :param effective_length: Effective length of the footing (:math:`L^{\\prime}`) [:math:`m`]  - Suggested range: 0.0<=effective_length
    :param effective_width: Minimum effective lateral dimension (:math:`B^{\\prime}`) [:math:`m`]  - Suggested range: 0.0<=effective_width
    :param length: True length of the footing (:math:`L`) [:math:`m`]  - Suggested range: 0.0<=length
    :param width: Minimum true lateral dimension (:math:`B`) [:math:`m`]  - Suggested range: 0.0<=width


    .. math::
        \\tan(\\text{inclination}) = \\frac{H_{eff}}{Q} = \\frac{H - H_{text{outside eff} - \\Delta H}{Q}

    :returns: Dictionary with the following keys:

        - 'envelope_v [kN]': Vertical capacities for the envelope (:math:`V`)  [:math:`kN`]
        - 'envelope_h [kN]': Horizontal capacities for the envelope (:math:`H`)  [:math:`kN`]
        - 'envelope_h_unchanged [kN]': Horizontal capacities for the envelope without accounting for effective area component only (:math:`H`)  [:math:`kN`]

    Reference - API RP 2GEO

    """

    #TODO: TAKE INTO ACCOUNT ECCENTRICITY FOR INCLINED LOAD + SKIRTS

    _inclinations = np.linspace(0.0, 90.0, 100)
    _envelope_v = np.array(list(map(lambda inclination: verticalcapacity_drained_api(
        vertical_effective_stress=vertical_effective_stress,
        effective_friction_angle=effective_friction_angle_bearing,
        effective_unit_weight=effective_unit_weight,
        effective_length=effective_length,
        effective_width=effective_width,
        load_inclination=inclination,
        **kwargs)['vertical_capacity [kN]'], _inclinations)))

    _inclinations = _inclinations[np.where(np.array(_envelope_v) > 0.0)]
    _envelope_v = _envelope_v[np.where(_envelope_v > 0.0)]

    _h_max = []
    _h_base = []
    _h_base_eff = []
    _h_base_outside_eff = []
    _h_skirt = []

    for v in _envelope_v:
        s = slidingcapacity_drained_api(
            vertical_load=v,
            effective_friction_angle=effective_friction_angle_sliding,
            effective_unit_weight=effective_unit_weight,
            **kwargs)
        _h_max.append(s['sliding_capacity [kN]'])
        base = s['base_capacity [kN]']
        base_eff = (base * effective_length * effective_width) / (length * width)
        base_outside_eff = base - base_eff
        _h_base.append(base)
        _h_base_eff.append(base_eff)
        _h_base_outside_eff.append(base_outside_eff)
        _h_skirt.append(s['skirt_capacity [kN]'])

    _envelope_h = np.array(_envelope_v) * np.tan(np.radians(_inclinations)) + np.array(_h_base_outside_eff) + \
        np.array(_h_skirt)
    _envelope_h_unchanged = np.array(_envelope_v) * np.tan(np.radians(_inclinations))


    return {
        'envelope_v [kN]': _envelope_v,
        'envelope_h [kN]': _envelope_h,
        'envelope_h_unchanged [kN]': _envelope_h_unchanged,
        'sliding_cuttoff [kN]': _h_max
    }


ENVELOPE_UNDRAINED_API = {
    'su_base': {'type': 'float', 'min_value': 0.0, 'max_value': 1000.0},
    'length': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'width': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'effective_length': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'effective_width': {'type': 'float', 'min_value': 0.0, 'max_value': None},
    'factor_sliding': {'type': 'float', 'min_value': 1.0, 'max_value': None},
    'factor_bearing': {'type': 'float', 'min_value': 1.0, 'max_value': None},
}

ENVELOPE_UNDRAINED_API_ERRORRETURN = {
    'envelope_v_unfactored [kN]': None,
    'envelope_h_unfactored [kN]': None,
    'envelope_v_factored [kN]': None,
    'envelope_h_factored [kN]': None,
    'envelope_v_uncorrected [kN]': None,
    'envelope_h_uncorrected [kN]': None,
    'sliding_capacity': None,
    'bearing_capacity': None,
}


@Validator(ENVELOPE_UNDRAINED_API, ENVELOPE_UNDRAINED_API_ERRORRETURN)
def envelope_undrained_api(
        su_base, length, width, effective_length, effective_width,
        factor_sliding=1.5, factor_bearing=2.0, **kwargs):
    """
    Calculates the undrained failure envelope according to API RP 2GEO. It is important to note than only the horizontal load acting on the effective area is taken into account for the envelope. To achieve this, the horizontal load points for the envelope are selected between 0 and the total horizontal capacity (including contributions from skirt resistance and total base area). Subsequently, a load inclination is calculated using only the effective area component of this horizontal load (subtract skirt resistance and horizontal capacity outside effective area). This inclination is used in the vertical capacity equation (through the inclination factor).

The envelope is calculated twice, first without correction for additional eccentricity at base level and next with a correction for this additional eccentricity. This two step approach is required since the load inclination is not known a priori.

To override the behaviour of the bearing and sliding capacity functions, use the optional keywords arguments defined in the function definitions of slidingcapacity_undrained_api and verticalcapacity_undrained_api

    :param su_base: Undrained shear strength at the foundation base (:math:`S_{uo}`) [:math:`kPa`] - Suggested range: 0.0 <= su_base <= 1000.0
    :param length: Total foundation length (:math:`L`) [:math:`m`] - Suggested range: length >= 0.0
    :param width: Total foundation with (:math:`B`) [:math:`m`] - Suggested range: width >= 0.0
    :param effective_length: Effective length (:math:`L^{\\prime}`) [:math:`m`] - Suggested range: effective_length >= 0.0
    :param effective_width: Effective width (:math:`B^{\\prime}`) [:math:`m`] - Suggested range: effective_width >= 0.0
    :param factor_sliding: Resistance factor for sliding, applied to the H component of the envelope (:math:`\\gamma_{sliding}`) [:math:`-`] - Suggested range: factor_sliding >= 1.0 (optional, default= 1.5)
    :param factor_bearing: Resistance factor for bearing failure, applied to the V component of the envelope (:math:`\\gamma_{bearing}`) [:math:`-`] - Suggested range: factor_bearing >= 1.0 (optional, default= 2.0)

    .. math::
        \\Delta e = D \\cdot \\tan \\theta

    :returns: Dictionary with the following keys:

        - 'envelope_v_unfactored [kN]': List with unfactored vertical capacities for the envelope (:math:`V`)  [:math:`kN`]
        - 'envelope_h_unfactored [kN]': List with unfactored horizontal capacities for the envelope (:math:`H`)  [:math:`kN`]
        - 'envelope_v_factored [kN]': List with factored vertical capacities for the envelope (:math:`V_{factored}`)  [:math:`kN`]
        - 'envelope_h_factored [kN]': List with factored horizontal capacities for the envelope (:math:`H_{factored}`)  [:math:`kN`]
        - 'envelope_v_uncorrected [kN]': List with vertical capacities for the envelope, not corrected for the additional eccentricity (:math:`V_{uncorrected}`)  [:math:`kN`]
        - 'envelope_h_uncorrected [kN]': List with horizontal capacities for the envelope, not corrected for the additional eccentricity (:math:`H_{uncorrected}`)  [:math:`kN`]
        - 'sliding_capacity': Dictionary with details for the sliding capacity calculation
        - 'bearing_capacity': Dictionary with details for the bearing capacity calculation for purely vertical load

    .. figure:: images/envelope_undrained_api_1.png
        :figwidth: 500.0
        :width: 450.0
        :align: center

        Undrained failure envelope

    Reference - API RP 2GEO, 2011. API RP 2GEO Geotechnical and Foundation Design Considerations

    """

    # Calculate the sliding capacity
    _sliding_capacity = slidingcapacity_undrained_api(
        su_base=su_base, foundation_area=length * width, **kwargs)
    # Select horizontal loads between zero and the total sliding capacity
    _horizontal_load = np.linspace(0.0, _sliding_capacity['sliding_capacity [kN]'], 100)
    # Calculate the sliding capacity outside effective area
    _h_outside = _sliding_capacity['base_resistance [kN]'] * \
        (1.0 - ((effective_length * effective_width) / (length * width)))
    # Subtract factored sliding capacity outside effective area and factored skirt resistance from horizontal load
    _horizontal_load_corrected = np.maximum(
        np.zeros(_horizontal_load.__len__()),
        _horizontal_load - \
        (_h_outside * factor_sliding) - \
        (_sliding_capacity['skirt_resistance [kN]'] * factor_sliding))
    # Calculate the vertical bearing capacity
    _bearing_capacity = verticalcapacity_undrained_api(
        effective_length=effective_length,
        effective_width=effective_width,
        su_base=su_base,
        **kwargs)
    # Calculate the envelope (first iteration)
    _envelope_v_raw = list(map(lambda h: verticalcapacity_undrained_api(
        effective_length=effective_length,
        effective_width=effective_width,
        su_base=su_base,
        horizontal_load=h,
        **kwargs)['vertical_capacity [kN]'], _horizontal_load_corrected))
    _envelope_v_uncorrected = np.append(_envelope_v_raw, [0.0, ])
    _envelope_h_uncorrected = np.append(_horizontal_load, [_horizontal_load.max(), ])
    try:
        # Correct the envelope for the additional eccentricity
        base_depth = kwargs['base_depth']
        if base_depth != 0.0:
            inclination = np.arctan(_envelope_h_uncorrected / _envelope_v_uncorrected)
            _effective_width_corrected = np.maximum(
                np.zeros(inclination.__len__()),
                effective_width - (2.0 * base_depth * np.tan(inclination)))
            envelope_v_corrected_raw = list(map(lambda h, b_eff_corr: verticalcapacity_undrained_api(
                effective_length=effective_length,
                effective_width=b_eff_corr,
                su_base=su_base,
                horizontal_load=h,
                **kwargs)['vertical_capacity [kN]'],
                                                _horizontal_load_corrected,
                                                _effective_width_corrected))
            _envelope_v_unfactored = np.append(envelope_v_corrected_raw, [0.0,])
        else:
            _envelope_v_unfactored = _envelope_v_uncorrected
    except:
        warnings.warn("Base depth not defined, assuming surface foundation", Warning)
        _envelope_v_unfactored = _envelope_v_uncorrected
    finally:
        _envelope_h_unfactored = _envelope_h_uncorrected
        _envelope_v_factored = _envelope_v_unfactored / factor_bearing
        _envelope_h_factored = _envelope_h_unfactored / factor_sliding

    return {
        'envelope_v_unfactored [kN]': _envelope_v_unfactored,
        'envelope_h_unfactored [kN]': _envelope_h_unfactored,
        'envelope_v_factored [kN]': _envelope_v_factored,
        'envelope_h_factored [kN]': _envelope_h_factored,
        'envelope_v_uncorrected [kN]': _envelope_v_uncorrected,
        'envelope_h_uncorrected [kN]': _envelope_h_uncorrected,
        'sliding_capacity': _sliding_capacity,
        'bearing_capacity': _bearing_capacity,
    }


NQ_FRICTIONANGLE_SAND = {
    'friction_angle': {'type': 'float', 'min_value': 20.0, 'max_value': 50.0},
}

NQ_FRICTIONANGLE_SAND_ERRORRETURN = {
    'Nq [-]': np.nan,
}


@Validator(NQ_FRICTIONANGLE_SAND, NQ_FRICTIONANGLE_SAND_ERRORRETURN)
def nq_frictionangle_sand(
        friction_angle,
        **kwargs):
    """
    Calculate the bearing capacity factor Nq from the friction angle

    :param friction_angle: Peak effective friction angle (:math:`\\phi_p^{\\prime}`) [:math:`deg`] - Suggested range: 20.0 <= friction_angle <= 50.0

    .. math::
        N_q = e^{\\pi \\tan \\phi_p^{\\prime}} \\tan^2 \\left( 45^{\\circ} + \\frac{ \\phi_p^{\\prime}}{2} \\right)

    :returns: Dictionary with the following keys:

        - 'Nq [-]': Bearing capacity factor (:math:`N_q`)  [:math:`-`]

    Reference - Budhu (2011) Introduction to soil mechanics and foundations

    """

    _Nq = np.exp(np.pi * np.tan(np.radians(friction_angle))) * \
          ((np.tan(np.radians(45.0 + 0.5 * friction_angle))) ** 2.0)

    return {
        'Nq [-]': _Nq,
    }


NGAMMA_FRICTIONANGLE_VESIC = {
    'friction_angle': {'type': 'float', 'min_value': 20.0, 'max_value': 50.0},
}

NGAMMA_FRICTIONANGLE_VESIC_ERRORRETURN = {
    'Ngamma [-]': np.nan,
}


@Validator(NGAMMA_FRICTIONANGLE_VESIC, NGAMMA_FRICTIONANGLE_VESIC_ERRORRETURN)
def ngamma_frictionangle_vesic(
        friction_angle,
        **kwargs):
    """
    Calculates the bearing capacity factor Ngamma according to the equation proposed by Vesic (1973). Note that alternative formulations are available.

    :param friction_angle: Peak drained friction angle (:math:`\\phi_p^{\\prime}`) [:math:`deg`] - Suggested range: 20.0 <= friction_angle <= 50.0

    .. math::
        N_{\\gamma} = 2 (N_q + 1) \\tan \\phi_p^{\\prime}

    :returns: Dictionary with the following keys:

        - 'Ngamma [-]': Bearing capacity factor (:math:`N_{\\gamma}`)  [:math:`-`]

    Reference - Budhu (2011) Introduction to soil mechanics and foundations

    """

    _Ngamma = 2.0 * (nq_frictionangle_sand(friction_angle)['Nq [-]'] + 1.0) * np.tan(np.radians(friction_angle))

    return {
        'Ngamma [-]': _Ngamma,
    }


NGAMMA_FRICTIONANGLE_MEYERHOF = {
    'friction_angle': {'type': 'float', 'min_value': 20.0, 'max_value': 50.0},
    'frictionangle_multiplier': {'type': 'float', 'min_value': None, 'max_value': None},
}

NGAMMA_FRICTIONANGLE_MEYERHOF_ERRORRETURN = {
    'Ngamma [-]': np.nan,
}


@Validator(NGAMMA_FRICTIONANGLE_MEYERHOF, NGAMMA_FRICTIONANGLE_MEYERHOF_ERRORRETURN)
def ngamma_frictionangle_meyerhof(
        friction_angle,
        frictionangle_multiplier=1.4, **kwargs):
    """
    Calculates the bearing capacity factor Ngamma according to the equation proposed by Meyerhof (1976). This formulation is more conservative compared to the Vesic formulation.

    :param friction_angle: Peak drained friction angle (:math:`\\phi_p^{\\prime}`) [:math:`deg`] - Suggested range: 20.0 <= friction_angle <= 50.0
    :param frictionangle_multiplier: Multiplier on the friction angle (:math:`\\alpha_1`) [:math:`-`] (optional, default= 1.4)

    .. math::
        N_{\\gamma} = (N_q - 1) \\tan (1.4 \\phi_p^{\\prime})

    :returns: Dictionary with the following keys:

        - 'Ngamma [-]': Bearing capacity factor (:math:`N_{\\gamma}`)  [:math:`-`]

    Reference - Budhu (2011) Introduction to soil mechanics and foundations

    """

    _Ngamma = (nq_frictionangle_sand(friction_angle)['Nq [-]'] - 1.0) * np.tan(
        np.radians(frictionangle_multiplier * friction_angle))

    return {
        'Ngamma [-]': _Ngamma,
    }


NGAMMA_FRICTIONANGLE_DAVISBOOKER = {
    'friction_angle': {'type': 'float', 'min_value': 20.0, 'max_value': 50.0},
    'roughness_factor': {'type': 'float', 'min_value': 0.0, 'max_value': 1.0},
    'multiplier_smooth': {'type': 'float', 'min_value': None, 'max_value': None},
    'multiplier_rough': {'type': 'float', 'min_value': None, 'max_value': None},
    'multiplier_exp_smooth': {'type': 'float', 'min_value': None, 'max_value': None},
    'multiplier_exp_rough': {'type': 'float', 'min_value': None, 'max_value': None},
}

NGAMMA_FRICTIONANGLE_DAVISBOOKER_ERRORRETURN = {
    'Ngamma [-]': np.nan,
    'Ngamma_smooth [-]': np.nan,
    'Ngamma_rough [-]': np.nan,
}

@Validator(NGAMMA_FRICTIONANGLE_DAVISBOOKER, NGAMMA_FRICTIONANGLE_DAVISBOOKER_ERRORRETURN)
def ngamma_frictionangle_davisbooker(
        friction_angle, roughness_factor,
        multiplier_smooth=0.0663, multiplier_rough=0.1054, multiplier_exp_smooth=9.3, multiplier_exp_rough=9.6,
        **kwargs):
    """
    Calculates the bearing capacity factor Ngamma according to the equation proposed by Davis and Booker (1971). This formulation is based on a more refined plasticity method and takes the roughness into account. This method is preferred in principle.

    :param friction_angle: Peak drained friction angle (:math:`\\phi_p^{\\prime}`) [:math:`deg`] - Suggested range: 20.0 <= friction_angle <= 50.0
    :param roughness_factor: Footing roughness factor where 0 is fully smooth and 1 is fully rough (:math:`R_{inter}`) [:math:`-`] - Suggested range: 0.0 <= roughness_factor <= 1.0
    :param multiplier_smooth: Multiplier for smooth footings (:math:`\\alpha_1`) [:math:`-`] (optional, default= 0.0663)
    :param multiplier_rough: Multiplier for rough footings (:math:`\\alpha_2`) [:math:`-`] (optional, default= 0.1054)
    :param multiplier_exp_smooth: Multiplier on exponential term for smooth footings (:math:`\\alpha_3`) [:math:`-`] (optional, default= 9.3)
    :param multiplier_exp_rough: Multiplier on exponential term for roughfootings (:math:`\\alpha_4`) [:math:`-`] (optional, default= 9.6)

    .. math::
        N_{\\gamma} = \\begin{cases}
            0.1054 \\exp (9.6 \\phi_p^{\\prime})       & \\quad \\text{for rough footings}\\\\
            0.0663 \\exp(9.3 \\phi_p^{\\prime})  & \\quad \\text{for smooth footings}
          \\end{cases}

    :returns: Dictionary with the following keys:

        - 'Ngamma [-]': Bearing capacity factor (:math:`N_{\\gamma}`)  [:math:`-`]
        - 'Ngamma_smooth [-]': Bearing capacity factor for smooth footing (:math:`N_{\\gamma,smooth}`)  [:math:`-`]
        - 'Ngamma_rough [-]': Bearing capacity factor for rough footing (:math:`N_{\\gamma,rough}`)  [:math:`-`]

    Reference - Budhu (2011) Introduction to soil mechanics and foundations

    """
    _Ngamma_smooth = multiplier_smooth * np.exp(multiplier_exp_smooth * np.radians(friction_angle))
    _Ngamma_rough = multiplier_rough * np.exp(multiplier_exp_rough * np.radians(friction_angle))
    _Ngamma = np.interp(roughness_factor, [0.0, 1.0], [_Ngamma_smooth, _Ngamma_rough])

    return {
        'Ngamma [-]': _Ngamma,
        'Ngamma_smooth [-]': _Ngamma_smooth,
        'Ngamma_rough [-]': _Ngamma_rough,
    }

class APIMudmatCalculation(object):

    def __init__(self, title):
        self.title = title

    def set_rectangular_dimensions(self, length, width, eccentricity_length, eccentricity_width):
        """
        Sets dimensions for a rectangular foundation

        :param length:
        :param width:
        :param eccentricity_length:
        :param eccentricity_width:
        :return:
        """
        pass


class APIMudmatCalculationDrained(APIMudmatCalculation):

    pass


class APIMudmatCalculationUndrained(APIMudmatCalculation):
    pass