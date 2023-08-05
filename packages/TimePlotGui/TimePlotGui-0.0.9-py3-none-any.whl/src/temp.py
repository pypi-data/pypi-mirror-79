    def set_local_ft_mode(self):
        """starts or stops the local FT mode depending on local fourier checkbox
        state
        """
        if self.menu.local_fourier_checkbox.isChecked():
            for dataitem in self.data_table.values():
                dataitem.start_local_ft_mode()
                print('%%%%%% started local fourier mode')
        else:
            for dataitem in self.data_table.values():
                dataitem.stop_local_ft_mode()
                print('%%%%%% stopped local fourier mode')
        return


#490
    local_fourier = QtGui.QWidgetAction(self.menu)
    local_fourier_checkbox = QtGui.QCheckBox("Local Fourier Transform", self)
    local_fourier.setDefaultWidget(local_fourier_checkbox)
    local_fourier_checkbox.stateChanged.connect(self.set_local_ft_mode)
    self.menu.addAction(local_fourier)
    self.menu.local_fourier = local_fourier
    self.menu.local_fourier_checkbox = local_fourier_checkbox


#1100
    def start_local_ft_mode(self):
        self.pdi.start_local_ft_mode()

    def stop_local_ft_mode(self):
        self.pdi.stop_local_ft_mode()
#tpdi
    def __init__(self, id_nr=0, absolute_time=None):
        self.id_nr = id_nr
        self.data_name = self._compose_data_name()
        self.pdi = PlotDataItemV2([],[])
        if absolute_time == None:
            self.absolute_time = time.time()
        else:
            self.absolute_time = absolute_time

    def _compose_data_name(self):
        return TimePlotDataItem.DATA_NAME.format(self.id_nr)

    def reset_absolute_time(self, absolute_time):
        self.absolute_time = absolute_time

    def get_plot_data_item(self):
        """returns the pg.PlotDataItem"""
        return self.pdi

    def add_value(self, val, time_val):
        """adds value to pg.PlotDataItem data array"""
        t, y = self.pdi.getData()
        t = np.append(t, time_val - self.absolute_time)
        y = np.append(y, val)
        self.pdi.setData(t,y)
