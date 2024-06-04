import pandas as pd
import lang_strings as la

str_rings_num = la.str_datasheet_rings_num
str_rings_pos_left = la.str_datasheet_rings_pos_left
str_rings_pos_right = la.str_datasheet_rings_pos_right
str_rings_diameter = la.str_datasheet_rings_diameter
str_rings_diameter_2 = la.str_datasheet_rings_diameter_2
str_rings_diameter_dd = la.str_datasheet_rings_diameter_dd

data_temp = {
    str_rings_num: ['11', '12', '13', '14','15','21','22','23','24','25'],
    str_rings_pos_left: ['', '', '', '','','','','','',''],
    str_rings_pos_right: ['', '', '', '','','','','','',''],
    str_rings_diameter: ['', '', '', '','','','','','',''],
    str_rings_diameter_2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    str_rings_diameter_dd: ['', '', '', '','','','','','',''],
    }
df = pd.DataFrame(data_temp)
data = df.to_dict('records')