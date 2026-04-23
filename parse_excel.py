import zipfile, xml.etree.ElementTree as ET

path = r'C:\Users\AdminTC\OneDrive - NUST\Documents\Academic Track\Academic track.xlsx'
with zipfile.ZipFile(path) as z:
    ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

    # Load shared strings
    with z.open('xl/sharedStrings.xml') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        shared = []
        for si in root.findall('ns:si', ns):
            t_nodes = si.findall('.//ns:t', ns)
            shared.append(''.join(t.text or '' for t in t_nodes))

    # Parse sheet
    with z.open('xl/worksheets/sheet1.xml') as f:
        tree = ET.parse(f)
        root = tree.getroot()

    rows = root.findall('.//ns:row', ns)
    for row in rows:
        cells = row.findall('ns:c', ns)
        row_data = []
        for c in cells:
            ref = c.get('r')
            t = c.get('t', '')
            v = c.find('ns:v', ns)
            if v is not None:
                val = shared[int(v.text)] if t == 's' else v.text
            else:
                val = ''
            row_data.append(str(ref) + '=' + repr(val))
        print('Row ' + str(row.get('r')) + ': ' + ' | '.join(row_data))
