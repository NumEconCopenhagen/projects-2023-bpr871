
"""
    dict_crosswalk: Content

    Contains a crosswalk file for converting the industry classifications 
    from Danmarks Statistik in to the classification system from the 
    Industrial Federation of Robotics.
"""

dict_crosswalk = {'01000':'A-B-Agriculture, forestry, fishing',
    '02000':'A-B-Agriculture, forestry, fishing',
    '03000':'A-B-Agriculture, forestry, fishing',
    '06090':'C-Mining and quarrying',
    '10120': '10-12-Food and beverages',
    '13150':'13-15-Textiles',
    '16000': '16-Wood and furniture',
    '17000':'17-18-Paper',
    '18000':'17-18-Paper',
    '19000':'19-22-Plastic and chemical products',
    '20000':'19-22-Plastic and chemical products',
    '21000':'19-22-Plastic and chemical products',
    '22000':'19-22-Plastic and chemical products',
    '23000':'23-Glass, ceramics, stone, mineral products (non-auto',
    '24000':'24-Basic metals',
    '25000':'25-Metal products (non-automotive)',
    '28000':'28-Industrial machinery',
    '26000':'26-27-Electrical/electronics',
    '27000':'26-27-Electrical/electronics',
    '29000':'29-Automotive',
    '30000':'30-Other vehicles',
    '31320':'91-All other manufacturing branches',
    '33000':'91-All other manufacturing branches',
    '35000':'E-Electricity, gas, water supply',
    '36000':'E-Electricity, gas, water supply',
    '37390':'E-Electricity, gas, water supply',
    '41430':'F-Construction',
    '72002':'P-Education/research/development',
    '85202':'P-Education/research/development'}

"""
    dict_legend: Content

    Translation for the industry classifications for IFR 
    in to more appropriate legend titles.
"""
  
dict_legend = {
    'A-B-Agriculture, forestry, fishing': 'Agriculture, forestry, fishing',
    'C-Mining and quarrying': 'Mining and quarrying',
    '10-12-Food and beverages': 'Food and beverages',
    '13-15-Textiles': 'Textiles',
    '16-Wood and furniture': 'Wood and furniture',
    '17-18-Paper': 'Paper',
    '19-22-Plastic and chemical products': 'Plastic and chemical products',
    '23-Glass, ceramics, stone, mineral products (non-auto': 'Glass, ceramics, stone, mineral products',
    '24-Basic metals': 'Basic metals',
    '25-Metal products (non-automotive)': 'Metal products (non-automotive)',
    '26-27-Electrical/electronics': 'Electrical/electronics',
    '28-Industrial machinery': 'Industrial machinery',
    '29-Automotive': 'Automotive',
    '30-Other vehicles': 'Other vehicles',
    '91-All other manufacturing branches': 'All other manufacturing branches',
    'E-Electricity, gas, water supply': 'Electricity, gas, water supply',
    'F-Construction': 'Construction',
    'P-Education/research/development': 'Education/research/development',
    '90-All other non-manufacturing branches': 'All other non-manufacturing branches'
}
