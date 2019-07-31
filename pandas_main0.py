# -*- coding: utf-8 -*-
"""

@author: Yoonjun Kim
"""
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMenu, QApplication, QDialog
from PyQt5 import QtCore, QtWidgets
from UIpandas_gui0 import Ui_pandas_gui
from PyQt5 import QtGui
from basic_utils import is_number
from UIdialog_summary import Ui_Dialog_Summary
from UIdialog_about0 import Ui_Dialog_about
import pandas as pd

import sys
        
class AboutDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        # Set up the user interface from Designer.
        self.ui = Ui_Dialog_about()
        self.ui.setupUi(self)
        # Connect up the buttons.
        self.ui.pb_close_about.clicked.connect(self._about_close)

        self.setWindowTitle('About DataViewer')
        self.setWindowIcon(QtGui.QIcon('data_viewer.ico'))
    
    def _about_close(self):
         self.close()

class SummaryDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        # Set up the user interface from Designer.
        self.ui = Ui_Dialog_Summary()
        self.ui.setupUi(self)
        # Connect up the buttons.
        self.ui.pb_close_summary.clicked.connect(self._summary_close)

        df_summary = DM.df.describe()
        df_summary.reset_index(level=0, inplace=True) 
        #print(df_summary)        
        model = PandasModel(df_summary)
       
        self.ui.tv_summary.setModel(model)
        self.ui.tv_summary.resizeColumnsToContents()

        self.setWindowTitle('Data Summary')
        self.setWindowIcon(QtGui.QIcon('data_viewer.ico'))
    
    def _summary_close(self):
         self.close()

class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        #return len(self._data.values)
        return self._data.shape[0]
    
    def columnCount(self, parent=None):
        #return self._data.columns.size
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return_data = self._data.values[index.row()][index.column()]
                if is_number(str(return_data)):
                    try:
                        return str(round(return_data,3))
                    except (TypeError, ValueError):
                        return str(return_data)
                else:
                    return str(return_data)
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None

class PANDASGUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowIcon(QtGui.QIcon('data_viewer.ico'))
        self.ui = Ui_pandas_gui()
        self.ui.setupUi(self)
        self.input_filename = []
        self.command_filename = []
        self.pd_results = None
        self.key_min = None
        self.key_max = None
        self.pd_key = None

        self.df = pd.DataFrame() 
        self.cmd = ''
        self.cmd_select = ''
        self.lv_index = None
        self.ui.cbb_keyword.clear()
        self.ui.cbb_condition.clear()
        self.ui.cbb_condition.addItems(['==', '>', '>=', '<=', '<'])
        self.ui.cbb_criteria.clear()
        self.ui.cbb_condition2next.clear()
        self.ui.cbb_condition2next.addItems(['', '&', '|', 'Selected'])
        self.ui.cbb_number.clear()
        self.ui.cbb_number.addItems(['100', '50', '20', '10', '5'])
        self.ui.cbb_keyword_ls.clear()
        self.ui.rb_nhead.setChecked(True)
        self.ui.listw_listcommand.clear()
        self.ui.le_command.clear()
        
        self.ui.actionOpen.triggered.connect(lambda:self._open_file())
        self.ui.actionClose.triggered.connect(lambda:self._close_file())
        self.ui.actionData_Summary.triggered.connect(lambda:self._summary())
        self.ui.actionDATA_MINER_0_1.triggered.connect(lambda:self._about())
        self.ui.actionCSV_ALL_export.triggered.connect(lambda:self._export_all_csv())
        self.ui.actionCSV_Result_export.triggered.connect(lambda:self._export_result_csv(self.cmd))
        self.ui.actionCSV_import.triggered.connect(lambda:self._import_csv())
        self.ui.listw_listcommand.doubleClicked.connect(lambda:self._lw_dclick())
        self.ui.le_command.returnPressed.connect(lambda: self._le_return())
        self.ui.le_command.textChanged.connect(lambda: self._clear_statusbar()) 
        
        
        self.ui.pb_addtolist.clicked.connect(lambda:self._add_command(self.cmd))
        self.ui.pb_run.clicked.connect(lambda:self._run_command(self.cmd_select))
        self.ui.pb_clear_all_comm.clicked.connect(lambda:self._clear_all_command())
