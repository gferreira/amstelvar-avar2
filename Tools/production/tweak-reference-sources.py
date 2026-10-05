import os
from controller import AmstelvarA2Controller
from ufoProcessor.ufoOperator import UFOOperator
from xTools4.modules.blendsPreview import instantiateGlyph

folder = os.path.dirname(os.path.dirname(os.getcwd()))

subFamily = ['Roman', 'Italic'][0]

p = AmstelvarA2Controller(folder, 'AmstelvarA2', subFamily)

glyphNames = p.defaultFont.glyphOrder

preflight = True

parametersTweak = {
    "wght1000": {
        # XOPQ = 132
        "XOUC" : 292,
        "XOUA" : 144,
        "XOLC" : 284,
        "XOLA" : 142,
        "XOFI" : 287,
        "XOET" : 242,
        # XTRA = 320
        "XTUC" : 170,
        "XTUR" : 262,
        "XTUD" : 224,
        "XTLC" : 90,
        "XTLR" : 124,
        "XTLD" : 128,
        "XTFI" : 188,
        "XTET" : 549,    
        # XSHA = 74
        "XSHU" : 59,
        "XSHL" : 44,
        "XSHF" : 94,
    },
    "wght1000_wdth125": {
        # XOPQ = 160
        "XOUC" : 310,
        "XOUA" : 154,
        "XOLC" : 293,
        "XOLA" : 142,
        "XOFI" : 302,
        "XOET" : 246,
        # YOPQ = 91
        "YOUC" : 106,
        "YOLC" : 103,
        "YOFI" : 99,
        "YOET" : 107,
        # XTRA = 318
        "XTUC" : 368,
        "XTUR" : 498,
        "XTUD" : 426,
        "XTLC" : 255,
        "XTLR" : 316,
        "XTLD" : 256,
        "XTFI" : 266,
        "XTET" : 673,    

    },
}

operator = UFOOperator()
operator.read(p.designspacePath)
operator.loadFonts()

print(f'parametrically tweaking reference sources...')

for styleName in parametersTweak.keys():
    print(f'\ttweaking {styleName}...')
    # open reference source
    referenceSourceName = f'Amstelvar-{subFamily}_{styleName}'
    referenceSourcePath = p.referenceSourcesPaths.get(referenceSourceName)
    referenceSource = OpenFont(referenceSourcePath, showInterface=False)
    # get current blend parameters for this style
    parameters = p.blendedSources[styleName]
    # apply tweaks to blend parameters
    for k, v in parametersTweak[styleName].items():
        print(f'\t\t{k}: {parameters[k]} -> {v}')
        parameters[k] = v
    # instantiate glyphs from parameters
    for glyphName in glyphNames:
        print(f'\t\tinstantiating {glyphName}...')
        g = instantiateGlyph(operator, glyphName, parameters)
        referenceSource[glyphName] = RGlyph(g)
    # close and save reference source
    if not preflight:
        print(f'\t\tsaving...')
        referenceSource.close(save=True)
    else:
        referenceSource.openInterface()

print('...done!\n')

