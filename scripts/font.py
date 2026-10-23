import ctypes
from fontTools.ttLib import TTFont
ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(),0x4000)
f=TTFont('maintenance/fonts/ChillRoundF.ttf')
for r in f['name'].names:
    if r.nameID in (1,3,4,6,16,17):
        value={1:'Utae Web Round',3:'UtaeWebRound-Regular',4:'Utae Web Round Regular',6:'UtaeWebRound-Regular',16:'Utae Web Round',17:'Regular'}[r.nameID]
        r.string=value.encode(r.getEncoding())
f.flavor='woff2'
f.save('site/assets/UtaeWebRound.woff2')
print('WOFF2 ready')

