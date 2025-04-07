import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Simple wxPython App', size=(400, 200))
        
        panel = wx.Panel(self)

        # Layout manager
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Top text box
        self.text_top = wx.TextCtrl(panel, style=wx.TE_LEFT)
        vbox.Add(self.text_top, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)

        # Slightly smaller text box
        self.text_mid = wx.TextCtrl(panel, size=(-1, 25), style=wx.TE_LEFT)
        vbox.Add(self.text_mid, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10, proportion=0)

        # Row of four buttons
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        for label in ['One', 'Two', 'Three', 'Four']:
            btn = wx.Button(panel, label=label)
            hbox.Add(btn, flag=wx.RIGHT, border=10)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame()
        return True

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()