#        self.ui.cbb_keyword.currentIndexChanged.connect(lambda:self._criteria_max_min())
        self.ui.cbb_keyword.currentIndexChanged.connect(lambda:self._criteria_all())
        self.ui.cbb_condition2next.currentIndexChanged.connect(lambda:self._codition_select())
        self.ui.listw_listcommand.clicked.connect(self._on_listw_clicked)
        self.ui.listw_listcommand.customContextMenuRequested.connect(self._on_popup_listw)
        self.ui.tablev_output.customContextMenuRequested.connect(self._on_popup_output)
        self.ui.actionExit.triggered.connect(lambda:self.close())

         
        self.ui.cbb_condition2next.setDisabled(self.ui.listw_listcommand.count()==0)
        self.ui.pb_clear_all_comm.setDisabled(self.ui.listw_listcommand.count()==0)
        self.ui.pb_run.setDisabled(True)
        self.ui.menuExport.setDisabled(True)
        self.ui.pb_clear_all_comm.setDisabled(True)
        
        self.ui.cbb_keyword.setDisabled(True)
        self.ui.cbb_condition.setDisabled(True)
        self.ui.cbb_criteria.setDisabled(True)
        self.ui.cbb_number.setDisabled(True)
        self.ui.cbb_keyword_ls.setDisabled(True)
        self.ui.pb_addtolist.setDisabled(True)
        self.ui.rb_nhead.setDisabled(True)
        self.ui.rb_ntail.setDisabled(True)
        self.ui.rb_nlarge.setDisabled(True)
        self.ui.rb_nsmall.setDisabled(True)
        self.ui.menuSummary.setDisabled(True)
        self.ui.le_command.setDisabled(True)
        
        self.ui.actionOpen.setEnabled(True)
        self.ui.actionCSV_Result_export.setDisabled(True)
        self.ui.actionData_Summary.setDisabled(True)
        self.ui.actionCSV_import.setEnabled(True)
        
        self.ui.actionClose.setDisabled(True)
        
        
    def _criteria_all(self):
        import numpy as np
        
        self.ui.cbb_criteria.clear()
        
        current_key = self.ui.cbb_keyword.currentText()
        all_criteria = []
        if current_key:
            all_criteria = list(self.df[current_key].drop_duplicates(keep='first'))
            all_criteria = map(str, all_criteria)
            
            exec('DM.pd_key = DM.df[\'%s\'].dtype' %(str(self.ui.cbb_keyword.currentText())))
            if self.pd_key != np.float64 and self.pd_key != np.int64:
                all_criteria = ['\'' +el+ '\'' for el in all_criteria]
                
        self.ui.cbb_criteria.addItems(all_criteria)

    def _criteria_max_min(self): # replaced by _criteria_all(self)
        import numpy as np
        
        self.ui.cbb_criteria.clear()
        
        if(self.ui.cbb_keyword.currentText()):
            try:
                exec('DM.key_min = str(DM.df[\'%s\'].min())' %(str(self.ui.cbb_keyword.currentText())))
                exec('DM.key_max = str(DM.df[\'%s\'].max())' %(str(self.ui.cbb_keyword.currentText())))
            except (TypeError, ValueError):
                exec('DM.key_min = str(DM.df[\'%s\'][0])' %(str(self.ui.cbb_keyword.currentText())))
                exec('DM.key_max = str(DM.df[\'%s\'][len(DM.df[\'%s\'])-1])' %(str(self.ui.cbb_keyword.currentText()),str(self.ui.cbb_keyword.currentText())))

            exec('DM.pd_key = DM.df[\'%s\'].dtype' %(str(self.ui.cbb_keyword.currentText())))
            
            #print(self.pd_key)
            if self.pd_key != np.float64 and self.pd_key != np.int64:
                self.key_max = '\'' + self.key_max + '\''
                self.key_min = '\'' + self.key_min + '\''

        self.ui.cbb_criteria.addItems([self.key_min, self.key_max])
        
    def _open_file(self):
        
        self.input_filename, _ = QFileDialog.getOpenFileName(self, 'Open HDF5 File', '', 'HDF5 Files (*.h5)')

        if self.input_filename:
            self.df = pd.read_hdf(self.input_filename, 'table')
            column_list = list(self.df)
    
            self.ui.cbb_keyword.addItems(column_list)        
            self.ui.cbb_keyword_ls.addItems(column_list)
            
            self.ui.actionOpen.setDisabled(True)
            self.ui.menuImport.setDisabled(True)
    
            self.ui.cbb_keyword.setEnabled(True)
            self.ui.cbb_condition.setEnabled(True)
            self.ui.cbb_criteria.setEnabled(True)
            self.ui.cbb_number.setEnabled(True)
            self.ui.cbb_keyword_ls.setEnabled(True)
            self.ui.pb_addtolist.setEnabled(True)
            self.ui.rb_nhead.setEnabled(True)
            self.ui.rb_ntail.setEnabled(True)
            self.ui.rb_nlarge.setEnabled(True)
            self.ui.rb_nsmall.setEnabled(True)
            self.ui.menuExport.setEnabled(True)
            self.ui.menuALLExport.setEnabled(True)
            self.ui.menuResExport.setDisabled(True)
            self.ui.menuSummary.setEnabled(True)
            self.ui.le_command.setEnabled(True)
    
            self.ui.actionOpen.setDisabled(True)
            self.ui.actionCSV_Result_export.setDisabled(True)
            self.ui.actionData_Summary.setEnabled(True)
            self.ui.actionCSV_import.setDisabled(True)
            self.ui.actionMRG.setDisabled(True)
            self.ui.actionSEG.setDisabled(True)
            self.ui.actionELFINI_F41_ELEM.setDisabled(True)
            self.ui.actionELFINI_F41_DISPL.setDisabled(True)
            self.ui.actionPNT29B.setDisabled(True)
            self.ui.actionPCH_D.setDisabled(True)
            self.ui.actionPCH_S.setDisabled(True)
            self.ui.actionBDF.setDisabled(True)
            self.ui.actionClose.setEnabled(True)

            self.setWindowTitle('%s - DataViewer' %(self.input_filename))

            self._summary()
            
    def _close_file(self):

        self.input_filename = []
        self.pd_results = None

        self.df = pd.DataFrame() 
        self.cmd = ''
        self.cmd_select = ''
        self.lv_index = None
        self.ui.cbb_condition.clear()
        self.ui.cbb_condition.addItems(['==', '>', '>=', '<=', '<'])
        self.ui.cbb_criteria.clear()
        self.ui.cbb_condition2next.clear()
        self.ui.cbb_condition2next.addItems(['', '&', '|', 'Selected'])
        self.ui.cbb_number.clear()
        self.ui.cbb_number.addItems(['100', '50', '20', '10', '5'])
        self.ui.cbb_keyword.clear()
        self.ui.cbb_keyword_ls.clear()
        self.ui.rb_nhead.setChecked(True)
        self.ui.listw_listcommand.clear()
        self.ui.le_command.clear()
        
        model = PandasModel(self.df)
        self.ui.tablev_output.setModel(model)
        
        self.ui.actionOpen.setEnabled(True)
        self.ui.menuImport.setEnabled(True)
        self.ui.menuExport.setDisabled(True)
        self.ui.pb_clear_all_comm.setDisabled(True)

        self.ui.cbb_keyword.setDisabled(True)
        self.ui.cbb_condition.setDisabled(True)
        self.ui.cbb_criteria.setDisabled(True)
        self.ui.cbb_number.setDisabled(True)
        self.ui.cbb_keyword_ls.setDisabled(True)
        self.ui.pb_addtolist.setDisabled(True)
        self.ui.rb_nhead.setDisabled(True)
        self.ui.rb_ntail.setDisabled(True)
        self.ui.rb_nlarge.setDisabled(True)
        self.ui.rb_nsmall.setDisabled(True)
        self.ui.menuSummary.setDisabled(True)
        self.ui.le_command.setDisabled(True)


        self.ui.actionOpen.setEnabled(True)
        self.ui.actionCSV_Result_export.setDisabled(True)
        self.ui.actionData_Summary.setDisabled(True)
        self.ui.actionCSV_import.setEnabled(True)
        self.ui.actionMRG.setEnabled(True)
        self.ui.actionSEG.setEnabled(True)
        self.ui.actionELFINI_F41_ELEM.setEnabled(True)
        self.ui.actionELFINI_F41_DISPL.setEnabled(True)
        self.ui.actionPNT29B.setEnabled(True)
        self.ui.actionPCH_D.setEnabled(True)
        self.ui.actionPCH_S.setEnabled(True)
        self.ui.actionBDF.setEnabled(True)
        self.ui.actionClose.setDisabled(True)

        self.setWindowTitle('DataViewer')

    def pd_type(prev_command, var1, var2, var3, var4):
        command = "(df[\'%s\'] %s %s) %s " %(var1, var2, var3, var4)
        command = prev_command + command
        return command
    
    def _add_command(self, prev_command):
        import re
        
        var1 = str(self.ui.cbb_keyword.currentText())
        var2 = str(self.ui.cbb_condition.currentText())
        var3 = str(self.ui.cbb_criteria.currentText())
        var4 = str(self.ui.cbb_condition2next.currentText())
        if var4 != 'Selected':
            self.cmd = " %s (DM.df[\'%s\'] %s %s)" %(var4, var1, var2, var3)
        cmd_only = "(DM.df[\'%s\'] %s %s)" %(var1, var2, var3)

        #print(prev_command, self.cmd, cmd_only)
        if(var4 != ''):
            if prev_command.find(cmd_only)==-1 and var4 !='Selected':
                self.cmd = prev_command + self.cmd
            elif var4 =='Selected':
                self.cmd = prev_command
            else:
                self.cmd = prev_command

        command = re.search('(?<=^(\&|\|)).*', self.cmd.strip())
        if(command):
            self.cmd = command.group(0)
            
        num_lines = int(self.ui.cbb_number.currentText())
        keyword_ls = str(self.ui.cbb_keyword_ls.currentText())

        if(self.ui.rb_nlarge.isChecked()):
            pd_cmd = ("DM.df[%s].nlargest(%d,\'%s\')" %(self.cmd,num_lines,keyword_ls))
        elif(self.ui.rb_nsmall.isChecked()):
            pd_cmd = ("DM.df[%s].nsmallest(%d,\'%s\')" %(self.cmd,num_lines,keyword_ls))
        elif(self.ui.rb_nhead.isChecked()):
            pd_cmd = ("DM.df[%s].head(%d)" %(self.cmd,num_lines))
        elif(self.ui.rb_ntail.isChecked()):
            pd_cmd = ("DM.df[%s].tail(%d)" %(self.cmd,num_lines))

        self.ui.listw_listcommand.addItem(pd_cmd)
        self.ui.cbb_condition2next.setDisabled(True)
        self.ui.pb_clear_all_comm.setEnabled(self.ui.listw_listcommand.count()!=0)
        self.ui.pb_run.setDisabled(True)
        self.ui.pb_clear_all_comm.setEnabled(True)
                
    def _clear_all_command(self):
        self.ui.listw_listcommand.clear()
        self.ui.cbb_condition2next.setDisabled(self.ui.listw_listcommand.count()==0)
        self.ui.pb_run.setDisabled(True)
        self.ui.cbb_condition2next.setCurrentText('')
        
    def _run_command(self, command):

        self.pd_results = pd.DataFrame()
        model = PandasModel(self.pd_results)

        #print (command,self.cmd_select,'----')          
        try:    
            exec("DM.pd_results = %s" %(command))
        except (SyntaxError, AttributeError, TypeError, KeyError):
            self.ui.statusBar.showMessage('ERROR in PANDAS command. Check command in Selection List',5000)
            
        #print (self.pd_results)
                
        model = PandasModel(self.pd_results)
       
        self.ui.tablev_output.setModel(model)
        self.ui.tablev_output.resizeColumnsToContents()

        self.ui.pb_run.setDisabled(True)
        self.ui.cbb_condition2next.setDisabled(True)
        
        self.ui.menuResExport.setEnabled(True)

        self.ui.actionOpen.setDisabled(True)
        self.ui.actionCSV_Result_export.setEnabled(True)
        self.ui.actionData_Summary.setEnabled(True)
        self.ui.actionCSV_import.setDisabled(True)
        self.ui.actionMRG.setDisabled(True)
        self.ui.actionSEG.setDisabled(True)
        self.ui.actionELFINI_F41_ELEM.setDisabled(True)
        self.ui.actionELFINI_F41_DISPL.setDisabled(True)
        self.ui.actionPNT29B.setDisabled(True)
        self.ui.actionPCH_D.setDisabled(True)
        self.ui.actionPCH_S.setDisabled(True)
        self.ui.actionBDF.setDisabled(True)
        self.ui.actionClose.setEnabled(True)

    def _on_listw_clicked(self, index):
        import re
        
        self.cmd_select = ''
        self.cmd_select = index.data()
        command = re.search('(?<=\.df\[).*?(?=\]\.(head|tail|nsmall|nlarg))',self.cmd_select)
        if(command):
            self.cmd = command.group(0)
            
        self.lv_index = index

        self.ui.pb_run.setEnabled(True)
        self.ui.cbb_condition2next.setEnabled(True)

        #print(self.cmd, self.cmd_select)
        
    def _on_popup_listw(self, pos):
        import io
        
        menu = QMenu()
        selectAction = menu.addAction('Select / Sort Option')
        andAction = menu.addAction('And ...')
        orAction = menu.addAction('OR ...')
        menu.addSeparator()
        runAction = menu.addAction('Run Selected')
        menu.addSeparator()
        copyAction = menu.addAction('Copy to Clipboard')
        deleteAction = menu.addAction('Delete')
        menu.addSeparator()
        loadAction = menu.addAction('Import Custom Commands')
        saveAction = menu.addAction('Save Custom Commands')
        
        action = menu.exec_(self.ui.listw_listcommand.mapToGlobal(pos))
        if(action == deleteAction):
            self.ui.listw_listcommand.takeItem(self.lv_index.row())
            self.ui.cbb_condition2next.setDisabled(self.ui.listw_listcommand.count()==0)
            self.ui.pb_clear_all_comm.setDisabled(self.ui.listw_listcommand.count()==0)
            self.ui.pb_run.setDisabled(self.ui.listw_listcommand.count()==0)
            if self.ui.listw_listcommand.count()==0:
                    self.ui.cbb_condition2next.setCurrentText('')
        elif(action == runAction):
            self._run_command(self.cmd_select)
        elif(action == copyAction):
            selection = self.ui.listw_listcommand.selectedItems()
            if selection:
                stream = io.StringIO()
                stream.write(self.cmd_select)
                QApplication.clipboard().setText(stream.getvalue())
        elif(action == selectAction):
            self.ui.cbb_condition2next.setCurrentText('Selected')
        elif(action == andAction):
            self.ui.cbb_condition2next.setCurrentText('&')
        elif(action == orAction):
            self.ui.cbb_condition2next.setCurrentText('|')
        elif(action == loadAction):
            self.command_filename, _ = QFileDialog.getOpenFileName(self, 'Open Command File', '', 'TEXT File (*.txt)')
            with open(self.command_filename) as command_f:
                command_data = command_f.read()
                command_data = command_data.split('\n')
                map(str.strip, command_data)
                command_data = list(filter(None,command_data))
                self.ui.listw_listcommand.addItems(command_data)
                
        elif(action == saveAction):
            dlg = QFileDialog()
            dlg.AnyFile
            self.command_filename, _ = dlg.getSaveFileName(self, 'Open Command File', '', 'TEXT File (*.txt)')

            with open(self.command_filename,'w') as command_f:
                for index in range(self.ui.listw_listcommand.count()):
                    command_f.write(self.ui.listw_listcommand.item(index).text()+'\n')
