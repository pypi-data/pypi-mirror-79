#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

# Native Python packages
import unittest
import os

# 3rd party packages
import pandas as pd
import numpy as np

# Project imports
from groundhog.general import soilprofile as sp


class Test_SoilProfile(unittest.TestCase):

    def setUp(self):
        self.profile = sp.SoilProfile(
            {
                'Depth from [m]': [0, 1, 5, 10],
                'Depth to [m]': [1, 5, 10, 20],
                'Soil type': ['SAND', 'SILT', 'CLAY', 'SAND']
            }
        )

    def test_wrong_layering(self):
        self.assertRaises(IOError, sp.SoilProfile, ({
            'Depth from [m]': [0, 1, 4, 10],
            'Depth to [m]': [1, 5, 10, 20],
            'Soil type': ['SAND', 'SILT', 'CLAY', 'SAND']
        }))

    def test_wrong_depthkey(self):
        self.assertRaises(IOError, sp.SoilProfile, ({
            'z from [m]': [0, 1, 4, 10],
            'z to [m]': [1, 5, 10, 20],
            'Soil type': ['SAND', 'SILT', 'CLAY', 'SAND']
        }))

    def test_wrong_linearvariation(self):
        # Test incomplete linear parameter variation
        self.assertRaises(IOError, sp.SoilProfile, ({
            'Depth from [m]': [0, 1, 5, 10],
            'Depth to [m]': [1, 5, 10, 20],
            'Soil type': ['SAND', 'SILT', 'CLAY', 'SAND'],
            'qc from [MPa]': [1, 3, 10, 40]
        }))
        # Check that complete parameter variation passes
        profile = sp.SoilProfile({
            'Depth from [m]': [0, 1, 5, 10],
            'Depth to [m]': [1, 5, 10, 20],
            'Soil type': ['SAND', 'SILT', 'CLAY', 'SAND'],
            'qc from [MPa]': [1, 3, 10, 40],
            'qc to [MPa]': [1, 3, 10, 40]
        })

    def test_profile_creation(self):
        self.assertEqual(self.profile.max_depth, 20)
        self.assertEqual(self.profile.min_depth, 0)
        self.assertEqual(self.profile.layer_transitions()[0], 1)
        self.assertEqual(self.profile.layer_transitions(include_top=True)[0], 0)

    def test_soilparameter_retrieval(self):
        profile = sp.SoilProfile({
            'Depth from [m]': [0, 1, 5, 10],
            'Depth to [m]': [1, 5, 10, 20],
            'Soil type': ['SAND', 'SILT', 'CLAY', 'SAND'],
            'Dr [%]': [40, 60, np.nan, 80],
            'qc from [MPa]': [1, 3, 10, 40],
            'qc to [MPa]': [1, 3, 10, 40]
        })
        self.assertIn('qc [MPa]',profile.soil_parameters())
        self.assertIn('Soil type',profile.soil_parameters())
        self.assertIn('qc from [MPa]',profile.soil_parameters(condense_linear=False))
        self.assertIn('qc [MPa]', profile.numerical_soil_parameters())
        self.assertNotIn('Soil type', profile.numerical_soil_parameters())
        self.assertIn('qc from [MPa]', profile.numerical_soil_parameters(condense_linear=False))
        self.assertNotIn('Soil type', profile.numerical_soil_parameters(condense_linear=False))
        self.assertNotIn('qc from [MPa]', profile.string_soil_parameters())
        self.assertIn('Soil type', profile.string_soil_parameters())
        self.assertTrue(profile.check_linear_variation('qc [MPa]'))
        self.assertFalse(profile.check_linear_variation('Dr [%]'))

    def test_transition_insert(self):
        self.profile.insert_layer_transition(depth=2.5)
        self.assertEqual(self.profile.loc[1, "Depth to [m]"], 2.5)
        self.profile.insert_layer_transition(depth=2)
        self.assertEqual(self.profile.loc[1, "Depth to [m]"], 2)

    def test_sign_conversion(self):
        self.profile.convert_depth_sign()
        self.assertEqual(self.profile.loc[1, 'Depth to [m]'], -5)
        self.profile.convert_depth_sign()
        self.assertEqual(self.profile.loc[1, 'Depth to [m]'], 5)

    def test_depth_shift(self):
        self.profile.shift_depths(offset=3)
        self.assertEqual(self.profile.loc[1, 'Depth to [m]'], 8)
        self.profile.shift_depths(offset=-3)
        self.assertEqual(self.profile.loc[1, 'Depth to [m]'], 5)

    def test_soilparameter_series(self):
        profile = sp.SoilProfile({
            'Depth from [m]': [0, 1, 5, 10],
            'Depth to [m]': [1, 5, 10, 20],
            'Soil type': ['SAND', 'SILT', 'CLAY', 'SAND'],
            'Dr [%]': [40, 60, np.nan, 80],
            'qc from [MPa]': [1, 3, 10, 40],
            'qc to [MPa]': [2, 3, 20, 50]
        })
        self.assertEqual(
            profile.soilparameter_series("qc [MPa]")[1][2], 3)
        self.assertEqual(
            profile.soilparameter_series("Dr [%]")[1][3], 60)

    def test_parameter_mapping(self):
        profile = sp.SoilProfile({
            'Depth from [m]': [0, 1, 5, 10],
            'Depth to [m]': [1, 5, 10, 20],
            'Soil type': ['SAND', 'SILT', 'CLAY', 'SAND'],
            'Relative density': ['Loose', 'Medium dense', None, 'Dense'],
            'Dr [%]': [40, 60, np.nan, 80],
            'qc from [MPa]': [1, 3, 10, 40],
            'qc to [MPa]': [2, 3, 20, 50]
        })
        mapped_df = profile.map_soilprofile(np.linspace(0, 20, 21))
        self.assertEqual(mapped_df.loc[3, 'Soil type'], 'SILT')
        self.assertRaises(ValueError, profile.map_soilprofile, (np.linspace(-1, 20, 22),))
        self.assertEqual(mapped_df.loc[15, 'qc [MPa]'], 45)

    def test_profile_selection_constant(self):
        self.profile.selection_soilparameter(
            parameter="Su [kPa]",
            depths=[6, 7, 8, 9],
            values=[10, 11, 12, 13]
        )
        self.assertEqual(self.profile.loc[2, "Su [kPa]"], 11.5)
        self.profile.selection_soilparameter(
            parameter="Dr [%]",
            depths=[6, 7, 8, 9],
            values=[10, 11, 12, 13],
            rule="min"
        )
        self.assertEqual(self.profile.loc[2, "Dr [%]"], 10)
        self.profile.selection_soilparameter(
            parameter="gamma [kN/m3]",
            depths=[6, 7, 8, 9],
            values=[10, 11, 12, 13],
            rule="max"
        )
        self.assertEqual(self.profile.loc[2, "gamma [kN/m3]"], 13)

    def test_profile_selection_linear(self):
        self.profile.selection_soilparameter(
            parameter="Su [kPa]",
            depths=[6, 7, 8, 9],
            values=[10, 11, 12, 13],
            linearvariation=True
        )
        self.assertAlmostEqual(self.profile.loc[2, "Su from [kPa]"], 9, 4)
        self.assertAlmostEqual(self.profile.loc[2, "Su to [kPa]"], 14, 4)
        # TODO: Check linear variation with min and max rule

    def test_merge_layers_top(self):
        self.profile.merge_layers(layer_ids=(1, 2))
        self.assertEqual(self.profile.loc[1, "Depth from [m]"], 1)
        self.assertEqual(self.profile.loc[1, "Depth to [m]"], 10)
        self.assertEqual(self.profile.loc[1, "Soil type"], "SILT")

    def test_merge_layers_bottom(self):
        self.profile.merge_layers(layer_ids=(1, 2), keep='bottom')
        self.assertEqual(self.profile.loc[1, "Depth from [m]"], 1)
        self.assertEqual(self.profile.loc[1, "Depth to [m]"], 10)
        self.assertEqual(self.profile.loc[1, "Soil type"], "CLAY")

    def test_remove_parameter(self):
        profile = sp.SoilProfile({
            'Depth from [m]': [0, 1, 5, 10],
            'Depth to [m]': [1, 5, 10, 20],
            'Soil type': ['SAND', 'SILT', 'CLAY', 'SAND'],
            'Relative density': ['Loose', 'Medium dense', None, 'Dense'],
            'Dr [%]': [40, 60, np.nan, 80],
            'qc from [MPa]': [1, 3, 10, 40],
            'qc to [MPa]': [2, 3, 20, 50]
        })
        profile.remove_parameter('qc [MPa]')
        def test_func():
            return profile.loc[0, "qc from [MPa]"]
        self.assertRaises(KeyError, test_func)
        profile.remove_parameter('Dr [%]')
        def test_func_2():
            return profile.loc[0, "Dr [%]"]

        self.assertRaises(KeyError, test_func_2)

    def test_cut_profile(self):
        profile = sp.SoilProfile({
            'Depth from [m]': [0, 1, 5, 10],
            'Depth to [m]': [1, 5, 10, 20],
            'Soil type': ['SAND', 'SILT', 'CLAY', 'SAND'],
            'Relative density': ['Loose', 'Medium dense', None, 'Dense'],
            'Dr [%]': [40, 60, np.nan, 80],
            'qc from [MPa]': [1, 3, 10, 40],
            'qc to [MPa]': [2, 4, 20, 50]
        })
        pf = profile.cut_profile(top_depth=1.5, bottom_depth=19)
        self.assertEqual(pf.min_depth, 1.5)
        self.assertEqual(pf.max_depth, 19)
        self.assertEqual(pf.loc[0, "qc from [MPa]"], 3.125)
        self.assertEqual(pf["qc to [MPa]"].iloc[-1], 49)

    def test_depth_integration(self):
        profile = sp.SoilProfile({
            'Depth from [m]': [0, 1, 5, 10],
            'Depth to [m]': [1, 5, 10, 20],
            'Soil type': ['SAND', 'SILT', 'CLAY', 'SAND'],
            'Relative density': ['Loose', 'Medium dense', None, 'Dense'],
            'Unit weight [kN/m3]': [9, 8, 7, 10],
            'Dr [%]': [40, 60, np.nan, 80],
            'qc from [MPa]': [1, 3, 10, 40],
            'qc to [MPa]': [2, 4, 20, 50]
        })
        profile.depth_integration(
            parameter='Unit weight [kN/m3]',
            outputparameter='Total vertical stress [kPa]'
        )
        self.assertEqual(profile['Total vertical stress from [kPa]'].iloc[0], 0)
        self.assertEqual(profile['Total vertical stress to [kPa]'].iloc[0], 9)
        self.assertEqual(profile['Total vertical stress to [kPa]'].iloc[1], 41)
