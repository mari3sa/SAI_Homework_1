from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader
r=Path.cwd(); results=json.loads((r/'experiments/results.json').read_text()); assert all(v['exit_code']==0 for v in results.values()), 'Esperimenti incompleti o errori software'; out=r/'submission/Mazzara_2278680_Homework1.pdf'
p=r/'report/relazione.md';s=p.read_text(encoding='utf-8').replace('Nome: DA COMPILARE | Cognome: DA COMPILARE | Matricola: DA COMPILARE','Nome: Mariateresa | Cognome: Mazzara | Matricola: 2278680').replace('Modello del telefono e immobilita tra le serie da confermare.','Telefono: Samsung Galaxy S22. Immobilita tra le serie non confermata.').replace('Previsione DA SALVARE PRIMA DEL RUN:','Previsione salvata prima del run:');p.write_text(s,encoding='utf-8')
c=canvas.Canvas(str(out),pagesize=(595.28,841.89)); c.setTitle('Break COLMAP - Mariateresa Mazzara - 2278680'); c.setAuthor('Mariateresa Mazzara')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=10,leading=13,textColor=HexColor('#243247'))
def page(title,num):
 c.setFillColor(HexColor('#17364d'));c.rect(0,766,596,76,fill=1,stroke=0);c.setFillColor(white);c.setFont('Helvetica-Bold',19);c.drawString(38,804,title);c.setFont('Helvetica',10);c.drawString(38,783,'Mariateresa Mazzara | 2278680 | Foundations of Spatial AI')
 c.setFillColor(HexColor('#64748b'));c.setFont('Helvetica',8);c.drawString(38,24,'Homework 1 - Break COLMAP | 16 ottobre 2026');c.drawRightString(557,24,str(num))
def para(txt,y,size=10):
 st=ParagraphStyle('p',parent=style,fontSize=size,leading=size+3);p=Paragraph(txt,st);w,h=p.wrap(519,740);p.drawOn(c,38,y-h);return y-h-9
def pic(path,x,y,w,h):
 c.drawImage(str(path),x,y,width=w,height=h,preserveAspectRatio=True,anchor='c',mask='auto')