#                
    def _on_popup_output(self, pos):
        import io
        import csv
        
        menu = QMenu()
        copyAction = menu.addAction('Copy to Clipboard')
        action = menu.exec_(self.ui.tablev_output.mapToGlobal(pos))
        if(action == copyAction):
            selection = self.ui.tablev_output.selectedIndexes()
            if selection:
                rows = sorted(index.row() for index in selection)
                columns = sorted(index.column() for index in selection)
                rowcount = rows[-1] - rows[0] + 1
                colcount = columns[-1] - columns[0] + 1
                table = [[''] * colcount for _ in range(rowcount)]

                for index in selection:
                    row = index.row() - rows[0]
                    column = index.column() - columns[0]
                    table[row][column] = index.data()

                table.insert(0,list(self.pd_results))
                table.insert(0,[self.cmd_select])
                table.insert(0,[self.input_filename])
                stream = io.StringIO()
                csv.writer(stream, delimiter='\t').writerows(table)
                #print(table)
                QApplication.clipboard().setText(stream.getvalue())

    def _export_all_csv(self):
        dlg = QFileDialog()
        dlg.AnyFile
        self.input_filename, _ = dlg.getSaveFileName(self, 'Save CSV File', '', 'CSV File (*.csv)')
        
        if self.input_filename:
            self.df.to_csv(self.input_filename, index=False)

    def _export_result_csv(self, command):
                
        if(command):
            command = ("DM.df[%s]" %(command))
            
            try:    
                exec("DM.pd_results = %s" %(command))
            except (SyntaxError, AttributeError, TypeError):
                self.ui.statusBar.showMessage('ERROR in PANDAS command. Check command in Selection List',5000)
            
            #print (command)
                
            dlg = QFileDialog()
            dlg.AnyFile
            self.input_filename, _ = dlg.getSaveFileName(self, 'Save CSV File', '', 'CSV File (*.csv)')
    
            if self.input_filename:
                self.pd_results.to_csv(self.input_filename, index=False)

    def _import_csv(self):
        self.input_filename, _ = QFileDialog.getOpenFileName(self, 'Open CSV File', '', 'CSV File (*.csv)')

        if self.input_filename:

            self.df = pd.read_csv(self.input_filename)
            column_list = list(self.df)
    
            self.ui.cbb_keyword.addItems(column_list)        
            self.ui.cbb_keyword_ls.addItems(column_list)
        
            self.ui.actionOpen.setDisabled(True)
            self.ui.menuImport.setDisabled(True)
            self.ui.cbb_keyword.setEnabled(True)
            self.ui.cbb_condition.setEnabled(True)
            self.ui.cbb_criteria.setEnabled(True)
            self.ui.cbb_number.setEnabled(True)
            self.ui.cbb_keyword_ls.setEnabled(True)
            self.ui.pb_addtolist.setEnabled(True)
            self.ui.rb_nhead.setEnabled(True)
            self.ui.rb_ntail.setEnabled(True)
            self.ui.rb_nlarge.setEnabled(True)
            self.ui.rb_nsmall.setEnabled(True)
            self.ui.menuExport.setEnabled(True)
            self.ui.menuALLExport.setEnabled(True)
            self.ui.menuResExport.setDisabled(True)
            self.ui.menuSummary.setEnabled(True)
            self.ui.le_command.setEnabled(True)
    
            self.setWindowTitle('%s - DataViewer' %(self.input_filename))
            self._summary()

            self.ui.actionOpen.setDisabled(True)
            self.ui.actionCSV_Result_export.setDisabled(True)
            self.ui.actionData_Summary.setEnabled(True)
            self.ui.actionCSV_import.setDisabled(True)
            self.ui.actionMRG.setDisabled(True)
            self.ui.actionSEG.setDisabled(True)
            self.ui.actionELFINI_F41_ELEM.setDisabled(True)
            self.ui.actionELFINI_F41_DISPL.setDisabled(True)
            self.ui.actionPNT29B.setDisabled(True)
            self.ui.actionPCH_D.setDisabled(True)
            self.ui.actionPCH_S.setDisabled(True)
            self.ui.actionBDF.setDisabled(True)
            self.ui.actionClose.setEnabled(True)
    
    def _codition_select(self):
        if self.ui.cbb_condition2next.currentText() == 'Selected':
            self.ui.cbb_keyword.setDisabled(True)
            self.ui.cbb_condition.setDisabled(True)
            self.ui.cbb_criteria.setDisabled(True)    
        else:
            self.ui.cbb_keyword.setEnabled(True)
            self.ui.cbb_condition.setEnabled(True)
            self.ui.cbb_criteria.setEnabled(True) 
            
    def _summary(self):
        self.dialog_summary = SummaryDialog()
        self.dialog_summary.show()

    def _about(self):
        self.dialog_about = AboutDialog()
        self.dialog_about.show()
        
    def _lw_dclick(self):
        self.ui.le_command.setText(self.cmd_select)
        
    def _le_return(self):

        pd_cmd = self.ui.le_command.text().strip()
        
        if(pd_cmd):
            self.ui.listw_listcommand.addItem(pd_cmd)
            self.ui.cbb_condition2next.setDisabled(True)
            self.ui.pb_clear_all_comm.setEnabled(self.ui.listw_listcommand.count()!=0)
            self.ui.pb_run.setDisabled(True)
            self.ui.pb_clear_all_comm.setEnabled(True)

    def _clear_statusbar(self):
        self.ui.statusBar.showMessage('')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DM = PANDASGUI()
    DM.setWindowTitle('DataViewer')

    DM.show()
    sys.exit(app.exec_())
