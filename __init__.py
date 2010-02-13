"""
Sudoku puzzle module implementation.  A standard 9x9 grid with 3x3 latin squares.

Copyright (c) 2009 Bryan Pieper, http://www.thepiepers.net/

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import random, sys, time

# latin square points (3x3) / (x,y)
grids = (
    (0, 0), (0, 3), (0, 6),
    (3, 0), (3, 3), (3, 6),
    (6, 0), (6, 3), (6, 6),
)

grid_size = 9
grid_index = {}

# build the grid index for fast lookup keyed by x,y
for pos in grids:
    for x in xrange(0, 3):
        for y in xrange(0, 3):
            grid_key = ','.join([str((pos[0] + x)), str((pos[1] + y))])
            grid_index[grid_key] = pos


def generate_sudoku():
    """
    Generate the sudoku grid (9x9) with (3x3) latin squares
    @return multi-dimensional array
    """
    buckets = []
    matrix = []
    
    # max time alloted to create grid, if exceeded, will restart and try another
    # random set
    max_time = 0.02   
    
    # setup matrix and buckets with random values
    def setup_grids():
        del buckets[:]
        del matrix[:]
        for _x in xrange(0, grid_size):
            data = range(1, grid_size + 1)
            random.shuffle(data)
            buckets.append(data)
            matrix.append([])
 
    # scan column for value
    def in_column(col, val):
        for n in xrange(0, grid_size):
            if matrix[n] and len(matrix[n]) > col:
                if matrix[n][col] == val:
                    return True
        return False
    
    # scan grid range (3x3)
    def in_grid(col, row, val):
        grid_key = ','.join([str(row), str(col)])
        grid_pos = grid_index[grid_key]
        _x = grid_pos[0]
        _y = grid_pos[1]
        for _i in xrange(0, 3):
            for _j in xrange(0, 3):
                try:
                    if matrix[(_x + _i)][(_y + _j)] == val:
                        return True
                except IndexError:
                    break
             
        return False
    
    # bucket check
    bucket_filter = lambda b: len(b) > 0
    
    # sanity limit
    round_timelimit = 0.001
    
    while 1:
        setup_grids()
        
        # starting time
        start = time.time()
    
        for i, row in enumerate(buckets):
            
            # sanity check
            if (time.time() - start) > max_time:
                break
            
            if i == 0:
                # append first row as-is
                matrix[i] = row[:]
                del row[:]
            else:
                # current column
                y = 0
                
                # keep a copy
                row_copy = row[:]
                next_row = []
                matrix[i] = next_row
                
                # sanity check time/count
                round_start = time.time()                
                
                while len(next_row) < grid_size:
                    
                    # sanity check
                    if (time.time() - start) > max_time:
                        break
                    
                    if (time.time() - round_start) > round_timelimit:
                        # we have a combination that won't work, start the row over
                        del next_row[:]
                        del row[:]
                        random.shuffle(row_copy)
                        row = row_copy[:]
                        y = 0
                        round_start = time.time()
                    
                    for num in row[:]:
                        if not in_column(y, num) and not in_grid(y, i, num):
                            next_row.append(num)
                            # move to next column
                            y += 1
                            # we are done with the bucket value
                            row.remove(num)

        if not filter(bucket_filter, buckets):
            break
 
    return matrix
    
    
def print_grid(grid, outfile=sys.stdout):
    """
    Print the given grid to the outfile
    """
    
    def mask_num(n):
        val = n
        if not val:
            val = ' '
        return str(val)
    
    for g in grid:
        print >> outfile, ' ', '  '.join([ mask_num(i) for i in g])
        


def masked_grid(grid, factor=2):
    """
    Take the given grid and mask out random values with 0's. Bases
    the difficulty on the factor value (the min taken out per row)
    """
    new_grid = grid[:]
    
    for x in xrange(0, len(grid)):
        xlen = len(new_grid[x]) 
        xmin = factor
        if (xmin >= xlen):
            xmin = xlen - 1
        xmax = xlen
        sample_size = random.randint(xmin, xmax)
        
        for n in xrange(0, sample_size):
            while 1:
                xindex = random.randint(0, (len(new_grid[x]) - 1))
                if new_grid[x][xindex]:
                    new_grid[x][xindex] = 0
                    break
                
    return new_grid
                    

def valid_grid(grid):
    """
    Check the grid rows and columns for valid ranges
    """
    def column(col):
        for n in xrange(0, len(grid)):
            yield grid[n][col]
    
    def row(r):
        for n in xrange(0, len(grid)):
            yield grid[r][n]
    
    for x in xrange(0, len(grid)):
       x_map = {}
       for n in column(x):
           if n in x_map:
               return False

    for y in xrange(0, len(grid)):
       y_map = {}
       for n in row(y):
           if n in y_map:
               return False
           
    return True 



def time_grids():
    """
    Print grid timing output
    """
    start = time.time()
    num = 1000
    high = 0
    low = 9999
    for n in xrange(num):
        _start = time.time()
        matrix = generate_sudoku()
        
        #if not valid_grid(matrix):
        #    print 'invalid'
        
        _end = time.time()
        _duration = _end - _start 
        
        if (_end - _start) > high:
            high = _duration
        if (_end - _start < low):
            low = _duration
            
        print '.',
        if n % 10 == 0:
            print ''
    print ''
    end = time.time()
        
    _time = (end - start)
    print "Generated %d grids" % num
    print "Average time per gen",  _time / num
    print "Total time", _time, "seconds"
    print "High", high
    print "Low", low
    print "Grids per second", num / _time
    
        
    
if __name__ == '__main__':
    matrix = generate_sudoku()
    print_grid(matrix)
    print ''
    print_grid(masked_grid(matrix, factor=4))
    
    #time_grids()
    
