"""
Presumably I copied this in from holoviews and hacked til it worked,
as a proof of concept? But since holoviews is deprecating magics, no
attempt was ever made (or will ever be made...) to do it properly :)
"""

from itertools import groupby

IGNORED_LINE_MAGICS = ['output']
IGNORED_CELL_MAGICS = ['output']

try:
    import numpy # noqa: Some bad numpy/pytest interaction. Without importing numpy here (so it happens when nbsmoke is imported, i.e. at plugin load time,
                 # we get the traceback in https://github.com/numpy/numpy/issues/14012 (no idea if same cause)
except ImportError:
    pass

def _make_optsspec():
    from holoviews.util.parser import OptsSpec
    
    class NbSmokeOptsSpec(OptsSpec):
    
        @classmethod
        def _hvparse(cls, line, ns={}):
            """
            Parse an options specification, returning a dictionary with
            path keys and {'plot':<options>, 'style':<options>} values.
            """
            parses  = [p for p in cls.opts_spec.scanString(line)]
            if len(parses) != 1:
                raise SyntaxError("Invalid specification syntax.")
            else:
                e = parses[0][2]
                processed = line[:e]
                if (processed.strip() != line.strip()):
                    raise SyntaxError("Failed to parse remainder of string: %r" % line[e:])
        
            grouped_paths = cls._group_paths_without_options(cls.opts_spec.parseString(line))
            things = []
            for pathspecs, group in grouped_paths:
        
        #        normalization = cls.process_normalization(group)
        #        if normalization is not None:
        #            options['norm'] = normalization
        
                if 'plot_options' in group:
                    plotopts =  group['plot_options'][0]
                    opts = cls.todict(plotopts, 'brackets', ns=ns)
                    things+=opts
        
                if 'style_options' in group:
                    styleopts = group['style_options'][0]
                    opts = cls.todict(styleopts, 'parens', ns=ns)
                    things+=opts
        
            return things
        
        @classmethod
        def _hvtodict(cls, parseresult, mode='parens', ns={}):
            """
            Helper function to return dictionary given the parse results
            from a pyparsing.nestedExpr object (containing keywords).
        
            The ns is a dynamic namespace (typically the IPython Notebook
            namespace) used to update the class-level namespace.
            """
            grouped = []
            things = []
            tokens = cls.collect_tokens(parseresult, mode)
            # Group tokens without '=' and append to last token containing '='
            for group in groupby(tokens, lambda el: '=' in el):
                (val, items) = group
                if val is True:
                    grouped += list(items)
                if val is False:
                    elements =list(items)
                    # Assume anything before ) or } can be joined with commas
                    # (e.g tuples with spaces in them)
                    joiner=',' if any(((')' in el) or ('}' in el))
                                      for el in elements) else ''
                    grouped[-1] += joiner + joiner.join(elements)
        
            for keyword in grouped:
                # Tuple ('a', 3) becomes (,'a',3) and '(,' is never valid
                # Same for some of the other joining errors corrected here
                for (fst,snd) in [('(,', '('), ('{,', '{'), ('=,','='),
                                  (',:',':'), (':,', ':'), (',,', ','),
                                  (',.', '.')]:
                    keyword = keyword.replace(fst, snd)
        
                things.append('dict(%s)' % keyword)
        
            return things

    return NbSmokeOptsSpec
        

def opts_handler(magic):
    """Given an opts magic, return line of python suitable for pyflakes."""

    NbSmokeOptsSpec = _make_optsspec()
    string_of_magic_args = magic.python
    return " ; ".join(NbSmokeOptsSpec.parse(string_of_magic_args)) + " # noqa: here to use names for original %s magic: %s"%(magic.__class__.__name__, magic.python)


cell_magic_handlers = {'opts': opts_handler}
line_magic_handlers = {'opts': opts_handler}
