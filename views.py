""" 
Sudoku puzzle web views.

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

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from sudoku.models import GeneratedSudoku

def index(request):
    return render_to_response('sudoku/index.html', { },
              context_instance=RequestContext(request))


def generate(request):
    """
    Generate the grid and redirect to grid view
    """
    import sudoku
    import hashlib
    from sudoku.models import marshal_grid
    from django.http import HttpResponseRedirect
    from django.core.urlresolvers import reverse
    
    grid = sudoku.generate_sudoku()
    grid_str = marshal_grid(grid)
    grid_mask = marshal_grid(sudoku.masked_grid(grid, factor=2))
    grid_alias = hashlib.sha224(grid_str).hexdigest()
    
    ip_address = request.META['REMOTE_ADDR']
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip_address = request.META['HTTP_X_FORWARDED_FOR']
    user_agent = request.META['HTTP_USER_AGENT']
    
    gs = GeneratedSudoku(alias=grid_alias)
    gs.ip_address = ip_address
    gs.user_agent = user_agent
    gs.sudoku_data = grid_str
    gs.sudoku_masked = grid_mask
    gs.save()

    return HttpResponseRedirect(reverse('sudoku-view', args=[grid_alias]))


def view(request, alias, printable=False):
    """
    Displays the sudoku puzzle.
    """    
    from sudoku.models import unmarshal_grid
    
    try:
        gs = GeneratedSudoku.objects.get(alias=alias)
    except GeneratedSudoku.DoesNotExist:
        return generate(request)
    
    grid_mask = unmarshal_grid(gs.sudoku_masked)
    
    template_view = 'sudoku/view.html'
    if printable:
        template_view = 'sudoku/print.html'
    
    return render_to_response(template_view, { 'alias': gs.alias, 
                                                   'grid_mask': grid_mask, 'grid_date': gs.created },
            context_instance=RequestContext(request))
    
    
    
def answers(request, alias):
    """
    Get sudoku answers
    """
    from sudoku.models import unmarshal_grid
    import sudoku
    
    try:
        gs = GeneratedSudoku.objects.get(alias=alias)
    except GeneratedSudoku.DoesNotExist:
        return generate(request)
     
    grid_data = unmarshal_grid(gs.sudoku_data)
    grid_mask = unmarshal_grid(gs.sudoku_masked)

    # apply answers content
    for row in xrange(0, sudoku.grid_size):
        for col in xrange(0, sudoku.grid_size):
            if not grid_mask[row][col]:
                grid_data[row][col] *= -1

    return render_to_response('sudoku/answers.html', { 'alias': gs.alias, 'grid_mask': grid_mask,
                                                   'grid': grid_data, 'grid_date': gs.created },
            context_instance=RequestContext(request))

