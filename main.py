import scraper
import aplikacja


url = scraper.makeURL()
data = scraper.scrapeData(url)

scraper.saveDataToCSV(data)

root = aplikacja.tk.Tk()
app = aplikacja.CarViewerApp(root)
root.mainloop()
