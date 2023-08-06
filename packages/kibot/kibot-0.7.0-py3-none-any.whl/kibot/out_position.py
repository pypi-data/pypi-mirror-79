# -*- coding: utf-8 -*-
# Copyright (c) 2020 Salvador E. Tropea
# Copyright (c) 2020 Instituto Nacional de Tecnología Industrial
# Copyright (c) 2019 Romain Deterre (@rdeterre)
# License: GPL-3.0
# Project: KiBot (formerly KiPlot)
# Adapted from: https://github.com/johnbeard/kiplot/pull/10
import operator
from datetime import datetime
from pcbnew import (IU_PER_MM, IU_PER_MILS)
from .gs import GS
from .misc import UI_SMD, UI_VIRTUAL
from .out_base import VariantOptions
from .macros import macros, document, output_class  # noqa: F401
from . import log

logger = log.get_logger(__name__)


class PositionOptions(VariantOptions):
    def __init__(self):
        with document:
            self.format = 'ASCII'
            """ [ASCII,CSV] format for the position file """
            self.separate_files_for_front_and_back = True
            """ generate two separated files, one for the top and another for the bottom """
            self.only_smd = True
            """ only include the surface mount components """
            self.output = GS.def_global_output
            """ output file name (%i='top_pos'|'bottom_pos'|'both_pos', %x='pos'|'csv') """
            self.units = 'millimeters'
            """ [millimeters,inches] units used for the positions """
        super().__init__()

    def _do_position_plot_ascii(self, board, output_dir, columns, modulesStr, maxSizes):
        topf = None
        botf = None
        bothf = None
        if self.separate_files_for_front_and_back:
            topf = open(self.expand_filename(output_dir, self.output, 'top_pos', 'pos'), 'w')
            botf = open(self.expand_filename(output_dir, self.output, 'bottom_pos', 'pos'), 'w')
        else:
            bothf = open(self.expand_filename(output_dir, self.output, 'both_pos', 'pos'), 'w')

        files = [f for f in [topf, botf, bothf] if f is not None]
        for f in files:
            f.write('### Module positions - created on {} ###\n'.format(datetime.now().strftime("%a %d %b %Y %X %Z")))
            f.write('### Printed by KiBot\n')
            unit = {'millimeters': 'mm', 'inches': 'in'}[self.units]
            f.write('## Unit = {}, Angle = deg.\n'.format(unit))

        if topf is not None:
            topf.write('## Side : top\n')
        if botf is not None:
            botf.write('## Side : bottom\n')
        if bothf is not None:
            bothf.write('## Side : both\n')

        for f in files:
            f.write('# ')
            for idx, col in enumerate(columns):
                if idx > 0:
                    f.write("   ")
                f.write("{0: <{width}}".format(col, width=maxSizes[idx]))
            f.write('\n')

        # Account for the "# " at the start of the comment column
        maxSizes[0] = maxSizes[0] + 2

        for m in modulesStr:
            fle = bothf
            if fle is None:
                if m[-1] == "top":
                    fle = topf
                else:
                    fle = botf
            for idx, col in enumerate(m):
                if idx > 0:
                    fle.write("   ")
                fle.write("{0: <{width}}".format(col, width=maxSizes[idx]))
            fle.write("\n")

        for f in files:
            f.write("## End\n")

        if topf is not None:
            topf.close()
        if botf is not None:
            botf.close()
        if bothf is not None:
            bothf.close()

    def _do_position_plot_csv(self, board, output_dir, columns, modulesStr):
        topf = None
        botf = None
        bothf = None
        if self.separate_files_for_front_and_back:
            topf = open(self.expand_filename(output_dir, self.output, 'top_pos', 'csv'), 'w')
            botf = open(self.expand_filename(output_dir, self.output, 'bottom_pos', 'csv'), 'w')
        else:
            bothf = open(self.expand_filename(output_dir, self.output, 'both_pos', 'csv'), 'w')

        files = [f for f in [topf, botf, bothf] if f is not None]

        for f in files:
            f.write(",".join(columns))
            f.write("\n")

        for m in modulesStr:
            fle = bothf
            if fle is None:
                if m[-1] == "top":
                    fle = topf
                else:
                    fle = botf
            fle.write(",".join('"{}"'.format(e) for e in m))
            fle.write("\n")

        if topf is not None:
            topf.close()
        if botf is not None:
            botf.close()
        if bothf is not None:
            bothf.close()

    def run(self, output_dir, board):
        super().run(output_dir, board)
        columns = ["Ref", "Val", "Package", "PosX", "PosY", "Rot", "Side"]
        colcount = len(columns)
        # Note: the parser already checked the units are milimeters or inches
        conv = 1.0
        if self.units == 'millimeters':
            conv = 1.0 / IU_PER_MM
        else:  # self.units == 'inches':
            conv = 0.001 / IU_PER_MILS
        # Format all strings
        comps_hash = self.get_refs_hash()
        modules = []
        for m in sorted(board.GetModules(), key=operator.methodcaller('GetReference')):
            ref = m.GetReference()
            # Apply any filter or variant data
            if comps_hash:
                c = comps_hash.get(ref, None)
                if c and (not c.fitted or not c.included):
                    continue
            # If passed check the position options
            if (self.only_smd and m.GetAttributes() == UI_SMD) or \
               (not self.only_smd and m.GetAttributes() != UI_VIRTUAL):
                center = m.GetCenter()
                # See PLACE_FILE_EXPORTER::GenPositionData() in
                # export_footprints_placefile.cpp for C++ version of this.
                modules.append([
                    "{}".format(ref),
                    "{}".format(m.GetValue()),
                    "{}".format(m.GetFPID().GetLibItemName()),
                    "{:.4f}".format(center.x * conv),
                    "{:.4f}".format(-center.y * conv),
                    "{:.4f}".format(m.GetOrientationDegrees()),
                    "{}".format("bottom" if m.IsFlipped() else "top")
                ])

        # Find max width for all columns
        maxlengths = [0] * colcount
        for row in range(len(modules)):
            for col in range(colcount):
                maxlengths[col] = max(maxlengths[col], len(modules[row][col]))

        # Note: the parser already checked the format is ASCII or CSV
        if self.format == 'ASCII':
            self._do_position_plot_ascii(board, output_dir, columns, modules, maxlengths)
        else:  # if self.format == 'CSV':
            self._do_position_plot_csv(board, output_dir, columns, modules)


@output_class
class Position(BaseOutput):  # noqa: F821
    """ Pick & place
        Generates the file with position information for the PCB components, used by the pick and place machine.
        This output is what you get from the 'File/Fabrication output/Footprint poistion (.pos) file' menu in pcbnew. """
    def __init__(self):
        super().__init__()
        with document:
            self.options = PositionOptions
            """ [dict] Options for the `position` output """
