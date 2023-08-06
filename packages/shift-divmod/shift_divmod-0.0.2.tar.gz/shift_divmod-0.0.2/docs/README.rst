==============================================================================
ShiftDivMod.  Implement faster divmod() for moduli with trailing 0 bits
==============================================================================
:Info: This is the README file for ShiftDivMod.
:Author: Shlomi Fish <shlomif@cpan.org>
:Copyright: © 2020, Shlomi Fish.
:Date: 2020-09-13
:Version: 0.0.2

.. index: README
.. image:: https://travis-ci.org/shlomif/shift_divmod.svg?branch=master
   :target: https://travis-ci.org/shlomif/shift_divmod

PURPOSE
-------

This distribution implements faster divmod() (and ``.mod()``) operations
for moduli with a large number of trailing 0 bits (where the div/mod base
is divisible by ``2 ** n`` for an integer `n`).

It should yield the same result as the built-n divmod() function for
positive numerators (its behaviour for negative ones is currently
untested and undefined).

INSTALLATION
------------

pip3 install shift_divmod

USAGE
-----

::

    from shift_divmod import ShiftDivMod

    base = 997
    shift = 1200
    modder = ShiftDivMod(base, shift)
    # Alternative constructor which may require more
    # work and eventualy calls the default constructor
    modder = ShiftDivMod.from_int(base << shift)

    x = 10 ** 500
    # Same as divmod(x, (base << shift))
    print( modder.divmod(x) )

NOTES
-----

The code from which this distribution has been derived, was proposed as a
proof-of-concept for a potential improvement for the built in cpython3
operations here: https://bugs.python.org/issue41487 . However, changing cpython3
in this manner was rejected.

libdivide ( https://github.com/ridiculousfish/libdivide ) provides a
different, but also interesting, approach for optimizing division.

COPYRIGHT
---------
Copyright © 2020, Shlomi Fish.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions, and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions, and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. Neither the name of the author of this software nor the names of
   contributors to this software may be used to endorse or promote
   products derived from this software without specific prior written
   consent.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
