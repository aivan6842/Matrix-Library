# Matrix-Library
This is a library of matrix operations.

Create a matrix by calling the Matrix constructor and passing the number of rows and columns the matrix should have:
  - `matrix = Matrix(# of rows, # of cols)

Methods included:
  - Matrix multiplication
      - `matrix1 * matrix2
  - Scalar(k) matrix multiplication
      - `k * matrix
  - Addition of matrices
      - `matrix1 + matrix2
  - Subtraction of matrices
      - `matrix1 - matrix2
  - Elementary row operations
      - Row swapping
       - `matrix.swap_rows(row1, row2)
      - Row multiplication by scalar(k)
       - `matrix.scale_row(row, k)
      - Adding scalar mutliples of rows
       - `matrix.add_rows(row1, row2, k)
      - Subtracting scalar multiples of rows
       - `matrix.sub_rows(row1, row2, k)
  - Converting matrix to Row Echelon Form
      - `matrix.ref()
  - Converting matrix to Reduced Row Echelon Form
      - `matrix.rref()
  - Finding determinant
      - `matrix.determinant()`
