import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Resizable Text Boxes with Buttons')

        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        # Overall vertical layout: [Splitter] + [Buttons]
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 1. Create a splitter window
        splitter = wx.SplitterWindow(self)
        splitter.SetMinimumPaneSize(60)  # Minimum height for each pane

        # 2. Top readonly text box
        top_panel = wx.Panel(splitter)
        top_text = wx.TextCtrl(top_panel,
                               style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.VSCROLL | wx.TE_RICH2)
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer.Add(top_text, 1, wx.EXPAND)
        top_panel.SetSizer(top_sizer)

        # 3. Bottom editable text box
        bottom_panel = wx.Panel(splitter)
        bottom_text = wx.TextCtrl(bottom_panel,
                                  style=wx.TE_MULTILINE | wx.HSCROLL | wx.VSCROLL | wx.TE_RICH2)
        bottom_sizer = wx.BoxSizer(wx.VERTICAL)
        bottom_sizer.Add(bottom_text, 1, wx.EXPAND)
        bottom_panel.SetSizer(bottom_sizer)

        # 4. Split horizontally
        splitter.SplitHorizontally(top_panel, bottom_panel)
        vbox.Add(splitter, 1, wx.EXPAND)

        # 5. Button row
        btn_panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        for label in ['One', 'Two', 'Three', 'Four']:
            btn = wx.Button(btn_panel, label=label)
            hbox.Add(btn, 1, wx.EXPAND | wx.ALL, 5)
        btn_panel.SetSizer(hbox)
        vbox.Add(btn_panel, 0, wx.EXPAND)

        self.SetSizer(vbox)

        # Set window height to 85% of screen like before
        display_index = wx.Display.GetFromWindow(self)
        if display_index == -1:
            display_index = 0
        display = wx.Display(display_index)
        geometry = display.GetGeometry()
        width = 600
        height = int(geometry.GetHeight() * 0.85)
        self.SetSize(width, height)
        self.Centre()

        self.Show()


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        return True

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
