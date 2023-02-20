import glob
import pandas as pd
import pyodbc 
import os
import warnings
warnings.filterwarnings('ignore')

# ************************************ requirement 3
def strip_obj(col):
   col = col.str.replace('\n', '')
   col = col.str.replace('\t', '')
   col = col.str.replace('\r', '')
   return col

#******************************************* requirement 4
def extract_director(value):
   if 'Director' in value or 'Directors' in value:
      director=value.strip().split('|')[0]
      director_name=director.split(':')[1]
      return director_name
   else:
      return ''

def extract_star(value):
   if 'Star' in value or 'Stars' in value:
      star_name=value.split(':')[-1]
      return star_name
   else:
      return ''
      
#********************************* requirement 6
def clean_year (value):
    if 'TV Special' in value or 'TV Movie' in value or 'TV Short' in value or 'Video' in value or 'Video Game'in value or 'I'in value or 'L'in value or 'Game' in value or 'II'in value or 'III'in value or 'V'in value or 'IV'in value or 'IX'in value or 'VI'in value or 'VII'in value or 'VIII'in value or 'XI'in value or 'X'in value or 'XX'in value or 'XL'in value or 'XII'in value or 'XIII'in value or 'XLI' in value or 'XXIII'in value:
        return 0
    else:
        return value
    
def extract_start(value):
   if "–" in value:
      cols=value.split('–')
      start_year=cols[0]  
      return start_year
   else:
      return value

def extract_end(value):
   if "–" in value:
      cols=value.split('–')      
      if cols[1] != ' ':
         end_year=cols[1]
      else: 
         end_year="Present"
      return end_year
   else:
      return value
 
def calc_lasted(start_year,end_year):
   lasted = [] 
   for index, value in end_year.items():
      if value == 'Present':
         lasted.append('')   
      else:
         lasted.append(int(value) - int(start_year.at[index])) 
   return lasted

def main():

   #***************************************************** requirement 1
   path = "C:/Users/A/OneDrive/Desktop/task2/Files/"
   filenames = glob.glob(path + "/*.csv")
   for file in filenames:
      df = pd.read_csv(file, on_bad_lines='skip')
      
      filename= file.split('\\')[-1]
      destination = 'C:/Users/A/OneDrive/Desktop/task2/archived_files'
      #********************************************************************** requirement 2
      ndf = df.dropna(subset=['MOVIES','YEAR','GENRE','RATING','ONE-LINE','STARS','VOTES','RunTime','Gross'], how='all')
      ndf.dropna(subset=['YEAR'],axis=0,inplace=True,how='any') 
      ndf.reset_index()
      
      #********************************************************************** requirement 3
      ndf[["GENRE","ONE-LINE","STARS","owner_company"]] = ndf[["GENRE","ONE-LINE","STARS","owner_company"]].apply(strip_obj)

      #********************************************************************** requirement 4    
      ndf['Director']=ndf['STARS'].map(lambda x: extract_director(x))      
      ndf['Stars']=ndf['STARS'].map(lambda x: extract_star(x))
      
      #********************************************************************** requirement 5
      ndf['extraction_date'] = pd.to_datetime(ndf['Extract_date']).dt.date
      ndf['extraction_time'] = pd.to_datetime(ndf['Extract_date']).dt.time

      #********************************************************************** requirement 6
      ndf['YEAR'] = ndf['YEAR'].str.strip('()').astype(str)
      
      ndf['YEAR']=ndf['YEAR'].map(lambda x: clean_year(x))
      
      ndf['YEAR'] = ndf['YEAR'].astype(str)
      ndf['start_year']=ndf['YEAR'].map(lambda x: extract_start(x))
      ndf['end_year']=ndf['YEAR'].map(lambda x: extract_end(x))

      ndf['lasted'] = calc_lasted(ndf['start_year'],ndf['end_year'])

      # ******************************************** requirement 7
      server='LAPTOP-DMTSAQEM'
      database='task2'

      cnxn=pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                           SERVER='+ server +'; \
                           DATABASE='+ database +'; \
                           Trusted_Connection=yes;')

      cursor=cnxn.cursor()
      ndf['owner_company'] = ndf['owner_company'].str.strip()
      for x in ndf['owner_company'].unique():
         cursor.execute(f'''INSERT INTO Company VALUES('{x}')''')
         cursor.commit()
      
      # ******************************************** requirement 8
      cursor=cnxn.cursor()
      ndf['Director'] = ndf['Director'].str.replace("'", "")
      for x in ndf['Director'].unique():
         cursor.execute(f'''INSERT INTO Director VALUES('{x}')''')
         cursor.commit()
               
      # ******************************************** requirement 9
      cursor=cnxn.cursor()
      ndf.drop('STARS', axis=1, inplace=True)
      ndf.drop('Extract_date', axis=1, inplace=True)
      ndf.drop('YEAR', axis=1, inplace=True)
      ndf.rename(columns={"ONE-LINE":"ONE_LINE"},inplace=True)
         
      cols = ",".join([str(i) for i in ndf.columns.tolist()])

      for col in ndf.columns:
         ndf[col] = ndf[col].astype(str)

      print('Dataframe shape:', ndf.shape)
      
      for i,row in ndf.iterrows():
         value_placeholders = ", ".join(['?'] * len(row))
         sql = "INSERT INTO {} ({}) VALUES ({});".format("task2.dbo.Movies", cols,value_placeholders )
         cursor.execute(sql,tuple(row.values))
         cursor.commit()
         
      #********************************************************************** requirement 10 :DONE
      dst_path = os.path.join(destination, filename)
      os.rename(file, dst_path)
      
main()


