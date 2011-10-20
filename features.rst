==================================================
Features to come
==================================================

Overall architecture:

Now everything will be implemented using PyQt. Also, reduction scripts should be drawn from this package.


Line Fitting



have an easily accesible section in the program where you can insert your own functions which to fit to the lines. The user just edits the code.

Having a good line database

* Single lines
* Multiplet viewer can add or subtract multiplet lines
* Search within a wavelength range to see which lines might apply

That user can add lines ad hoc
Spectrum remembers which lines have been labelled
Needs a continuum finding routine

Can convert line profiles to velocity space easily
Create routines for viewing these.

Be able to switch from normal to log space easily


View Options
==================================================

Turn on/off Grid
Switch from Linear to Log space
Switch from wavelength to velocity space (also select from common lines to make zero velocity).

Select which spectra are visible on the main plot screen. This will be accomplished through the Tix checkList extension.

spectrum.multiplicative_offset and spectrum.additive_offset will be used to scale spectrum so that they appear in the same window.

The tix.CheckList will be very helpful for displaying certain spectral lines, when the time comes. Perfect utility for browsing them.


Import/Export
==================================================

Can read spectra in a variety of formats
        This needs some more work to be robust.

Can export spectra in a variety of formats (mostly ASCII right now)

Keep track of recent spectra viewed

Easily convert UT, sidereal times.

Function to quickly view header


