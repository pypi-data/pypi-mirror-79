# -*- coding: utf-8 -*-
# Copyright (c) 2020 Salvador E. Tropea
# Copyright (c) 2020 Instituto Nacional de Tecnología Industrial
# License: GPL-3.0
# Project: KiBot (formerly KiPlot)
from pcbnew import EDGE_MODULE, wxPoint, LSET
from .gs import GS
from .misc import Rect
from .kiplot import load_sch
from .registrable import RegOutput
from .optionable import Optionable, BaseOptions
from .fil_base import BaseFilter, apply_fitted_filter, reset_filters
from .macros import macros, document  # noqa: F401
from . import log

logger = log.get_logger(__name__)


class BaseOutput(RegOutput):
    def __init__(self):
        super().__init__()
        with document:
            self.name = ''
            """ Used to identify this particular output definition """
            self.type = ''
            """ Type of output """
            self.dir = '.'
            """ Output directory for the generated files """
            self.comment = ''
            """ A comment for documentation purposes """  # pragma: no cover
        self._sch_related = False
        self._unkown_is_error = True

    @staticmethod
    def attr2longopt(attr):
        return '--'+attr.replace('_', '-')

    def is_sch(self):
        """ True for outputs that works on the schematic """
        return self._sch_related

    def is_pcb(self):
        """ True for outputs that works on the PCB """
        return not self._sch_related

    def config(self):
        super().config()
        if getattr(self, 'options', None) and isinstance(self.options, type):
            # No options, get the defaults
            self.options = self.options()
            # Configure them using an empty tree
            self.options.config()

    def run(self, output_dir, board):
        self.options.run(output_dir, board)


class BoMRegex(Optionable):
    """ Implements the pair column/regex """
    def __init__(self):
        super().__init__()
        self._unkown_is_error = True
        with document:
            self.column = ''
            """ Name of the column to apply the regular expression """
            self.regex = ''
            """ Regular expression to match """
            self.field = None
            """ {column} """
            self.regexp = None
            """ {regex} """


