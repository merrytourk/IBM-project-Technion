
import numpy as np
from .Clifford import Clifford
from .basic_utils import BasicUtils




class PauliUtils(BasicUtils):
    """Class for util functions for the Pauli group."""

    def __init__(self, num_qubits=2, group_tables=None, elmnt=None,
                 gatelist=None, elmnt_key=None):
        """
        Args:
            num_qubits: number of qubits.
            group_table: table of Pauli objects.
            elmnt: a group element.
            elmnt_key: a unique index of a Pauli object.
            gatelist: a list of gates corresponding to a
                Pauli object.
        """

        self._num_qubits = num_qubits
        self._group_tables = group_tables
        self._elmnt = elmnt
        self._elmnt_key = elmnt_key
        self._gatelist = gatelist

    def num_qubits(self):
        """Return the number of qubits."""
        return self._num_qubits

    def group_tables(self):
        """Return the Pauli group tables."""
        return self._group_tables

    def elmnt(self):
        """Return a Pauli object."""
        return self._elmnt

    def elmnt_key(self):
        """Return a unique index of a Pauli object."""
        return self._elmnt_key

    def gatelist(self):
        """Return a list of gates corresponding to a Pauli object."""
        return self._gatelist

    # ----------------------------------------------------------------------------------------
    # Functions that convert to/from a Pauli object
    # ----------------------------------------------------------------------------------------
    def compose_gates(self, cliff, gatelist):
        """
        Add gates to a Pauli object from a list of gates.
        Args:
            cliff: A Clifford class object.
            gatelist: a list of gates.
        Returns:
            A Pauli class object.
        """

        for op in gatelist:
            split = op.split()
            q1 = int(split[1])
            if split[0] == 'x':
                cliff.x(q1)
            elif split[0] == 'y':
                cliff.y(q1)
            elif split[0] == 'z':
                cliff.z(q1)
            else:
                raise ValueError("Unknown gate type: ", op)

        self._gatelist = gatelist
        self._elmnt = cliff
        return cliff

    def Pauli_from_gates(self, num_qubits, gatelist):
        """
        Generates a Pauli object from a list of gates.
        Args:
            num_qubits: the number of qubits for the Pauli.
            gatelist: a list of gates.
        Returns:
            A num-qubit Pauli class object.
        """
        cliff = Clifford(num_qubits)
        new_cliff = self.compose_gates(cliff, gatelist)
        return new_cliff

    # --------------------------------------------------------
    # Add gates to Paulis
    # --------------------------------------------------------

    def pauli_gates(self, gatelist, q, pauli):
        """Adds a pauli gate on qubit q"""
        if pauli == 2:
            gatelist.append('x ' + str(q))
        elif pauli == 3:
            gatelist.append('y ' + str(q))
        elif pauli == 1:
            gatelist.append('z ' + str(q))

    # --------------------------------------------------------
    # Create a 1 or 2 Qubit Pauli based on a unique index
    # --------------------------------------------------------

    def Pauli1_gates(self, idx: int):
        """
        Make a single qubit Pauli gate.
        Args:
            idx: the index (mod 4) of a single qubit Pauli.
        Returns:
            A single qubit Pauli gate.
        """

        gatelist = []
        # Cannonical Ordering of Pauli 0,...,4
        cannonicalorder = idx % 4
        pauli = np.mod(cannonicalorder, 4)

        self.pauli_gates(gatelist, 0, pauli)

        return gatelist

    def Pauli2_gates(self, idx: int):
        """
        Make a 2-qubit Pauli gate.
        Args:
            idx: the index (mod 16) of a two-qubit Pauli.
        Returns:
            A 2-qubit Pauli gate.
        """

        gatelist = []
        cannon = idx % 16

        pauli = np.mod(cannon, 16)

        self.pauli_gates(gatelist, 0, np.mod(pauli, 4))
        self.pauli_gates(gatelist, 1, pauli // 4)

        return gatelist

    # --------------------------------------------------------
    # Create a 1 or 2 Qubit Pauli tables
    # --------------------------------------------------------
    def Pauli2_gates_table(self):
        """
        Generate a table of all 2-qubit Pauli gates.
        Args:
            None.
        Returns:
            A table of all 2-qubit Pauli gates.
        """
        pauli2 = {}
        for i in range(16):
            circ = self.Pauli2_gates(i)
            key = self.Pauli_from_gates(2, circ).index()
            pauli2[key] = circ
        return pauli2

    def Pauli1_gates_table(self):
        """
        Generate a table of all 1-qubit Pauli gates.
        Args:
            None.
        Returns:
            A table of all 1-qubit Pauli gates.
        """
        pauli1 = {}
        for i in range(4):
            circ = self.Pauli1_gates(i)
            key = self.Pauli_from_gates(1, circ).index()
            pauli1[key] = circ
        return pauli1

   
    def load_clifford_table(self, picklefile='cliffords2.pickle'):
        """
        Load pickled files of the tables of 1 and 2 qubit Clifford tables.
        Args:
            picklefile: pickle file name.
        Returns:
            A table of 1 and 2 qubit Clifford gates.
        """
        with open(picklefile, "rb") as pf:
            return pickle.load(pf)
        pf.close()

    def load_tables(self, num_qubits):
        """
        Returns the needed pauli tables
        Args:
            num_qubits: number of qubits for the required table
        Returns:
            A table of Pauli objects
        """

        # load the pauli tables, but only if we're using that particular
        # num_qubits
        if num_qubits == 1:
            # 1Q Cliffords, load table programmatically
            pauli_tables = self.Pauli1_gates_table()

        elif num_qubits == 2:
            # 2Q Cliffords, load table programmatically
            pauli_tables = self.Pauli2_gates_table()

           
        self._group_tables = pauli_tables
        return pauli_tables

    # --------------------------------------------------------
    # Main function that generates a random pauli gate
    # --------------------------------------------------------
    def random_gates(self, num_qubits):
        """
        Pick a random Pauli gate.
        Args:
            num_qubits: dimension of the Pauli.
        Returns:
            A 1 or 2 qubit Pauli gate.
        """

        if num_qubits == 1:
            paul_gatelist = self.Pauli1_gates(np.random.randint(0, 4))
        elif num_qubits == 2:
            paul_gatelist = self.Pauli2_gates(np.random.randint(0, 16))
        else:
            raise ValueError("The number of qubits should be only 1 or 2")

        self._gatelist = paul_gatelist
        return paul_gatelist

    # --------------------------------------------------------
    # Main function that calculates an inverse of a Pauli gate
    # --------------------------------------------------------
    def find_inverse_gates(self, num_qubits, gatelist):
        """
        Find the inverse of a Pauli gate.
        Args:
            num_qubits: the dimension of the Pauli.
            gatelist: a Pauli gate.
        Returns:
            An inverse Pauli gate.
        """

        if num_qubits in (1, 2):
            inv_gatelist = gatelist.copy()
            inv_gatelist.reverse()
            return inv_gatelist
        raise ValueError("The number of qubits should be only 1 or 2")

    def find_key(self, paul, num_qubits):
        """
        Find the Pauli index.
        Args:
            paul: a Pauli object.
            num_qubits: the dimension of the Pauli.
        Returns:
            Pauli index (an integer).
        """
        G_table = self.load_tables(num_qubits)
        assert paul.index() in G_table, \
            "inverse not found in lookup table!\n%s" % paul
        return paul.index()
