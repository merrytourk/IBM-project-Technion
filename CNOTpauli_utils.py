
import numpy as np
from .Clifford import Clifford
from .basic_utils import BasicUtils




class CNOTPauliUtils(BasicUtils):
    """Class for util functions for the CNOTPauli group."""

    def __init__(self, num_qubits=2, group_tables=None, elmnt=None,
                 gatelist=None, elmnt_key=None):
        """
        Args:
            num_qubits: number of qubits.
            group_table: table of CNOTPauli objects.
            elmnt: a group element.
            elmnt_key: a unique index of a CNOTPauli object.
            gatelist: a list of gates corresponding to a
                CNOTPauli object.
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
        """Return the CNOTPauli group tables."""
        return self._group_tables

    def elmnt(self):
        """Return a CNOTPauli object."""
        return self._elmnt

    def elmnt_key(self):
        """Return a unique index of a CNOTPauli object."""
        return self._elmnt_key

    def gatelist(self):
        """Return a list of gates corresponding to a CNOTPauli object."""
        return self._gatelist

    # ----------------------------------------------------------------------------------------
    # Functions that convert to/from a CNOTPauli object
    # ----------------------------------------------------------------------------------------
    def compose_gates(self, cliff, gatelist):
        """
        Add gates to a CNOTPauli object from a list of gates.
        Args:
            cliff: A Clifford class object.
            gatelist: a list of gates.
        Returns:
            A CNOTPauli class object.
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
            elif split[0] == 'cx':
                cliff.cx(q1, int(split[2]))
         
            else:
                raise ValueError("Unknown gate type: ", op)

        self._gatelist = gatelist
        self._elmnt = cliff
        return cliff

    def CNOTPauli_from_gates(self, num_qubits, gatelist):
        """
        Generates a CNOTPauli object from a list of gates.
        Args:
            num_qubits: the number of qubits for the CNOTPauli.
            gatelist: a list of gates.
        Returns:
            A num-qubit CNOTPauli class object.
        """
        cliff = Clifford(num_qubits)
        new_cliff = self.compose_gates(cliff, gatelist)
        return new_cliff

    # --------------------------------------------------------
    # Add gates to CNOTPaulis
    # --------------------------------------------------------

    def pauli_gates(self, gatelist, q, pauli):
        """Adds a pauli gate on qubit q"""
        if pauli == 2:
            gatelist.append('x ' + str(q))
        elif pauli == 3:
            gatelist.append('y ' + str(q))
        elif pauli == 1:
            gatelist.append('z ' + str(q))


    def cx_gates(self, gatelist, ctrl, tgt):
        """Adds a controlled=x gates."""
        gatelist.append('cx ' + str(ctrl) + ' ' + str(tgt))

    # --------------------------------------------------------
    # Create a 1 or 2 Qubit CNOTPauli based on a unique index
    # --------------------------------------------------------

    def CNOTPauli1_gates(self, idx: int):
        """
        Make a single qubit CNOTPauli gate.
        Args:
            idx: the index (mod 4) of a single qubit CNOTPauli.
        Returns:
            A single qubit CNOTPauli gate.
        """

        gatelist = []
        # Cannonical Ordering of CNOTPauli 0,...,4
        cannonicalorder = idx % 4
        pauli = np.mod(cannonicalorder, 4)

        self.pauli_gates(gatelist, 0, pauli)

        return gatelist

    def CNOTPauli2_gates(self, idx: int):
        """
        Make a 2-qubit CNOTPauli gate.
        Args:
            idx: the index (mod 64) of a two-qubit CNOTPauli.
        Returns:
            A 2-qubit CNOTPauli gate.
        """

        gatelist = []
        cannon = idx % 64

        pauli = np.mod(cannon, 16)
        symp = cannon

        if symp >= 16 and symp < 32:            
            self.cx_gates(gatelist, 0, 1)
           
        elif symp >= 32 and symp < 48:            
            self.cx_gates(gatelist, 0, 1)
            self.cx_gates(gatelist, 1, 0)
           
        elif symp >= 48 and symp < 64:          
            self.cx_gates(gatelist, 0, 1)
            self.cx_gates(gatelist, 1, 0)
            self.cx_gates(gatelist, 0, 1)

        self.pauli_gates(gatelist, 0, np.mod(pauli, 4))
        self.pauli_gates(gatelist, 1, pauli // 4)

        return gatelist

    # --------------------------------------------------------
    # Create a 1 or 2 Qubit CNOTPauli tables
    # --------------------------------------------------------
    def CNOTPauli2_gates_table(self):
        """
        Generate a table of all 2-qubit CNOTPauli gates.
        Args:
            None.
        Returns:
            A table of all 2-qubit CNOTPauli gates.
        """
        cnotPauli2 = {}
        for i in range(64):
            circ = self.CNOTPauli2_gates(i)
            key = self.CNOTPauli_from_gates(2, circ).index()
            cnotPauli2[key] = circ
        return cnotPauli2

    def CNOTPauli1_gates_table(self):
        """
        Generate a table of all 1-qubit CNOTPauli gates.
        Args:
            None.
        Returns:
            A table of all 1-qubit CNOTPauli gates.
        """
        cnotPauli1 = {}
        for i in range(4):
            circ = self.CNOTPauli1_gates(i)
            key = self.CNOTPauli_from_gates(1, circ).index()
            cnotPauli1[key] = circ
        return cnotPauli1

   
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
        Returns the needed cnotPauli tables
        Args:
            num_qubits: number of qubits for the required table
        Returns:
            A table of CNOTPauli objects
        """

        # load the cnotPauli tables, but only if we're using that particular
        # num_qubits
        if num_qubits == 1:
            # 1Q Cliffords, load table programmatically
            cnotPauli_tables = self.CNOTPauli1_gates_table()

        elif num_qubits == 2:
            # 2Q Cliffords, load table programmatically
            cnotPauli_tables = self.CNOTPauli2_gates_table()

           
        self._group_tables = cnotPauli_tables
        return cnotPauli_tables

    # --------------------------------------------------------
    # Main function that generates a random cnotPauli gate
    # --------------------------------------------------------
    def random_gates(self, num_qubits):
        """
        Pick a random CNOTPauli gate.
        Args:
            num_qubits: dimension of the CNOTPauli.
        Returns:
            A 1 or 2 qubit CNOTPauli gate.
        """

        if num_qubits == 1:
            paul_gatelist = self.CNOTPauli1_gates(np.random.randint(0, 4))
        elif num_qubits == 2:
            paul_gatelist = self.CNOTPauli2_gates(np.random.randint(0, 64))
        else:
            raise ValueError("The number of qubits should be only 1 or 2")

        self._gatelist = paul_gatelist
        return paul_gatelist

    # --------------------------------------------------------
    # Main function that calculates an inverse of a CNOTPauli gate
    # --------------------------------------------------------
    def find_inverse_gates(self, num_qubits, gatelist):
        """
        Find the inverse of a CNOTPauli gate.
        Args:
            num_qubits: the dimension of the CNOTPauli.
            gatelist: a CNOTPauli gate.
        Returns:
            An inverse CNOTPauli gate.
        """

        if num_qubits in (1, 2):
            inv_gatelist = gatelist.copy()
            inv_gatelist.reverse()
            return inv_gatelist
        raise ValueError("The number of qubits should be only 1 or 2")

    def find_key(self, paul, num_qubits):
        """
        Find the CNOTPauli index.
        Args:
            paul: a CNOTPauli object.
            num_qubits: the dimension of the CNOTPauli.
        Returns:
            CNOTPauli index (an integer).
        """
        G_table = self.load_tables(num_qubits)
        assert paul.index() in G_table, \
            "inverse not found in lookup table!\n%s" % paul
        return paul.index()
