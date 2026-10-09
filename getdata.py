import pandas as pd
import eurostat

BALKAN_CODES = ['EL', 'BG', 'RO', 'HR', 'SI', 'RS', 'AL', 'ME', 'MK']

def filter_balkan_nuts2(df):
    geo_col = next((col for col in df.columns if col.startswith('geo')), None)
    if not geo_col: return pd.DataFrame()
    mask = df[geo_col].apply(lambda x: isinstance(x, str) and len(x) == 4 and x[:2] in BALKAN_CODES)
    return df[mask].copy()

def filter_balkan_nuts0(df):
    geo_col = next((col for col in df.columns if col.startswith('geo')), None)
    if not geo_col: return pd.DataFrame()
    mask = df[geo_col].apply(lambda x: isinstance(x, str) and len(x) == 2 and x in BALKAN_CODES)
    return df[mask].copy()

def melt_and_filter(df, value_name):
    geo_col = next((col for col in df.columns if col.startswith('geo')), None)
    year_cols = [col for col in df.columns if str(col).isdigit()]
    
    df_melted = pd.melt(df, id_vars=[geo_col], value_vars=year_cols, var_name='Year', value_name=value_name)
    df_melted['Year'] = df_melted['Year'].astype(int)
    df_filtered = df_melted[(df_melted['Year'] >= 2018) & (df_melted['Year'] <= 2024)].copy()
    df_filtered = df_filtered.rename(columns={geo_col: 'geo'})
    
    df_filtered[value_name] = pd.to_numeric(df_filtered[value_name], errors='coerce')
    # Kluczowe: usuwamy duplikaty, jeśli w danym roku/regionie pojawiło się coś wielokrotnie
    return df_filtered.dropna(subset=[value_name]).drop_duplicates(subset=['geo', 'Year'])[['geo', 'Year', value_name]]

# 1. Noclegi ogółem
df_tot = filter_balkan_nuts2(eurostat.get_data_df('tour_occ_nin2'))
df_tot = df_tot[(df_tot['c_resid'] == 'TOTAL') & (df_tot['unit'] == 'NR')]
nights_tot_long = melt_and_filter(df_tot, 'Noclegi_Ogolem')

# 2. Noclegi zagraniczne
df_for = filter_balkan_nuts2(eurostat.get_data_df('tour_occ_nin2'))
df_for = df_for[(df_for['c_resid'] == 'FOR') & (df_for['unit'] == 'NR')]
nights_for_long = melt_and_filter(df_for, 'Noclegi_Zagraniczne')

# 3. Baza noclegowa (obiekty)
df_cap = filter_balkan_nuts2(eurostat.get_data_df('tour_cap_nuts2'))
df_est = df_cap[(df_cap['accomunit'] == 'ESTBL') & (df_cap['unit'] == 'NR') & (df_cap['nace_r2'] == 'I551-I553')]
establishments_long = melt_and_filter(df_est, 'Liczba_Obiektow')

# 4. Ruch lotniczy
df_air = filter_balkan_nuts2(eurostat.get_data_df('tran_r_avpa_nm'))
df_air = df_air[df_air['tra_meas'] == 'PAS_CRD']
air_long = melt_and_filter(df_air, 'Ruch_Lotniczy')

# 5. Poziom cen - bierzemy OGÓLNY wskaźnik poziomu cen (PLI) dla całej gospodarki, 
# żeby uniknąć tysięcy wierszy z podziałem na konkretne grupy produktów
df_prices = filter_balkan_nuts0(eurostat.get_data_df('prc_ppp_ind'))
if 'na_item' in df_prices.columns:
    # PLI_EU27_2020 to uniwersalny wskaźnik poziomu cen względem średniej UE
    df_prices = df_prices[df_prices['na_item'] == 'PLI_EU27_2020']
prices_long = melt_and_filter(df_prices, 'Poziom_Cen_NUTS0')

# =====================================================================
# Bezpieczne łączenie (Left join pilnujący 1 wiersza na region/rok)
# =====================================================================
master_df = nights_tot_long.copy()

for df_to_merge in [nights_for_long, establishments_long, air_long]:
    master_df = pd.merge(master_df, df_to_merge, on=['geo', 'Year'], how='left')

master_df['NUTS0'] = master_df['geo'].str[:2]
prices_long = prices_long.rename(columns={'geo': 'NUTS0'})

# Łączymy ceny krajowe, upewniając się, że prices_long ma unikalne pary [NUTS0, Year]
prices_long = prices_long.drop_duplicates(subset=['NUTS0', 'Year'])
master_df = pd.merge(master_df, prices_long, on=['NUTS0', 'Year'], how='left')

# =====================================================================
# 6. Jakość wód kąpielowych (Krajowa - sdg_14_40)
# =====================================================================
print("Pobieranie jakości wód kąpielowych...")
df_water_raw = eurostat.get_data_df('sdg_14_40')
df_water_nuts0 = filter_balkan_nuts0(df_water_raw)

# Bezpieczne filtrowanie wskaźnika (np. udział wód o doskonałej jakości - 'EXC' lub ogółem)
mask_water = pd.Series(True, index=df_water_nuts0.index)
if 'wat_qual' in df_water_nuts0.columns:
    mask_water &= (df_water_nuts0['wat_qual'] == 'EXC')
if 'c_env' in df_water_nuts0.columns:
    mask_water &= (df_water_nuts0['c_env'] == 'TOTAL')

df_wat = df_water_nuts0[mask_water]
water_long = melt_and_filter(df_wat, 'Wody_Doskonała_Jakość_NUTS0')

# =====================================================================
# Łączenie wód kąpielowych z Master DataFrame
# =====================================================================
water_long = water_long.rename(columns={'geo': 'NUTS0'})
water_long = water_long.drop_duplicates(subset=['NUTS0', 'Year'])

master_df = pd.merge(master_df, water_long, on=['NUTS0', 'Year'], how='left')

print("Liczba wierszy po poprawionym złączeniu:", len(master_df))
print(master_df.head(15))

master_df.to_excel("baza_balkany.xlsx", index=False)