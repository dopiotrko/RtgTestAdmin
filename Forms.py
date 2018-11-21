import wx
import wx.grid as gridlib
import urllib.request
from io import BytesIO
from Answer import Answer
from RTG import RTG
from database import Database

Database.initialise(user='jagxthtr',
                    password='puasVa9LZh0D58Dy7Z-h8VdmCppGNbko',
                    database='jagxthtr',
                    host='baasu.db.elephantsql.com',
                    port=5432)
answers = Answer.open_from_db()
current_choice = 0


########################################################################
class LeftPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        #answers = Answer.open_from_db()
        grid = gridlib.Grid(self)
        grid.CreateGrid(len(answers), 4)
        grid.SetRowLabelSize(30)
        grid.SetColLabelValue(0, "Imię")
        grid.SetColLabelValue(1, "Nazwisko")
        grid.SetColLabelValue(2, "email")
        grid.SetColLabelValue(3, "Czas testu")
        for i, answer in enumerate(answers):
            grid.SetCellValue(i, 0, answer.name)
            grid.SetCellValue(i, 1, answer.surname)
            grid.SetCellValue(i, 2, answer.email)
            grid.SetCellValue(i, 3, str(answer.time))
        grid.SetColSize(2, 120)
        grid.Bind(gridlib.EVT_GRID_SELECT_CELL, parent.parent.on_select)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 0, wx.EXPAND)
        self.SetSizer(sizer)


########################################################################
class ImgPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        self.rtg_url = "http://www.rtgobrazki.ugu.pl/bialy.jpg"
        self.show_img(self.rtg_url)

    def show_img(self, rtg_url):
        self.rtg_url = rtg_url
        with urllib.request.urlopen(self.rtg_url) as url:
            buf = url.read()
        sbuf = BytesIO(buf)
        image = wx.Image(sbuf).ConvertToBitmap()
        wx.StaticBitmap(self, -1, image)


########################################################################


class RightPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        self.txt = wx.StaticText(self)

        self.img_panel = ImgPanel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.img_panel, 0, wx.EXPAND)
        sizer.Add(self.txt, 0, wx.EXPAND)
        self.SetSizer(sizer)


########################################################################
class MySplitterWindow(wx.SplitterWindow):
    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent)
        self.parent = parent


class MyForm(wx.Frame):

    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, title="RTG Test - przeglądarka odpopwiedzi", size=wx.Size(900, 900))

        self.menuBar = wx.MenuBar()
        add_menu = wx.Menu()
        add_item = add_menu.Append(wx.ID_ABOUT, 'Dodaj obraz do bazy danych')#, 'About')
        self.Bind(wx.EVT_MENU, self.on_add, add_item)
        self.menuBar.Append(add_menu, '&Dodaj')

        self.SetMenuBar(self.menuBar)

        self.answer = ""
        splitter = MySplitterWindow(self)
        self.leftP = LeftPanel(splitter)
        self.rightP = RightPanel(splitter)

        # split the window
        splitter.SplitVertically(self.leftP, self.rightP)
        splitter.SetSashPosition(420, False)
        splitter.SetSashInvisible(False)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def on_add(self, event):
        myframe = wx.Frame(None, -1, 'win.py')
        myframe.SetSize(200, 50)

        # Create text input
        dlg = wx.TextEntryDialog(myframe, 'Dodaj obraz do bazy danych, '
                                        'Upewnij się że wpisujesz poprawny adres URL do pliku',
                                        'Dodaj obraz')
        dlg.SetValue("")
        if dlg.ShowModal() == wx.ID_OK:
            RTG(dlg.GetValue()).save_to_db()
            print('You entered: %s\n' % dlg.GetValue())
        dlg.Destroy()

    def on_select(self, event):
        row = event.GetRow()
        try:
            self.rightP.img_panel.show_img('http://www.rtgobrazki.ugu.pl/bialy.jpg')
            self.rightP.img_panel.show_img(answers[row].rtg_url)
        except urllib.error.HTTPError:
            self.answer ="\nERROR: Nie znaleziono pliku"
        else:
            self.answer = "Wyświetla odpowiedż dla studenta o Nr:" \
                 + str(row + 1) + " - " \
                 + answers[row].name + " " \
                 + answers[row].surname + ".\nOdp:" \
                 + answers[row].answer
        self.rightP.txt.SetLabelText(self.answer)


# ----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()
