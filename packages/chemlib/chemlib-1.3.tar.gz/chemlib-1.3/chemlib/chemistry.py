import pandas as pd
import numpy as np
import sympy
from fractions import Fraction
from io import StringIO

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
AVOGADROS_NUMBER = 6.02e+23

class PeriodicTable(pd.DataFrame):

    def __init__(self, *args, **kwargs):
        super(PeriodicTable, self).__init__(pd.read_csv(r"chemlib/resources/PTE_updated.csv"))
        
    def get_element_properties_from_symbol(self, symbol):
        values = np.array(self.iloc[[self.index[self['Symbol'] == symbol].tolist()[0]]]).ravel()
        keys = list(self)
        return dict(zip(keys, values))

pte = PeriodicTable()

class Element:
    
    def __init__(self, symbol): 
        self.properties = pte.get_element_properties_from_symbol(symbol)
        for key in self.properties:
            setattr(self, key, self.properties[key])

class Compound:

    def __init__(self, atom_list):
        self.atom_list = atom_list 
        self.types = list(dict.fromkeys(self.atom_list))
        self.occurences = dict(zip(self.types, [self.atom_list.count(i) for i in self.types]))
        self.formula = list(zip(self.types, [self.atom_list.count(i) for i in self.types]))
        self.formula = sum([[i[0], i[1]] for i in self.formula], [])
        self.formula = (''.join([str(i) for i in self.formula])).translate(SUB)
        self.elements = [Element(i) for i in self.atom_list]

    def molar_mass(self):
        mass = 0
        for element in self.elements:
            mass += element.AtomicMass
        return round(mass, 2)

    def percentage_by_mass(self, element):
        return round(((self.occurences[element] * Element(element).AtomicMass) / self.molar_mass()) * 100, 3)
    
    def get_amounts(self, **kwargs):
        keys = kwargs.keys()

        if 'grams' not in keys and 'moles' not in keys and 'molecules' not in keys:
            raise TypeError('Expecting one argument: either grams= , moles= , or molecules=')

        if len(kwargs) > 1:
            raise TypeError(f"Got {len(kwargs)} arguments when expecting 1. Use either grams= , moles=, or molecules=")

        if 'grams' in keys:
            grams = kwargs['grams']
            mols = grams/self.molar_mass()
            molecules = mols*AVOGADROS_NUMBER

        elif 'moles' in keys:
            mols = kwargs['moles']
            grams = mols*self.molar_mass()
            molecules = mols*AVOGADROS_NUMBER
        
        elif 'molecules' in keys:
            molecules = kwargs['molecules']
            mols = molecules / AVOGADROS_NUMBER
            grams = mols*self.molar_mass()

        return {
            'Compound': self.formula,
            'Grams': round(grams, 3),
            'Moles': round(mols, 4), 
            'Molecules': float('{:0.3e}'.format(molecules))
        }

class Reaction:
    def __init__(self, reactants, products):
        self.reactants = reactants
        self.products = products
        self.compounds = self.reactants + self.products
        self.reactant_formulas = [reactant.formula for reactant in self.reactants]
        self.product_formulas = [product.formula for product in self.products]
        self.update_formula()

        self.reactant_occurences = {}
        self.product_occurences = {}

        for i in [self.reactants, self.products]:
            for reactant in i: 
                for key in reactant.occurences:
                    if i == self.reactants:
                        if not key in self.reactant_occurences:
                            self.reactant_occurences[key] = reactant.occurences[key]
                        else:
                            self.reactant_occurences[key] += reactant.occurences[key]
                    else:
                        if not key in self.product_occurences:
                            self.product_occurences[key] = reactant.occurences[key]
                        else:
                            self.product_occurences[key] += reactant.occurences[key]
                            
        if self.reactant_occurences == self.product_occurences:
            self.is_balanced = True
        else:
            self.is_balanced = False
        
    def update_formula(self):
        self.formula = []

        for i in self.reactants: self.formula.append(i.formula)
        self.formula.append(' --> ')
        for i in self.products: self.formula.append(i.formula)

        self.frequencies = {i:self.formula.count(i) for i in self.formula}
        self.constituents = list(dict.fromkeys(self.formula))

        self.formula = []
        for i in self.constituents:
            self.formula.append(str(self.frequencies[i]) + i)

        del self.frequencies[' --> ']
        self.constituents.remove(' --> ')

        self.formula = ' + '.join(self.formula).replace('+ 1 ', '').replace('  +', '')

    def balance(self):
        if not self.is_balanced:
            reference_vector = []
            seen_formulas = []
            for j in [self.reactants, self.products]:
                for compound in j:
                    for i in compound.elements:
                        if i.Symbol not in seen_formulas:
                            seen_formulas.append(i.Symbol)
                            reference_vector.append(i)

            compound_formulas = []
            compounds = []
            for j in [i for i in self.compounds]:
                if j.formula not in compound_formulas:
                    compound_formulas.append(j.formula)
                    compounds.append(j)

            matrix = []
            for compound in compounds:
                col = []
                for m in seen_formulas:
                    try:
                        if compound.formula in self.product_formulas:
                            col.append(-compound.occurences[m])
                        else:
                            col.append(compound.occurences[m])
                    except:
                        col.append(0)
                matrix.append(col)
            
            matrix = sympy.Matrix(np.array(matrix).transpose()).rref() #Row - echelon form
            solutions = list(np.array(matrix[0][:, -1].tolist() + [matrix[-1][-1]]))
            solutions = np.array([[i] if type(i) is int else i for i in solutions]).ravel().astype(np.float)
            solutions = [abs(i) for i in solutions]
            denominators = [f.denominator for f in [Fraction(x).limit_denominator() for x in solutions]]
            solutions = [int(i*max(denominators)) for i in solutions]
            solutions[-1] = max(denominators)
            while 0 in solutions:
                solutions.remove(0)

            final_reactants = []
            final_products = []

            for sol in range(len(compounds)):
                if compounds[sol].formula in self.reactant_formulas:
                    final_reactants.append([compounds[sol]]*solutions[sol])

                if compounds[sol].formula in self.product_formulas:
                    final_products.append([compounds[sol]]*solutions[sol])
            
            final_reactants = sum(final_reactants, [])
            final_products = sum(final_products, [])
            
            self.__init__(reactants = final_reactants, products = final_products)

        else:
            return True

if __name__ == '__main__':
    print(pte)
    b = Element('B')
    print(b.properties)