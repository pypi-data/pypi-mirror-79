# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "24/09/2019"


from silx.gui import qt


class ChooseDimensionDock(qt.QDockWidget):

    def __init__(self, parent=None):
        """
        Dock widget containing the ChooseDimensionWidget.
        """
        qt.QDockWidget.__init__(self, parent)
        self.widget = ChooseDimensionWidget()
        self.setWidget(self.widget)


class ChooseDimensionWidget(qt.QWidget):
    """
    Widget to choose a dimension from a dict and choose the value to filter
    the data. It can be included in other widget like StackView to filter the
    stack.
    """
    filterChanged = qt.Signal(int, int)
    stateDisabled = qt.Signal()

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)

        self.setLayout(qt.QGridLayout())
        dimensionLabel = qt.QLabel("Dimension: ")
        self._dimensionCB = qt.QComboBox()
        valueLabel = qt.QLabel("Value: ")
        self._valueCB = qt.QComboBox()
        self._checkbox = qt.QCheckBox("Filter by dimension", self)
        self._dimensionCB.setEnabled(0)
        self._valueCB.setEnabled(0)

        self.layout().addWidget(dimensionLabel, 0, 0, 1, 1)
        self.layout().addWidget(self._dimensionCB, 0, 1, 1, 1)
        self.layout().addWidget(valueLabel, 1, 0, 1, 1)
        self.layout().addWidget(self._valueCB, 1, 1, 1, 1)
        self.layout().addWidget(self._checkbox, 2, 1, 1, 1)

    def setDimensions(self, dimensions):
        """
        Function that fills the corresponeding comboboxes with the dimension's
        name and possible values.

        :param array_like dimensions: List of `darfix.core.dataset.Dimension`
                                      elements.
        """
        self._dimensionCB.clear()
        for dimension in dimensions:
            self._dimensionCB.insertItem(dimension[0], dimension[1].name)
        self.dimension = 0
        self.value = 0
        self._dimensionCB.setCurrentIndex(self.dimension)
        self.dimensions = dimensions
        self._valueCB.clear()
        for value in dimensions.get(self.dimension).unique_values:
            self._valueCB.addItem(str(value))
        self._dimensionCB.currentIndexChanged.connect(self._updateDimension)
        self._valueCB.currentIndexChanged.connect(self._updateValue)
        self._checkbox.stateChanged.connect(self._updateState)

    def _updateDimension(self, axis=-1):
        """
        Updates the selected dimension and set's the corresponding possible values.

        :param int axis: selected dimension's axis. (For now, the item position in
                         the combobox and the dimension's axis have to be the same).
        """
        if axis != -1 and axis is not None:
            self.dimension = axis
            self._valueCB.clear()
            for value in self.dimensions.get(self.dimension).unique_values:
                self._valueCB.addItem(str(value))
            self.filterChanged.emit(axis, 0)

    def _updateValue(self, index=None):
        """
        Updates the selected value.

        :param int index: selected value's index.
        """
        if index is not None:
            self.value = index
            self.filterChanged.emit(self.dimension, index)

    def _updateState(self, state):
        """
        Updates the state of the widget.

        :param bool state: If True, the widget emit's a signal
                    with the selected dimension and value. Else,
                    a disabled signal is emitted.

        """
        self._dimensionCB.setEnabled(state)
        self._valueCB.setEnabled(state)

        if state:
            self.filterChanged.emit(self.dimension, self.value)
        else:
            self.stateDisabled.emit()
