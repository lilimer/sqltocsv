import mysql.connector
import wx
import wx.dataview as dv
import pandas as pd
from readconfig import readConfig


class App(wx.Frame):
    def __init__(self, parent, title):
        super(App, self).__init__(parent, title=title, size=(400, 200))

        self.db_config = readConfig()
        self.connection = self.connectToDB()
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.dvlc = dv.DataViewListCtrl(panel)
        self.dvlc.AppendToggleColumn('Export', width=50)
        self.dvlc.AppendTextColumn('Table Name', width=wx.COL_WIDTH_AUTOSIZE)
        self.loadTables()

        exportButton = wx.Button(panel, label='Export Selected to CSV')
        exportButton.Bind(wx.EVT_BUTTON, self.onExport)

        vbox.Add(self.dvlc, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        vbox.Add(exportButton, proportion=0, flag=wx.EXPAND|wx.ALL, border=10)

        panel.SetSizer(vbox)

    def connectToDB(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            if conn.is_connected():
                db_name = self.db_config.get('database')
                print(f"Connected to '{db_name}'")
                return conn
        except mysql.connector.Error as e:
            wx.LogError(f"Database connection failed: {e}")
            return None

    def loadTables(self):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            for table in cursor.fetchall():
                self.dvlc.AppendItem([False, table[0]])
            cursor.close()

    def onExport(self, event):
        selected_tables = [self.dvlc.GetTextValue(i, 1) for i in range(self.dvlc.GetItemCount()) if self.dvlc.GetToggleValue(i, 0)]
        if selected_tables:
            for table in selected_tables:
                self.exportToCsv(table)
            wx.LogMessage("Selected tables exported to CSV.")
        else:
            wx.LogWarning("No tables selected for export.")

    def exportToCsv(self, table_name):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                if not rows:
                    df = pd.DataFrame(columns=columns)
                else:
                    df = pd.DataFrame(rows, columns=columns)
                csv_file = f"{table_name}.csv"
                df.to_csv(f"output/{csv_file}", index=False)
                wx.LogMessage(f"Table '{table_name}' exported to {csv_file}")
            except Exception as e:
                wx.LogError(f"Error exporting table '{table_name}': {e}")
            finally:
                cursor.close()

    def onClose(self, event):
        if self.connection and self.connection.is_connected():
            self.connection.close()
        self.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    frame = App(None, "SQL to CSV Exporter")
    frame.Show()
    app.MainLoop()