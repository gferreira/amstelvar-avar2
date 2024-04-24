# menuTitle: copy glyph order from default to all other sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
defaultName   = 'wght400'
defaultPath   = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{defaultName}.ufo')

assert os.path.exists(sourcesFolder)
assert os.path.exists(defaultPath)

srcFont = OpenFont(defaultPath, showInterface=False)
# glyphOrder = srcFont.glyphOrder
glyphOrder = srcFont.templateGlyphOrder

ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

for ufoPath in ufoPaths:
    if ufoPath == defaultPath:
        continue
    font = OpenFont(ufoPath, showInterface=False)
    print(f'setting glyph order in {ufoPath}…')
    font.templateGlyphOrder = glyphOrder
    font.save()
    # font.close()
