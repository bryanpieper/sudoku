""" 
Sudoku puzzle models and model logic.

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

from django.db import models

class GeneratedSudoku(models.Model):
    """
    Generated sudoku record
    """
    alias = models.CharField(db_index=True, max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField()
    user_agent = models.CharField(max_length=255, blank=True)
    factor = models.PositiveIntegerField(null=True, default=4)
    sudoku_data = models.TextField(editable=False)
    sudoku_masked = models.TextField(editable=False)


def marshal_grid(grid):
    """
    Marshall the grid data
    """
    import cPickle as pickle
    return pickle.dumps(grid)
    
    
def unmarshal_grid(grid_str):
    """
    Unmarshall grid data
    """
    import cPickle as pickle
    from cStringIO import StringIO
    buf = StringIO()
    buf.write(grid_str)
    buf.reset()
    return pickle.load(buf)
    