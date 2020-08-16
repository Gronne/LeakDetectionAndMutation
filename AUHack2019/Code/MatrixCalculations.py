import copy

class MatrixCalculations:
    def __init__(self):
        pass

    def generate_zero_matrix(self, rows, columns):
        column = [0 for count in range(0, columns)]
        zero_matrix = [copy.deepcopy(column) for count in range(0, rows)]

        return zero_matrix


    def multiply_matrices(self, matrix_a, matrix_b):
        zero_matrix = self.generate_zero_matrix(self.rows(matrix_a), self.columns(matrix_b))

        for row_nr, vector_a in enumerate(self.get_rows(matrix_a)):
            for col_nr, vector_b in enumerate(self.get_columns(matrix_b)):
                zero_matrix[row_nr][col_nr] = self.multiply_vector(vector_a, vector_b)

        return zero_matrix


    def get_rows(self, matrix):
        return matrix


    def get_columns(self, matrix):
        return self.transpose(matrix)


    def transpose(self, matrix):
        new_matrix = self.generate_zero_matrix(self.columns(matrix), self.rows(matrix))

        for row_nr in range(0, self.rows(matrix)):
            for col_nr in range(0, self.columns(matrix)):
                new_matrix[col_nr][row_nr] = copy.deepcopy(matrix[row_nr][col_nr])

        return new_matrix


    def multiply_vector(self, vector_a, vector_b):
        return sum([float(vector_a[element_counter]) * float(vector_b[element_counter]) for element_counter in range(0, len(vector_a))])


    def rows(self, matrix):
        return len(matrix)


    def columns(self, matrix):
        return len(matrix[0])
