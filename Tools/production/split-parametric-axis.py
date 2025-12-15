# menuTitle: split parametric axes

import os, glob, shutil
from fontTools.designspaceLib import DesignSpaceDocument

familyName      = 'AmstelvarA2'
subFamilyName   = ['Roman', 'Italic'][0]
baseFolder      = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder   = os.path.join(baseFolder, 'Sources', subFamilyName)
designspacePath = os.path.join(sourcesFolder, f'AmstelvarA2-{subFamilyName}_avar2.designspace')

preflight = False

glyphNames = ['U']

axesNames = {
    # src   # dst
    'XOUC': 'U#XO',
    'YOUC': 'U#YO',
    'XTUR': 'U#XT',
    # 'XUCS': 'U#XS',
    'XQUC': 'U#XQ',
    # 'YQUC': 'U#YQ',
}

srcPaths = glob.glob(f'{sourcesFolder}/*.ufo')

designspace = DesignSpaceDocument()
designspace.read(designspacePath)

defaultFont = OpenFont(designspace.default.path, showInterface=False)

for srcAxisName, dstAxisName in axesNames.items():

    print(f'splitting {dstAxisName} from {srcAxisName}...') # srcAxisName, styleName, dstAxisName)

    for srcPath in srcPaths:
        srcStyleName = os.path.splitext(os.path.split(srcPath)[-1])[0].split('_')[-1]

        if srcAxisName not in srcStyleName:
            continue

        dstStyleName = srcStyleName.replace(srcAxisName, dstAxisName)

        print(f'\t making {dstStyleName} from {srcStyleName}...')

        srcFont = OpenFont(srcPath, showInterface=False)

        dstPath = srcPath.replace(srcAxisName, dstAxisName)
        if os.path.exists(dstPath):
            shutil.rmtree(dstPath)
        shutil.copytree(designspace.default.path, dstPath)
        dstFont = OpenFont(dstPath, showInterface=False)
        dstFont.info.styleName = dstStyleName

        for glyphName in glyphNames:
            print(f'\t\tmoving /{glyphName}...')
            # copy src glyph to dst
            srcGlyph = srcFont[glyphName]
            dstFont.insertGlyph(srcGlyph, name=glyphName)
            # copy default glyph to src
            defaultGlyph = defaultFont[glyphName]
            srcFont.insertGlyph(defaultGlyph, name=glyphName)

        if not preflight:
            srcFont.save()
            dstFont.save()

    print()

