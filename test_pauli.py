#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Test Pauli functions:
- Generating Pauli tables on 1 and 2 qubits: pauli_utils.Pauli1_table
  and pauli_utils.Pauli2_table
- Generating a pseudo-random Pauli (using the tables):
  pauli_utils.random_gates
- Inverting a Pauli: pauli_utils.find_inverse_gates
"""
import numpy as np
import matplotlib.pyplot as plt
from IPython import display

import os, sys
HOME = "/home/jolea/anaconda3/git/qiskit-ignis/"
QISKIT_ROOT = HOME
root_dir = os.path.expanduser(QISKIT_ROOT)
sys.path = [os.path.expanduser(QISKIT_ROOT)] + sys.path

import unittest
import random
#import os
#import numpy as np
#sys.path.insert(1,"/home/jolea/anaconda3/git/qiskit-ignis/qiskit/")
# Import the pauli_utils functions
from qiskit1.ignis.verification.randomized_benchmarking \
    import PauliUtils as plutils


class TestPauli(unittest.TestCase):
    """
        Test Pauli functions
    """
    def setUp(self):
        """
            setUp and global parameters
        """
        self.number_of_tests = 20  # number of pseudo-random seeds
        self.max_nq = 2  # maximal number of qubits to check
        self.plutils = plutils()

    def test_tables(self):
        """
            test: generating the tables for 1 and 2 qubits
        """
        test_tables_content = []
        test_tables_content.append(
            "test: generating the pauli group table for 1 qubit:\n")
        pauli1 = self.plutils.Pauli1_gates_table()
        test_tables_content.append(str(len(pauli1)) + '\n')
        test_tables_content.append(str(sorted(pauli1.values())) + '\n')
        test_tables_content.append(
            "-------------------------------------------------------\n")

        test_tables_content.append(
            "test: generating the pauli group table for 2 qubits:\n")
        pauli2 = self.plutils.Pauli2_gates_table()
        test_tables_content.append(str(len(pauli2)) + '\n')
        test_tables_content.append(str(sorted(pauli2.values())) + '\n')
         
        expected_file_path = os.path.join(
            os.path.dirname(__file__),
            'test_pauli_tables_expected.txt')
        with open(expected_file_path, 'r') as fd:
            expected_file_content = fd.readlines()
        self.assertEqual(expected_file_content, test_tables_content,
                         "Error: tables on 1 and 2 qubits are not the same")
        
    def test_random_and_inverse(self):
        """
            test: generating a pseudo-random pauli using tables
            and computing its inverse
        """
        pauli_tables = [[]]*self.max_nq
        pauli_tables[0] = self.plutils.Pauli1_gates_table()
        pauli_tables[1] = self.plutils.Pauli2_gates_table()
        test_random_file_content = []
        # test: generating a pseudo-random pauli using tables -
        # 1&2 qubits and computing its inverse
        for nq in range(1, 1+self.max_nq):
            for i in range(0, self.number_of_tests):
                my_seed = i
                np.random.seed(my_seed)
                random.seed(my_seed)
                test_random_file_content.append(
                    "test: generating a pseudo-random pauli using the "
                    "tables - %d qubit - seed=%d:\n" % (nq, my_seed))
                pauli_nq = self.plutils.random_gates(nq)
                test_random_file_content.append(str(pauli_nq) + '\n')
                test_random_file_content.append(
                    "test: inverting a pseudo-random pauli using the "
                    "tables - %d qubit - seed=%d:\n" % (nq, my_seed))
                inv_pauli_nq = self.plutils.find_inverse_gates(
                    nq, pauli_nq)
                test_random_file_content.append(str(inv_pauli_nq) + '\n')
                test_random_file_content.append(
                    "-----------------------------------------------------"
                    "--\n")
      
        expected_file_path = os.path.join(
            os.path.dirname(__file__),
            'test_pauli_random_expected.txt')
        with open(expected_file_path, 'r') as fd:
            expected_file_content = fd.readlines()
        self.assertEqual(expected_file_content, test_random_file_content,
                         "Error: random and/or inverse pauli are not "
                         "the same")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
