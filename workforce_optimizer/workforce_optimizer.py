import pulp
import pandas as pd
from utils.dataexchange import Data

class Optimizer:
    def __init__(self):
        self.num_applicants = 50
        self.name = Data.get_applicants()
        self.dept = ['D1', 'D2']
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.shift = ['S1', 'S2', 'S3', 'S4']
        self.demand  = Data.get_demand_df()
        self.E = Data.get_availibility_df()
        self.x = None
        self.z = None

        self.model = pulp.LpProblem('Cost',pulp.LpMinimize)
        self._create_variables()
        self._create_objective()
        self._create_demand_constraint()
        self._create_supply_constraint()
        self._one_department_in_shift_constraint()
        self._allocate_to_available_shit_constraint()

    def _create_objective(self):
        self.model += (29*sum([self.x[i][j][k][l] for i in self.name for j in self.dept for k in self.days for l in self.shift])
                 + 70 * sum([self.z[i] for i in self.name]))

    def _create_variables(self):
        self.x = pulp.LpVariable.dicts('X_%s%s%s%s', (self.name, self.dept, self.days, self.shift), lowBound=0, cat='Binary')
        self.z = pulp.LpVariable.dicts('Z_%s%s', (self.name), lowBound=0, cat='Binary')

    def _create_demand_constraint(self):
        for j in self.dept:
            for k in self.days:
                for l in self.shift:
                    self.model += sum([self.x[i][j][k][l] for i in self.name]) >= self.demand.loc[j, k, l]


    def _create_supply_constraint(self):
        for i in self.name:
            self.model += sum([self.x[i][j][k][l] for j in self.dept for k in self.days for l in self.shift]) <= 5 * z[i]

    def _one_department_in_shift_constraint(self):
        for i in self.name:
            for k in self.days:
                for l in self.shift:
                    self.model+=sum([self.x[i][j][k][l] for j in self.dept]) <= 1

    def _allocate_to_available_shit_constraint(self):
        for i in self.name:
            for j in self.dept:
                for k in self.days:
                    for l in self.shift:
                        self.x[i][j][k][l] = self.E[i][j][k][l]

    def solve(self):
        self.model.solve(pulp.GUROBI(mip=True, epgap=.0067))

    def write_to_file(self):
        result = Data.master_df.copy()
        result.iloc[0:, 0:50] = 0
        result.iloc[0:, 0:] = result.iloc[0:, 0:].astype(str)

        for i in self.name:
            for j in self.dept:
                for k in self.days:
                    for l in self.shift:
                        if self.x[i][j][k][l].value() == 1:
                            result.loc[j, k, l][i] = 1
                        else:
                            result.loc[j, k, l][i] = 0

        for i in self.name:
            if sum([self.x[i][j][k][l].value() for j in self.dept for k in self.days for l in self.shift]) == 0:
                result.loc['D1', 'Monday', 'S1'][i] = "Not Hired"

        final = result.T
        final.to_csv('out.csv')

def main():
    model = Optimizer()
    model.solve()
    model.write_to_file()

if __name__=="__main__":
    model = Optimizer()
    model.solve()
    model.write_to_file()


