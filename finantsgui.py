from tkinter import *
from tkinter import ttk, messagebox
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches
from matplotlib.figure import Figure
#############################################
#TODO
############################################
#pie chart - lisamisel paned juurde tag'i ja siis ta salvestab pie charti,
# kui tühi siis läheb muu alla

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Finantstabel 2019').sheet1

kuu = '.02'


def lisatulu(tulunr, tulu_nime_input, tulu_kuup2eva_input, tulu_summa_input):
	lisatulu1 = sheet.update_cell((tulunr+1), 4, tulu_nime_input)
	lisatulu2 = sheet.update_cell((tulunr+1), 5, tulu_kuup2eva_input)
	lisatulu3 = sheet.update_cell((tulunr+1), 6, tulu_summa_input)

def lisakulu(kulunr, kulu_nime_input, kulu_kuup2eva_input, kulu_summa_input):
	lisakulu1 = sheet.update_cell((kulunr+1), 1, kulu_nime_input)
	lisakulu2 = sheet.update_cell((kulunr+1), 2, kulu_kuup2eva_input)
	lisakulu3 = sheet.update_cell((kulunr+1), 3, kulu_summa_input)

def mainbackend():

	kogukulu = 0
	kogutulu = 0
	autokuluplot = 0
	kodukuluplot = 0
	muukuluplot = 0
	selfkuluplot = 0
	söökkuluplot = 0
	riidedkuluplot = 0

	kulu_nimi = sheet.col_values(1)
	kulu_kuup2ev = sheet.col_values(2)
	kulu_summa = sheet.col_values(3)
	kulutused_list = []
	kulunr = 0

	tulu_nimi = sheet.col_values(4)
	tulu_kuup2ev = sheet.col_values(5)
	tulu_summa = sheet.col_values(6)
	tulu_list = []
	tulunr = 0

	for i in range(len(kulu_nimi)):
		subkulutused = []
		subkulutused.append((kulu_nimi[i], kulu_kuup2ev[i], kulu_summa[i]))
		kulutused_list.append(subkulutused)
		kogukulu = round((kogukulu + float(kulu_summa[i])),2)
		kulunr +=1

	for i in range((len(tulu_nimi))):
		subtulu = []
		subtulu.append((tulu_nimi[i], tulu_kuup2ev[i], tulu_summa[i]))
		tulu_list.append(subtulu)
		kogutulu = round((kogutulu + float(tulu_summa[i])), 2)
		tulunr +=1

	for p in range(len(kulu_nimi)):
		if 'söök' in kulu_nimi[p]:
			söökkuluplot = söökkuluplot + float(kulu_summa[p])
		elif 'kodu' in kulu_nimi[p]:
			kodukuluplot = kodukuluplot + float(kulu_summa[p])
		elif 'self' in kulu_nimi[p]:
			selfkuluplot = selfkuluplot + float(kulu_summa[p])
		elif 'auto' in kulu_nimi[p]:
			autokuluplot = autokuluplot + float(kulu_summa[p])
		elif 'riided' in kulu_nimi[p]:
			riidedkuluplot = riidedkuluplot + float(kulu_summa[p])
		elif 'muu' in kulu_nimi[p]:
			muukuluplot = muukuluplot + float(kulu_summa[p])
		else:
			muukuluplot = muukuluplot + float(kulu_summa[p])


	k2ive = kogutulu + kogukulu
	hetkeseis = kogutulu - kogukulu
	return	tulu_nimi, kulu_nimi, kulu_kuup2ev, tulu_kuup2ev, tulunr, kulunr, tulu_summa, kulu_summa, kogutulu, kogukulu, k2ive, hetkeseis, söökkuluplot, kodukuluplot, muukuluplot, selfkuluplot, autokuluplot, riidedkuluplot

tulu_nimi, kulu_nimi, kulu_kuup2ev, tulu_kuup2ev, tulunr, kulunr, tulu_summa, kulu_summa, kogutulu, kogukulu, k2ive, hetkeseis, söökkuluplot, kodukuluplot, muukuluplot, selfkuluplot, autokuluplot, riidedkuluplot = mainbackend()

