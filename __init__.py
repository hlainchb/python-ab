"""

    Program.....: ab.py
    Author......: Herb Lainchbury
    License.....: (C) 2011 Dynamic Solutions Inc.
    Description.: python split test library

"""

import traceback

class Variant:
    def __init__(self, name, properties=None):
        self.name = name
        self.properties = properties

    def __repr__(self):
        return 'Variant(%s,%s)' % (repr(self.name),repr(self.properties))

class Selector:
    def select(self):
        pass

class FixedSelector(Selector):
    """
    A variant selector that returns a fixed variant.

    >>> selector = FixedSelector('one')
    >>> selector.select('123')
    'one'

    """
    def __init__(self, variant_name):
        self.variant_name = variant_name

    def select(self, subject):
        return self.variant_name
        
class Logger:
    def log(self, test, variant, subject):
        pass

class MultiLogger:
    def __init__(self, loggers, system_logger):
        self.loggers = loggers
        self.system_logger = system_logger

    def log(self, test, variant, subject):
        for i, logger in enumerate(self.loggers):
            try:
                logger.log(test, variant, subject)
            except:
                self.system_logger('ab logger %d failed: %s' % (i,traceback.format_exc))

class SubjectIDProvider:
    def get_id(self): pass

class Test:
    def __init__(self, name, variants, selector, id_provider, logger, enabled=True):
        """
        Runs a test.

        >>> test = Test('t1',[Variant('a'),Variant('b')],FixedSelector('a'),lambda: '001',Logger())

        """
        self.name = name
        self.variants = variants
        self.selector = selector
        self.id_provider = id_provider
        self.logger = logger
        self.enabled = enabled
        self.variant_lookup = dict((v.name, v) for v in variants)
        
    def select(self,subject_id=None):
        """
        Select one of the variants.

        >>> test = Test('t1',[Variant('a'),Variant('b')],FixedSelector('a'),lambda: '001',Logger())
        >>> test.select()
        Variant('a',None)

        >>> test.select().name
        'a'

        """
        if self.enabled:
            subject = subject_id or self.id_provider()
            key = self.selector.select(subject)    
            if key in self.variant_lookup:
                self.logger.log(self.name,key,subject)
                return self.variant_lookup[key]

if __name__ == '__main__':
    import doctest
    doctest.testmod()

