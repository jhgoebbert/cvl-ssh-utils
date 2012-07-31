#! /usr/bin/env python

# wx11vnc 0.2
# A graphical tool to set up a vnc server with x11vnc.

import wx
import os
import socket
import commands
from urllib2 import urlopen

ID_About = 100
ID_Exit = 101

class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(640,480),
                        style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.RESIZE_BOX | wx.MAXIMIZE_BOX))
       
        self.Center()
        self.CreateStatusBar()
        #self.SetStatusText("VNC Server")
        output = commands.getoutput('ps -A')
        if "x11vnc" in output:
            self.SetStatusText("Server Status: Running")
        else:
            self.SetStatusText("Server Status: Stopped")
        
        menuFile = wx.Menu()
        menuFile.Append(ID_Exit, "E&xit")
        
        menuHelp = wx.Menu()
        menuHelp.Append(ID_About, "&About")
        
        menu_bar = wx.MenuBar()
        menu_bar.Append(menuFile, "&File")
        menu_bar.Append(menuHelp, "&Help")
        self.SetMenuBar(menu_bar)
        
        wx.EVT_MENU(self, ID_Exit, self.onExit)
       
        self.notebookContainerPanel = wx.Panel(self, wx.ID_ANY)

        self.tabbed = wx.Notebook(self.notebookContainerPanel, wx.ID_ANY, style=(wx.NB_TOP))
        notebookContainerPanelSizer = wx.FlexGridSizer(rows=2, cols=3, vgap=15, hgap=15)
        notebookContainerPanelSizer.Add(wx.StaticText(self.notebookContainerPanel, wx.ID_ANY, "     "))
        notebookContainerPanelSizer.Add(self.tabbed, flag=wx.EXPAND)
        notebookContainerPanelSizer.Add(wx.StaticText(self.notebookContainerPanel, wx.ID_ANY, "     "))

        smallFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        smallFont.SetPointSize(11)

        # Connection tab

        self.connectionPanel = wx.Panel(self.tabbed, wx.ID_ANY)
        self.connectionPanelSizer = wx.FlexGridSizer(rows=1, cols=4, vgap=15, hgap=15)

        self.connectionLeftBorderPanel = wx.Panel(self.connectionPanel, wx.ID_ANY)
        self.connectionPanelSizer.Add(self.connectionLeftBorderPanel)

        self.connectionLeftPanel = wx.Panel(self.connectionPanel, wx.ID_ANY)
        self.connectionPanelSizer.Add(self.connectionLeftPanel, flag=wx.EXPAND)
        self.connectionLeftPanelSizer = wx.FlexGridSizer(rows=2, cols=1, vgap=5, hgap=5)

        self.connectionRightPanel = wx.Panel(self.connectionPanel, wx.ID_ANY)
        self.connectionPanelSizer.Add(self.connectionRightPanel, flag=wx.EXPAND)
        self.connectionRightPanelSizer = wx.FlexGridSizer(rows=4, cols=1, vgap=5, hgap=5)

        self.connectionRightBorderPanel = wx.Panel(self.connectionPanel, wx.ID_ANY)
        self.connectionPanelSizer.Add(self.connectionRightBorderPanel)

        # Encoding group box

        self.encodingPanel = wx.Panel(self.connectionLeftPanel, wx.ID_ANY)
        self.connectionLeftPanelSizer.Add(self.encodingPanel, flag=wx.EXPAND)

        self.encodingGroupBox = wx.StaticBox(self.encodingPanel, wx.ID_ANY, label="Encoding")
        self.encodingGroupBox.SetFont(smallFont)
        self.encodingGroupBoxSizer = wx.StaticBoxSizer(self.encodingGroupBox, wx.VERTICAL)
        self.encodingPanel.SetSizer(self.encodingGroupBoxSizer)

        self.innerEncodingPanel = wx.Panel(self.encodingPanel, wx.ID_ANY)
        self.innerEncodingPanelSizer = wx.FlexGridSizer(rows=10, cols = 1, vgap=5,hgap=5)
        self.innerEncodingPanel.SetSizer(self.innerEncodingPanelSizer)

        self.encodingMethodLabel = wx.StaticText(self.innerEncodingPanel, wx.ID_ANY, "Encoding method:")
        self.innerEncodingPanelSizer.Add(self.encodingMethodLabel)
        self.encodingMethodLabel.SetFont(smallFont)
        
        encodingMethods = ['Tight + Perceptually Lossless JPEG (LAN)', '???', '???', '???', '???']
        self.encodingMethodsComboBox = wx.Choice(self.innerEncodingPanel, wx.ID_ANY,
            choices=encodingMethods, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.encodingMethodsComboBox.SetFont(smallFont)
        self.innerEncodingPanelSizer.Add(self.encodingMethodsComboBox, flag=wx.EXPAND)

        self.jpegCompressionCheckBox = wx.CheckBox(self.innerEncodingPanel, wx.ID_ANY, "Allow JPEG compression")
        self.jpegCompressionCheckBox.SetValue(True)
        self.jpegCompressionCheckBox.SetFont(smallFont)
        self.innerEncodingPanelSizer.Add(self.jpegCompressionCheckBox)

        self.jpegChrominanceSubsamplingLabel = wx.StaticText(self.innerEncodingPanel, wx.ID_ANY, "JPEG chrominance subsampling:    None")
        self.jpegChrominanceSubsamplingLabel.SetFont(smallFont)
        self.innerEncodingPanelSizer.Add(self.jpegChrominanceSubsamplingLabel)

        self.jpegChrominanceSubsamplingSlider = wx.Slider(self.innerEncodingPanel, wx.ID_ANY, style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL)
        self.innerEncodingPanelSizer.Add(self.jpegChrominanceSubsamplingSlider)

        self.jpegImageQualityLabel = wx.StaticText(self.innerEncodingPanel, wx.ID_ANY, "JPEG image quality:    95")
        self.jpegImageQualityLabel.SetFont(smallFont)
        self.innerEncodingPanelSizer.Add(self.jpegImageQualityLabel)

        self.jpegImageQualitySlider = wx.Slider(self.innerEncodingPanel, wx.ID_ANY, style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL)
        self.innerEncodingPanelSizer.Add(self.jpegImageQualitySlider)

        self.zlibCompressionLevelLabel = wx.StaticText(self.innerEncodingPanel, wx.ID_ANY, "Zlib compression level:    1")
        self.zlibCompressionLevelLabel.Disable()
        self.zlibCompressionLevelLabel.SetFont(smallFont)
        self.innerEncodingPanelSizer.Add(self.zlibCompressionLevelLabel)

        self.zlibCompressionLevelSlider = wx.Slider(self.innerEncodingPanel, wx.ID_ANY, style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL)
        self.zlibCompressionLevelSlider.Disable()
        self.innerEncodingPanelSizer.Add(self.zlibCompressionLevelSlider)

        self.copyRectEncodingCheckBox = wx.CheckBox(self.innerEncodingPanel, wx.ID_ANY, "Allow CopyRect encoding")
        self.copyRectEncodingCheckBox.SetValue(True)
        self.copyRectEncodingCheckBox.SetFont(smallFont)
        self.innerEncodingPanelSizer.Add(self.copyRectEncodingCheckBox)

        self.innerEncodingPanel.SetSizerAndFit(self.innerEncodingPanelSizer)

        self.encodingGroupBoxSizer.Add(self.innerEncodingPanel, flag=wx.EXPAND)

        self.encodingPanel.SetSizerAndFit(self.encodingGroupBoxSizer)

        # Restrictions group box

        self.restrictionsPanel = wx.Panel(self.connectionLeftPanel, wx.ID_ANY)
        self.connectionLeftPanelSizer.Add(self.restrictionsPanel, flag=wx.EXPAND)

        self.restrictionsGroupBox = wx.StaticBox(self.restrictionsPanel, wx.ID_ANY, label="Restrictions")
        self.restrictionsGroupBox.SetFont(smallFont)
        self.restrictionsGroupBoxSizer = wx.StaticBoxSizer(self.restrictionsGroupBox, wx.VERTICAL)
        self.restrictionsPanel.SetSizer(self.restrictionsGroupBoxSizer)

        self.innerRestrictionsPanel = wx.Panel(self.restrictionsPanel, wx.ID_ANY)
        self.innerRestrictionsPanelSizer = wx.FlexGridSizer(rows=10, cols = 1, vgap=5,hgap=5)
        self.innerRestrictionsPanel.SetSizer(self.innerRestrictionsPanelSizer)

        self.viewOnlyCheckBox = wx.CheckBox(self.innerRestrictionsPanel, wx.ID_ANY, "View only (inputs ignored)")
        self.viewOnlyCheckBox.SetValue(False)
        self.innerRestrictionsPanelSizer.Add(self.viewOnlyCheckBox)
        self.viewOnlyCheckBox.SetFont(smallFont)
        
        self.disableClipboardTransferCheckBox = wx.CheckBox(self.innerRestrictionsPanel, wx.ID_ANY, "Disable clipboard transfer")
        self.disableClipboardTransferCheckBox.SetValue(False)
        self.innerRestrictionsPanelSizer.Add(self.disableClipboardTransferCheckBox)
        self.disableClipboardTransferCheckBox.SetFont(smallFont)
        
        self.innerRestrictionsPanel.SetSizerAndFit(self.innerRestrictionsPanelSizer)

        self.restrictionsGroupBoxSizer.Add(self.innerRestrictionsPanel, flag=wx.EXPAND)

        self.restrictionsPanel.SetSizerAndFit(self.restrictionsGroupBoxSizer)

        # Bottom border panel

        self.bottomBorderPanel = wx.Panel(self.connectionLeftPanel, wx.ID_ANY)
        self.connectionLeftPanelSizer.Add(self.bottomBorderPanel, flag=wx.EXPAND)

        # Display group box

        self.displayPanel = wx.Panel(self.connectionRightPanel, wx.ID_ANY)
        self.connectionRightPanelSizer.Add(self.displayPanel, flag=wx.EXPAND)

        self.displayGroupBox = wx.StaticBox(self.displayPanel, wx.ID_ANY, label="Display")
        self.displayGroupBox.SetFont(smallFont)
        self.displayGroupBoxSizer = wx.StaticBoxSizer(self.displayGroupBox, wx.VERTICAL)
        self.displayPanel.SetSizer(self.displayGroupBoxSizer)

        self.innerDisplayPanel = wx.Panel(self.displayPanel, wx.ID_ANY)
        self.innerDisplayPanelSizer = wx.FlexGridSizer(rows=10, cols = 1, vgap=5,hgap=5)
        self.innerDisplayPanel.SetSizer(self.innerDisplayPanelSizer)

        scaleOptions = ['100', '???', '???', '???', '???']
        self.scaleByComboBox = wx.Choice(self.innerDisplayPanel, wx.ID_ANY, choices=scaleOptions, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.scaleByComboBox.SetFont(smallFont)
        self.innerDisplayPanelSizer.Add(self.scaleByComboBox, flag=wx.EXPAND)

        self.doubleBufferingCheckBox = wx.CheckBox(self.innerDisplayPanel, wx.ID_ANY, "Double buffering")
        self.doubleBufferingCheckBox.SetValue(True)
        self.innerDisplayPanelSizer.Add(self.doubleBufferingCheckBox)
        self.doubleBufferingCheckBox.SetFont(smallFont)
        
        self.fullScreenModeCheckBox = wx.CheckBox(self.innerDisplayPanel, wx.ID_ANY, "Full-screen mode")
        self.fullScreenModeCheckBox.SetValue(False)
        self.innerDisplayPanelSizer.Add(self.fullScreenModeCheckBox)
        self.fullScreenModeCheckBox.SetFont(smallFont)
        
        spanModes = ['Automatic', '???', '???', '???', '???']
        self.spanModeComboBox = wx.Choice(self.innerDisplayPanel, wx.ID_ANY, choices=spanModes, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.spanModeComboBox.SetFont(smallFont)
        self.innerDisplayPanelSizer.Add(self.spanModeComboBox, flag=wx.EXPAND)

        self.deiconifyOnRemoteBellEventCheckBox = wx.CheckBox(self.innerDisplayPanel, wx.ID_ANY, "Deiconify on remote Bell event")
        self.deiconifyOnRemoteBellEventCheckBox.SetValue(False)
        self.innerDisplayPanelSizer.Add(self.deiconifyOnRemoteBellEventCheckBox)
        self.deiconifyOnRemoteBellEventCheckBox.SetFont(smallFont)
        
        self.innerDisplayPanel.SetSizerAndFit(self.innerDisplayPanelSizer)

        self.displayGroupBoxSizer.Add(self.innerDisplayPanel, flag=wx.EXPAND)

        self.displayPanel.SetSizerAndFit(self.displayGroupBoxSizer)

        # Mouse group box

        self.mousePanel = wx.Panel(self.connectionRightPanel, wx.ID_ANY)
        self.connectionRightPanelSizer.Add(self.mousePanel, flag=wx.EXPAND)

        self.mouseGroupBox = wx.StaticBox(self.mousePanel, wx.ID_ANY, label="Mouse")
        self.mouseGroupBox.SetFont(smallFont)
        self.mouseGroupBoxSizer = wx.StaticBoxSizer(self.mouseGroupBox, wx.VERTICAL)
        self.mousePanel.SetSizer(self.mouseGroupBoxSizer)

        self.innerMousePanel = wx.Panel(self.mousePanel)
        self.innerMousePanelSizer = wx.FlexGridSizer(rows=10, cols = 1, vgap=5,hgap=5)
        self.innerMousePanel.SetSizer(self.innerMousePanelSizer)

        self.emulate3ButtonsWith2ButtonClickCheckBox = wx.CheckBox(self.innerMousePanel, wx.ID_ANY, "Emulate 3 buttons (with 2-button click)")
        self.emulate3ButtonsWith2ButtonClickCheckBox.SetValue(True)
        self.innerMousePanelSizer.Add(self.emulate3ButtonsWith2ButtonClickCheckBox)
        self.emulate3ButtonsWith2ButtonClickCheckBox.SetFont(smallFont)
        
        self.swapMouseButtons2And3CheckBox = wx.CheckBox(self.innerMousePanel, wx.ID_ANY, "Swap mouse buttons 2 and 3")
        self.swapMouseButtons2And3CheckBox.SetValue(False)
        self.innerMousePanelSizer.Add(self.swapMouseButtons2And3CheckBox)
        self.swapMouseButtons2And3CheckBox.SetFont(smallFont)
        
        self.innerMousePanel.SetSizerAndFit(self.innerMousePanelSizer)

        self.mouseGroupBoxSizer.Add(self.innerMousePanel, flag=wx.EXPAND)

        self.mousePanel.SetSizerAndFit(self.mouseGroupBoxSizer)

        # Mouse cursor group box

        self.mouseCursorPanel = wx.Panel(self.connectionRightPanel, wx.ID_ANY)
        self.connectionRightPanelSizer.Add(self.mouseCursorPanel, flag=wx.EXPAND)

        self.mouseCursorGroupBox = wx.StaticBox(self.mouseCursorPanel, wx.ID_ANY, label="Mouse cursor")
        self.mouseCursorGroupBox.SetFont(smallFont)
        self.mouseCursorGroupBoxSizer = wx.StaticBoxSizer(self.mouseCursorGroupBox, wx.VERTICAL)
        self.mouseCursorPanel.SetSizer(self.mouseCursorGroupBoxSizer)

        self.innerMouseCursorPanel = wx.Panel(self.mouseCursorPanel, wx.ID_ANY)
        self.innerMouseCursorPanelSizer = wx.FlexGridSizer(rows=10, cols = 1, vgap=5,hgap=5)
        self.innerMouseCursorPanel.SetSizer(self.innerMouseCursorPanelSizer)

        self.trackRemoteCursorLocallyRadioButton = wx.RadioButton(self.innerMouseCursorPanel, wx.ID_ANY, "Track remote cursor locally")
        self.trackRemoteCursorLocallyRadioButton.SetValue(True)
        self.innerMouseCursorPanelSizer.Add(self.trackRemoteCursorLocallyRadioButton)
        self.trackRemoteCursorLocallyRadioButton.SetFont(smallFont)
        
        self.letRemoteServerDealWithMouseCursorRadioButton = wx.RadioButton(self.innerMouseCursorPanel, wx.ID_ANY, "Let remote server deal with mouse cursor")
        self.letRemoteServerDealWithMouseCursorRadioButton.SetValue(False)
        self.innerMouseCursorPanelSizer.Add(self.letRemoteServerDealWithMouseCursorRadioButton)
        self.letRemoteServerDealWithMouseCursorRadioButton.SetFont(smallFont)
        
        self.dontShowRemoteCursorRadioButton = wx.RadioButton(self.innerMouseCursorPanel, wx.ID_ANY, "Don't show remote cursor")
        self.dontShowRemoteCursorRadioButton.SetValue(False)
        self.innerMouseCursorPanelSizer.Add(self.dontShowRemoteCursorRadioButton)
        self.dontShowRemoteCursorRadioButton.SetFont(smallFont)
        
        self.innerMouseCursorPanel.SetSizerAndFit(self.innerMouseCursorPanelSizer)

        self.mouseCursorGroupBoxSizer.Add(self.innerMouseCursorPanel, flag=wx.EXPAND)

        self.mouseCursorPanel.SetSizerAndFit(self.mouseCursorGroupBoxSizer)

        # Connection panels

        self.connectionLeftPanel.SetSizerAndFit(self.connectionLeftPanelSizer)
        self.connectionRightPanel.SetSizerAndFit(self.connectionRightPanelSizer)
        self.connectionPanel.SetSizerAndFit(self.connectionPanelSizer)

        # Globals tab
        
        self.globalsPanel = wx.Panel(self.tabbed, wx.ID_ANY)
        self.tabbed.AddPage(self.connectionPanel, "Connection")
        self.tabbed.AddPage(self.globalsPanel, "Globals")
       
        # Buttons panel

        notebookContainerPanelSizer.Add(wx.StaticText(self.notebookContainerPanel, wx.ID_ANY, "     "))
        self.buttonsPanel = wx.Panel(self.notebookContainerPanel, wx.ID_ANY)
        notebookContainerPanelSizer.Add(self.buttonsPanel, flag=wx.ALIGN_RIGHT)
        notebookContainerPanelSizer.Add(wx.StaticText(self.notebookContainerPanel, wx.ID_ANY, "     "))

        okButton = wx.Button(self.buttonsPanel, wx.ID_ANY, "OK")
        cancelButton = wx.Button(self.buttonsPanel, wx.ID_ANY, "Cancel")
        
        buttonsPanelSizer = wx.FlexGridSizer(rows=2, cols=3, vgap=5, hgap=5)
        buttonsPanelSizer.Add(wx.StaticText(self.buttonsPanel, wx.ID_ANY, "     "))
        buttonsPanelSizer.Add(okButton)
        buttonsPanelSizer.Add(cancelButton)
        buttonsPanelSizer.Add(wx.StaticText(self.buttonsPanel, wx.ID_ANY, "     "))
        self.buttonsPanel.SetAutoLayout(True)
        self.buttonsPanel.SetSizerAndFit(buttonsPanelSizer) 

        # Button stays pressed, can't stop server
        okButton.Bind(wx.EVT_BUTTON, self.onOK)
        cancelButton.Bind(wx.EVT_BUTTON, self.onCancel)
     
        ###

        self.notebookContainerPanel.SetSizer(notebookContainerPanelSizer)

        self.Layout()

        
    def onExit(self, event):
        self.Close(True)
    
    def onOK(self, event):
        self.Close(True)
        
    def onCancel(self, event):
        self.Close(True)
        #import sys
        #sys.exit(0)


class wx11vnc(wx.App):
    def OnInit(self):
        frame = MainWindow(None, wx.ID_ANY, "TurboVNC Viewer Options")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = wx11vnc(0)
app.MainLoop()  