page('Break COLMAP: risultati e analisi',1)
y=748
y=para('<b>Acquisizione e impostazioni.</b> Foto scattate con Samsung Galaxy S22. Baseline: scarpa su cesto bianco, ripresa in ambiente interno lungo un giro; selezionate 20 viste dalle serie 22:19 e 22:21, con spaziatura approssimativa. Sottoinsiemi da 10, 5 e 3 immagini agli indici floor(i*20/n) dell’ordine circolare. Non è stata confermata l’immobilità tra le due serie. Sono state utilizzate le fotografie originali fornite dalla studentessa, conservate senza ulteriori ricompressioni.',y)
y=para('COLMAP 4.2.1 (commit bd1fcf6), automatic_reconstructor, impostazioni geometriche predefinite, ricostruzione sparsa (--dense 0). Tutti i sei esperimenti usano CPU (--use_gpu 0) e due thread (--num_threads 2), dopo arresti software nelle esecuzioni GPU e CPU con parallelismo automatico. Ogni caso ha database e workspace indipendenti; gli arresti software preliminari sono esclusi dai risultati.',y)
data=[['Esperimento','Input','Registrate','Punti 3D','Esito'],['Baseline','20','20','11.560','Un modello, sfondo e dispersione'],['Riduzione','10','10','2.018','Nuvola molto più rada'],['Riduzione','5','3','51','Frammento non riconoscibile'],['Riduzione','3','0','0','Nessun modello'],['Fallimento','6','4','13','Scena non ricostruita utilmente'],['Riparazione','9','9','6.795','Recupero parziale della struttura']]
t=Table(data,colWidths=[84,37,61,62,275],rowHeights=22);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#17364d')),('TEXTCOLOR',(0,0),(-1,0),white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#edf3f7'),white]),('VALIGN',(0,0),(-1,-1),'MIDDLE')]));t.wrap(519,200);t.drawOn(c,38,y-154);y-=168
y=para('<b>Riduzione delle viste.</b> Tutti i casi con modello producono una sola componente. Passando da 20 a 10 viste i punti scendono da 11.560 a 2.018; con 5 restano 3 viste e 51 punti, con 3 nessun modello. Con 20 e 10 viste il profilo della scarpa è riconoscibile, insieme a punti di sfondo; con 5 resta un frammento non interpretabile. Il minor numero di viste aumenta i cambiamenti di aspetto tra immagini e riduce il supporto alle tracce. La registrazione completa non certifica la correttezza geometrica.',y)
y=para('<b>Fallimento intenzionale.</b> Sei viste dei libri e del piano, seguendo un protocollo di rotazione quasi sul posto. Previsione salvata prima del run: feature e corrispondenze presenti, ma poca parallasse e inizializzazione/triangolazione instabile. Sono estratti 56.508 keypoint complessivi. Il log mostra difficoltà di inizializzazione e rilassamento automatico dei vincoli; il modello conservato ha solo 13 punti e 27 osservazioni. È un fallimento geometrico utile, non un crash. L’esito è coerente con scarsa parallasse, senza dimostrare rotazione perfettamente pura.',y)
y=para('<b>Riparazione.</b> Aggiunte esattamente 3 foto con cambiamento di punto di vista, mantenendo le 6 iniziali e gli stessi parametri. Si ottengono 9/9 viste, 6.795 punti e 31.371 osservazioni; traccia media 4,62 e errore medio di riproiezione 1,065 px. Si distinguono fasce dei dorsi e parti del piano, ma persistono zone mancanti e punti dispersi. Il recupero è netto, la scena resta parziale. Accuratezza metrica e pose non sono verificate indipendentemente. Il precedente errore di soli 0,000016 px su 13 punti dimostra che un residuo basso da solo non prova una ricostruzione corretta.',y)
assert y>40,y
c.showPage();page('Figure: riduzione delle viste',2)
base=sorted((r/'originals/baseline').glob('*.jpeg'))
for i,idx in enumerate([0,8,15]):pic(base[idx],38+i*176,554,166,190)
para('Figura 1. Tre immagini di ingresso rappresentative della serie baseline. Le fotografie originali sono conservate senza modifiche nello ZIP.',541,9)
pic(r/'report/baseline_clouds.png',30,70,535,440)
para('Figura 2. Proiezioni dei modelli da 20, 10 e 5 immagini (righe). Assi PCA e scala arbitraria indipendenti per modello; limiti ai percentili 2-98 per leggibilità, senza eliminare punti dai modelli. Il caso da 3 viste non produce un modello.',65,8)
c.showPage();page('Figure: fallimento e riparazione',3)
broken=sorted((r/'originals/broken').glob('*.jpeg'));extra=sorted((r/'originals/repair_extra').glob('*.jpeg'))
for i,path in enumerate([broken[2],extra[0],extra[2]]):pic(path,38+i*176,501,166,238)
para('Figura 3. Una vista del caso iniziale (sinistra) e due delle tre viste aggiunte (centro e destra). Il cambiamento di punto di vista aggiunge vincoli sulla profondità.',484,9)
pic(r/'report/repaired_clouds.png',24,235,547,220)
para('Figura 4. Tre proiezioni della nuvola riparata, con 6.795 punti. Le fasce colorate dei libri sono riconoscibili, ma la ricostruzione è incompleta. Limiti ai percentili 2-98; scala arbitraria.',221,9)
para('<b>Tracciabilità.</b> I sei esperimenti, i comandi e gli hash delle immagini sono salvati nel progetto. La previsione iniziale è registrata separatamente prima dell’esecuzione. Lo ZIP contiene 29 file: 20 baseline, 6 fallimento e 3 aggiuntivi; i sottoinsiemi riutilizzano le stesse immagini.',155,10)
para('Documentazione del comando: https://colmap.github.io/cli.html',83,9)
c.save()
reader=PdfReader(out);assert len(reader.pages)==3
assert '2278680' in reader.pages[0].extract_text()
print(out);print('Pages:',len(reader.pages),'page1 characters:',len(reader.pages[0].extract_text()))
import pypdfium2 as pdfium
qa=r/'tmp/pdfs';qa.mkdir(parents=True,exist_ok=True)
doc=pdfium.PdfDocument(str(out))
for i in range(len(doc)):doc[i].render(scale=1.2).to_pil().save(qa/f'page_{i+1}.png')