class VariantOptions(BaseOptions):
    """ BaseOptions plus generic support for variants. """
    def __init__(self):
        with document:
            self.variant = ''
            """ Board variant to apply """
            self.dnf_filter = Optionable
            """ [string|list(string)=''] Name of the filter to mark components as not fitted.
                A short-cut to use for simple cases where a variant is an overkill """
        super().__init__()
        self._comps = None

    def config(self):
        super().config()
        self.variant = RegOutput.check_variant(self.variant)
        self.dnf_filter = BaseFilter.solve_filter(self.dnf_filter, 'dnf_filter')

    def get_refs_hash(self):
        if not self._comps:
            return None
        return {c.ref: c for c in self._comps}

    def get_fitted_refs(self):
        """ List of fitted and included components """
        if not self._comps:
            return []
        return [c.ref for c in self._comps if c.fitted and c.included]

    def get_not_fitted_refs(self):
        """ List of 'not fitted' components, also includes 'not included' """
        if not self._comps:
            return []
        return [c.ref for c in self._comps if not c.fitted or not c.included]

    @staticmethod
    def cross_module(m, rect, layer):
        """ Draw a cross over a module.
            The rect is a Rect object with the size.
            The layer is which layer id will be used. """
        seg1 = EDGE_MODULE(m)
        seg1.SetWidth(120000)
        seg1.SetStart(wxPoint(rect.x1, rect.y1))
        seg1.SetEnd(wxPoint(rect.x2, rect.y2))
        seg1.SetLayer(layer)
        seg1.SetLocalCoord()  # Update the local coordinates
        m.Add(seg1)
        seg2 = EDGE_MODULE(m)
        seg2.SetWidth(120000)
        seg2.SetStart(wxPoint(rect.x1, rect.y2))
        seg2.SetEnd(wxPoint(rect.x2, rect.y1))
        seg2.SetLayer(layer)
        seg2.SetLocalCoord()  # Update the local coordinates
        m.Add(seg2)
        return [seg1, seg2]

    def cross_modules(self, board, comps_hash):
        """ Draw a cross in all 'not fitted' modules using *.Fab layer """
        # Cross the affected components
        ffab = board.GetLayerID('F.Fab')
        bfab = board.GetLayerID('B.Fab')
        extra_ffab_lines = []
        extra_bfab_lines = []
        for m in board.GetModules():
            ref = m.GetReference()
            # Rectangle containing the drawings, no text
            frect = Rect()
            brect = Rect()
            c = comps_hash.get(ref, None)
            if c and c.included and not c.fitted:
                # Meassure the component BBox (only graphics)
                for gi in m.GraphicalItems():
                    if gi.GetClass() == 'MGRAPHIC':
                        l_gi = gi.GetLayer()
                        if l_gi == ffab:
                            frect.Union(gi.GetBoundingBox().getWxRect())
                        if l_gi == bfab:
                            brect.Union(gi.GetBoundingBox().getWxRect())
                # Cross the graphics in *.Fab
                if frect.x1 is not None:
                    extra_ffab_lines.append(self.cross_module(m, frect, ffab))
                else:
                    extra_ffab_lines.append(None)
                if brect.x1 is not None:
                    extra_bfab_lines.append(self.cross_module(m, brect, bfab))
                else:
                    extra_bfab_lines.append(None)
        # Remmember the data used to undo it
        self.extra_ffab_lines = extra_ffab_lines
        self.extra_bfab_lines = extra_bfab_lines

    def uncross_modules(self, board, comps_hash):
        """ Undo the crosses in *.Fab layer """
        # Undo the drawings
        for m in board.GetModules():
            ref = m.GetReference()
            c = comps_hash.get(ref, None)
            if c and c.included and not c.fitted:
                restore = self.extra_ffab_lines.pop(0)
                if restore:
                    for line in restore:
                        m.Remove(line)
                restore = self.extra_bfab_lines.pop(0)
                if restore:
                    for line in restore:
                        m.Remove(line)

    def remove_paste_and_glue(self, board, comps_hash):
        """ Remove from solder paste layers the filtered components. """
        exclude = LSET()
        exclude.addLayer(board.GetLayerID('F.Paste'))
        exclude.addLayer(board.GetLayerID('B.Paste'))
        old_layers = []
        fadhes = board.GetLayerID('F.Adhes')
        badhes = board.GetLayerID('B.Adhes')
        old_fadhes = []
        old_badhes = []
        rescue = board.GetLayerID('Rescue')
        for m in board.GetModules():
            ref = m.GetReference()
            c = comps_hash.get(ref, None)
            if c and c.included and not c.fitted:
                # Remove all pads from *.Paste
                old_c_layers = []
                for p in m.Pads():
                    pad_layers = p.GetLayerSet()
                    old_c_layers.append(pad_layers.FmtHex())
                    pad_layers.removeLayerSet(exclude)
                    p.SetLayerSet(pad_layers)
                old_layers.append(old_c_layers)
                # Remove any graphical item in the *.Adhes layers
                for gi in m.GraphicalItems():
                    l_gi = gi.GetLayer()
                    if l_gi == fadhes:
                        gi.SetLayer(rescue)
                        old_fadhes.append(gi)
                    if l_gi == badhes:
                        gi.SetLayer(rescue)
                        old_badhes.append(gi)
        # Store the data to undo the above actions
        self.old_layers = old_layers
        self.old_fadhes = old_fadhes
        self.old_badhes = old_badhes
        self.fadhes = fadhes
        self.badhes = badhes
        return exclude

    def restore_paste_and_glue(self, board, comps_hash):
        for m in board.GetModules():
            ref = m.GetReference()
            c = comps_hash.get(ref, None)
            if c and c.included and not c.fitted:
                restore = self.old_layers.pop(0)
                for p in m.Pads():
                    pad_layers = p.GetLayerSet()
                    res = restore.pop(0)
                    pad_layers.ParseHex(res, len(res))
                    p.SetLayerSet(pad_layers)
        for gi in self.old_fadhes:
            gi.SetLayer(self.fadhes)
        for gi in self.old_badhes:
            gi.SetLayer(self.badhes)

    def run(self, output_dir, board):
        """ Makes the list of components available """
        if not self.dnf_filter and not self.variant:
            return
        load_sch()
        # Get the components list from the schematic
        comps = GS.sch.get_components()
        # Apply the filter
        reset_filters(comps)
        apply_fitted_filter(comps, self.dnf_filter)
        # Apply the variant
        if self.variant:
            # Apply the variant
            self.variant.filter(comps)
        self._comps = comps
