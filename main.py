import wx

class MyFrame(wx.Frame):
     def __init__(self):
        super().__init__(parent=None, title='Simple wxPython App')

        # Get display where the window is opening
        display_index = wx.Display.GetFromWindow(self)
        if display_index == -1:
            display_index = 0  # fallback to primary monitor

        display = wx.Display(display_index)
        geometry = display.GetGeometry()

        width = 600
        height = int(geometry.GetHeight() * 0.85)  # leave space for taskbar etc.

        # Resize the frame after creating it
        self.SetSize(width, height)
        self.Centre()

        # Background color
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
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