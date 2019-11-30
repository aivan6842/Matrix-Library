from fractions import Fraction
import copy

class Matrix():
    def __init__(self, num_rows, num_cols, inter_created = False, inter_rows = []):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.rows = []
        self.cols = []
        self.inter_created = inter_created
        if not(self.inter_created):
            self.create_rows()
            self.create_cols()
        else:
            self.rows = inter_rows
            self.create_cols()
        

    def create_rows(self):
        '''
        (Matrix) -> None

        Prompts the user to create rows for the matrix.
        '''
        i = 0
        while i < self.num_rows:
            print(f'Enter the entries for row {i+1} separated by spaces:')
            entries = input().strip()
            row = entries.split()
            
            flag = False
            for j in range(len(row)):
                try:
                    row[j] = Fraction(row[j])
                except ValueError:
                    print('Invalid input')
                    flag = True
                    break

            if flag:
                 continue
            else:
                if len(row) > self.num_cols:
                    print('You entered more entries than the matrix requires.')
                    continue
                elif len(row) < self.num_cols:
                    print('You entered less entries than the matrix requires.')
                    continue
                self.rows.append(row)
                i += 1

    def create_cols(self):
        '''
        (Matrix) -> (None)

        Creates columns based on the given rows.
        '''
        for i in range(self.num_cols):
            col = []
            for row in self.rows:
                col.append(row[i])
            self.cols.append(col)

    def __repr__(self):
        '''
        (Matrix) -> (String)

        Returns the representation of a matrix.
        '''
        s = 'Matrix('
        for row in self.rows:
                s+= str(row) + ', '
        s = s[:-2] + ')'
        return s

    def __str__(self):
        '''
        (Matrix) -> String

        Returns the string representation of a matrix.
        '''
        s = ''
        for row in self.rows:
            for item in row:
                s += str(item)+ '  '
            s+= '\n'
        return s[:-1]


    def __eq__(self, other):
        '''
        (Matrix, Matrix) -> Boolean

        Returns true is both matrices are the same and false if they are not the same.
        '''
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            return False

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.rows[i][j] != other.rows[i][j]:
                    return False
        return True
    
    
    def __mul__(self, other):
        '''
        (Matrix, int or float or Fraction or Matrix) -> Exception or Matrix

        Returns a new matrix multipled by the other given argument or raises an exception if 2
        matrices cannot be multipled.
        '''
        if type(other) == int or type(other) == float or type(other) == Fraction:
            rows = []
            for row in self.rows:
                new_matrix_rows = []
                for entry in row:
                    new_matrix_rows.append(entry * other)
                rows.append(new_matrix_rows)
            return Matrix(self.num_rows, self.num_cols, True,rows)

        if self.num_cols != other.num_rows:
            raise Exception('Dimensions of matrices are not the same')

        rows = []
        for i in range(self.num_rows):
            new_matrix_row = []
            for j in range(other.num_cols):
                entry_sum = 0
                for z in range(self.num_cols):
                    entry_sum += self.rows[i][z] * other.cols[j][z]
                new_matrix_row.append(entry_sum)
            rows.append(new_matrix_row)
        return Matrix(self.num_rows, other.num_cols, True, rows)

    def __rmul__(self, other):
        '''
        (Matrix, int or float or Fraction or Matrix) -> Exception or Matrix

        Returns a new matrix multipled by the other given argument or raises an exception if 2
        matrices cannot be multipled.
        '''
        return Matrix.__mul__(self, other)

    def __add__(self, other):
        '''
        (Matrix, Matrix) -> Exception or Matrix

        Returns new matrix if the arguments can be added. If not an exception will be raised.
        '''
        if self.num_cols != other.num_cols or self.num_rows != other.num_rows:
            raise Exception('Dimensions of matrices are not the same.')

        rows = []
        for i in range(self.num_rows):
            new_matrix_rows = []
            for j in range(self.num_cols):
                new_matrix_rows.append(self.rows[i][j] + other.rows[i][j])
            rows.append(new_matrix_rows)
        return Matrix(self.num_rows, self.num_cols, True, rows)

    def __sub__(self, other):
        '''
        (Matrix, Matrix) -> Exception or Matrix

        Returns new matrix if the arguments can be subtracted. If not an exception will be raised.
        '''
        return Matrix.__add__(self, Matrix.__mul__(other, -1))

    def find_pivot(self, z=0, w=0):
        '''
        (Matrix, int, int) -> Tuple or None

        Given a matrix, the function will return a tuple containing the coordinates of the first
        pivot starting from (z, w) or None if no pivots are found from (z, w).

        '''
        for i in range(z, self.num_cols):
            for j in range(w, self.num_rows):
                if self.rows[j][i] != 0:
                    return (j, i)
        
    def swap_rows(self, row1, row2):
        '''
        (Matrix, int, int) -> None

        Swap 2 rows in a given matrix.
        '''
        self.rows[row1], self.rows[row2] = self.rows[row2], self.rows[row1]

    def scale_row(self, row_num, k):
        '''
        (Matrix, int, int or float or fraction) -> None

        Will multiply given row by k.
        '''
        for i in range(self.num_cols):
            self.rows[row_num][i] *= k

    def add_rows(self, row1, row2, k=1):
        '''
        (Matrix, int, int, float or int or fraction) -> None

        Will add k times row2 to row1. 
        '''
        for i in range(self.num_cols):
            self.rows[row1][i] += k*self.rows[row2][i]

    def sub_rows(self, row1, row2, k=1):
        '''
        (Matrix, int, int, float or int or fraction) -> None

        Will subtract k times row2 from row1.
        '''
        for i in range(self.num_cols):
            self.rows[row1][i] -= k*self.rows[row2][i]

    def ref(self):
        '''
        (Matrix) -> None

        Will convert the given matrix is Row Echelon Form.
        '''
        i = 0
        j = 0
        while i < self.num_rows and j < self.num_cols:
            piv = self.find_pivot(i, j)
            if not piv:
                break
            piv_row, piv_col = piv
            self.swap_rows(piv_row, i)
            piv_row = i
            j = piv_col

            if self.rows[piv_row][piv_col] > 0:
                const = Fraction(Fraction('1/1')/Fraction(self.rows[piv_row][piv_col]))
            elif self.rows[i][j] < 0:
                const = Fraction(Fraction('-1/1')/Fraction(-self.rows[piv_row][piv_col]))
            else:
                const = Fraction('0/1')
                
            self.scale_row(i, const)
            for z in range(i+1, self.num_rows):
                if self.rows[z][j] > 0:
                    self.sub_rows(z, i, self.rows[z][j])
                elif self.rows[z][j] < 0:
                    self.add_rows(z, i, -self.rows[z][j])
            i += 1
            j += 1
         

    def rref(self):
        '''
        (Matrix)

        Will convert the given matrix to Reduced Row Echelon Form.
        '''
        i = 0
        j = 0
        while i < self.num_rows and j < self.num_cols:
            piv = self.find_pivot(i, j)
            if not piv:
                break
            piv_row, piv_col = piv
            self.swap_rows(piv_row, i)
            piv_row = i
            j = piv_col

            if self.rows[piv_row][piv_col] > 0:
                const = Fraction(Fraction('1/1')/Fraction(self.rows[piv_row][piv_col]))
            elif self.rows[piv_row][piv_col] < 0:
                const = Fraction(Fraction('-1/1')/Fraction(-self.rows[piv_row][piv_col]))
            else:
                const = Fraction('0/1')
                
            self.scale_row(i, const)
            for z in range(self.num_rows):
                if z == i:
                    continue
                if self.rows[z][j] > 0:
                    self.sub_rows(z, i, self.rows[z][j])
                elif self.rows[z][j] < 0:
                    self.add_rows(z, i, -self.rows[z][j])
            i += 1
            j += 1

    def is_square(self):
        '''
        (Matrix) -> Boolean

        Returns True if matrix is a sqaure matrix and False if matrix isn't a square matrix.
        '''
        return self.num_rows == self.num_cols        

    def determinant(self):        
        '''
        (Matrix) -> Exception or Fraction

        Returns the determinant of the matrix or raises an exception if the matrix is not a sqaure.
        '''
        row_swaps = 0
        total_scale = 1
        temp_matrix = copy.deepcopy(self)

        if not temp_matrix.is_square():
            raise Exception('Can\'t compute determinant of a non square matrix')

        i = 0
        j = 0
        while i < temp_matrix.num_rows and j < temp_matrix.num_cols:
            piv = temp_matrix.find_pivot(i, j)
            if not piv:
                break
            piv_row, piv_col = piv

            if piv_row != i:
                temp_matrix.swap_rows(piv_row, i)
                row_swaps += 1
                piv_row = i

            if temp_matrix.rows[piv_row][piv_col] > 0:
                const = Fraction(Fraction('1/1')/Fraction(temp_matrix.rows[piv_row][piv_col]))
            elif temp_matrix.rows[i][j] < 0:
                const = Fraction(Fraction('-1/1')/Fraction(-temp_matrix.rows[piv_row][piv_col]))
            else:
                const = Fraction('0/1')
                
            if const != 1:
                temp_matrix.scale_row(i, const)
                total_scale *= const
            
            for z in range(i+1, temp_matrix.num_rows):
                if temp_matrix.rows[z][j] > 0:
                    temp_matrix.sub_rows(z, i, temp_matrix.rows[z][j])
                elif temp_matrix.rows[z][j] < 0:
                    temp_matrix.add_rows(z, i, -temp_matrix.rows[z][j])
            i += 1
            j += 1

        for i in range(temp_matrix.num_rows):
                if temp_matrix.rows[i][i] != 1:
                    return 0
        return (1/total_scale) * (-1)**(row_swaps)
        
         