def tkinteraken():

	def salvesta():
		if kuluvoitulu_entry.get() == 'kulu':
			lisakulu(kulunr, nimi_entry.get(), kuup2ev_entry.get(), summa_entry.get())
			# tree1.insert('', 'end', text=nimi_entry.get(),
			# 			 values=((kuup2ev_entry.get() + kuu), (summa_entry.get() + '€')))
			# kuluvoitulu_entry.delete(0, 'end')
			# nimi_entry.delete(0, 'end')
			# kuup2ev_entry.delete(0, 'end')
			# summa_entry.delete(0, 'end')
			# kuluvoitulu_entry.focus()
			tkinteraken()


		elif kuluvoitulu_entry.get() == 'tulu':
			lisatulu(tulunr, nimi_entry.get(), kuup2ev_entry.get(), summa_entry.get())
			# tree2.insert('', 'end', text=nimi_entry.get(), values=((kuup2ev_entry.get() + kuu), (summa_entry.get() + '€')))
			# koguvahe_label.configure(text=float(kogukulu-kogutulu-summa_entry.get()))
			# kuluvoitulu_entry.delete(0, 'end')
			# nimi_entry.delete(0, 'end')
			# kuup2ev_entry.delete(0, 'end')
			# summa_entry.delete(0, 'end')
			# kuluvoitulu_entry.focus()
			tkinteraken()

		else:
			messagebox.showwarning('Kas tulu või kulu?', message='Vali üks!')
			kuluvoitulu_entry.delete(0, 'end')
			kuluvoitulu_entry.focus()

	tulu_nimi, kulu_nimi, kulu_kuup2ev, tulu_kuup2ev, tulunr, kulunr, tulu_summa, kulu_summa, kogutulu, kogukulu, k2ive, hetkeseis, söökkuluplot, kodukuluplot, muukuluplot, selfkuluplot, autokuluplot, riidedkuluplot = mainbackend()

	lisamine_frame = Frame(root,width=450, height=400, pady=3)
	tabel_frame1 = Frame(root, width=500, height=400, pady=3)
	tabel_frame2 = Frame(root, width=500, height=400, pady=3)
	piechart_frame = Frame(root, width=450,height=400, pady=3)

	root.columnconfigure(1, weight=1)
	root.columnconfigure(2, weight=1)
	root.rowconfigure(0, weight=1)

	lisamine_frame.grid(row=0, column=0, sticky=NSEW)
	tabel_frame1.grid(row=0, column=1, sticky=NS)
	tabel_frame2.grid(row=0, column=2, sticky=NS)
	piechart_frame.grid(row=1, column=0, sticky=NSEW)

	#Lisamine_frame widgets
	Label(lisamine_frame, text='Kulu/tulu:', font=("Bebasneueregular", 14)).grid(row=1, column=0, padx=10, pady=5, sticky=W)
	Label(lisamine_frame, text='Nimi:', font=("Helvetica", 14)).grid(row=2, column=0, padx=10, pady=5, sticky=W)
	Label(lisamine_frame, text='Kuupäev:', font=("Helvetica", 14)).grid(row=3, column=0, padx=10, pady=5, sticky=W)
	Label(lisamine_frame, text='Summa:', font=("Helvetica", 14)).grid(row=4, column=0, padx=10, pady=5, sticky=W)

	kuluvoitulu_entry = Entry(lisamine_frame)
	nimi_entry = Entry(lisamine_frame)
	kuup2ev_entry = Entry(lisamine_frame)
	summa_entry = Entry(lisamine_frame)
	salvesta_button = Button(lisamine_frame, text='Salvesta', command=salvesta)

	kuluvoitulu_entry.grid(row=1, column=1, padx=10, pady=5, ipadx=10, ipady=3)
	nimi_entry.grid(row=2, column=1, padx=10, pady=5, ipadx=10, ipady=3)
	kuup2ev_entry.grid(row=3, column=1, padx=10, pady=5, ipadx=10, ipady=3)
	summa_entry.grid(row=4, column=1, padx=10, pady=5, ipadx=10, ipady=3)
	salvesta_button.grid(row=5, column=1, ipadx=20, ipady=5, pady=10)

	kogutulu_label = Label(lisamine_frame, text=('Kogu tulu: {} €').format(kogutulu), font=("Helvetica", 14)).grid(row=6, column=0, padx=15, pady=5, sticky=W)
	kogukulu_label = Label(lisamine_frame, text=('Kogu kulu: {} €').format(kogukulu), font=("Helvetica", 14)).grid(row=7, column=0, padx=15, pady=5, sticky=W)
	koguvahe_label = Label(lisamine_frame, text=('Vahe: {} €').format(round((kogutulu - kogukulu), 2)), font=("Helvetica", 14))
	koguvahe_label.grid(row=8, column=0, padx=15, pady=5, sticky=W)

	tree1 = ttk.Treeview(tabel_frame1, columns=('kuup2ev','summa'), selectmode='browse')
	tree1.grid(row=0, column=0, sticky=NSEW)
	vsb1 = ttk.Scrollbar(tabel_frame1, orient="vertical", command=tree1.yview)
	vsb1.grid(row=0, column=2, sticky=NS, columnspan=2)
	tree1.configure(yscrollcommand=vsb1.set)
	tree1.rowconfigure(1, weight=1)

	tree1.heading('#0', text='Kulu')
	tree1.column('#0',minwidth=0, width=166)
	tree1.heading('#1', text='Kuupäev')
	tree1.column('#1', minwidth=0, width=166)
	tree1.heading('#2', text='Summa')
	tree1.column('#2', minwidth=0, width=166)
	for j in range(len(kulu_nimi)):
		tree1.insert('', j, text=kulu_nimi[j], values=((kulu_kuup2ev[j] + kuu), (kulu_summa[j] + '€')))

	tree2 = ttk.Treeview(tabel_frame2, columns=('kuup2ev','summa'), selectmode='browse')
	tree2.grid(row=0, column=3, sticky=NSEW)
	vsb2 = ttk.Scrollbar(tabel_frame2, orient="vertical", command=tree2.yview)
	vsb2.grid(row=0, column=5, sticky=NS)
	tree2.configure(yscrollcommand=vsb2.set)

	tree2.heading('#0', text='Tulu')
	tree2.column('#0',minwidth=0, width=166)
	tree2.heading('#1', text='Kuupäev')
	tree2.column('#1', minwidth=0, width=166)
	tree2.heading('#2', text='Summa')
	tree2.column('#2', minwidth=0, width=166)
	for m in range(len(tulu_nimi)):
		tree2.insert('', m, text=tulu_nimi[m], values=((tulu_kuup2ev[m] + kuu), (tulu_summa[m] + '€')))


#PIECHART WIDGETS
	labels = ['Auto', 'Kodu','Muu', 'Self', 'Söök', 'Riided']
	prices = [autokuluplot, kodukuluplot, muukuluplot, selfkuluplot, söökkuluplot, riidedkuluplot]
	fig = matplotlib.figure.Figure(figsize=(5,5))
	ax = fig.add_subplot(111)
	fig.suptitle('Kulude kokkuvõte')
	ax.pie(prices, labels=labels, shadow=True,autopct=lambda p : '{:.2f}%  ({:,.0f})'.format(p,p * sum(prices)/100))
	ax.legend(labels, loc="upper right")

	canvas = FigureCanvasTkAgg(fig, piechart_frame)
	canvas.get_tk_widget().grid(sticky=E)
	canvas.draw()
	kuluvoitulu_entry.focus()



root = Tk()
# root.state('zoomed')
root.title("Finatstabel 2019")
root.iconbitmap(r'C:\Users\Marten\Programmeerimine\Projektid\Finantsid_gui\pilt.ico')

tkinteraken()

root.mainloop()