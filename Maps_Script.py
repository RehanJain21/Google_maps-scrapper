import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import time

user_agent = UserAgent().random


headers = {
    'User-Agent': user_agent,
    'Accept-Language': 'en-US,en;q=0.5',
}


all_company_name1 = []
all_company_names = []
all_company_links = []


for page in range(1, 13):
 
    url = f"https://www.google.com/search?sca_esv=585445638&tbs=lf:1,lf_ui:2&tbm=lcl&sxsrf=AM9HkKlWztXowrT648F5OEde0hebAuAQjQ:1701021135358&q=real+estate+agent+in+Jasola&rflfq=1&num=20&start={20 * (page - 1)}"

    response = requests.get(url, headers=headers)
    print(response)

   
    soup = BeautifulSoup(response.text, 'html.parser')

  
    company_divs = soup.find_all('div', class_='VkpGBb')

    for company_div in company_divs:
        company_name = company_div.text.strip()
        all_company_names.append(company_name)

   
        link_tag = company_div.find('a', href=True)
        if link_tag:
            company_link = link_tag['href']
            all_company_links.append(company_link)
        else:
            all_company_links.append(None)
            
    company_divs1=soup.find_all("div",class_='dbg0pd')
    
    for company_div1 in company_divs1:
        company_name1 = company_div1.text.strip()
        all_company_name1.append(company_name1)
    
    
    time.sleep(5)


data = {'Company Name': all_company_names, 'Company Link': all_company_links, 'Company Name1':all_company_name1}
df = pd.DataFrame(data)

print(df.head())

df['Company Name'] = df['Company Name'].astype(str)  
print(df)
df[['col1', 'col2', 'col3', 'col4', 'col5']] = df['Company Name'].str.split('·', expand=True)

columns_to_clean = ['col3','col4', 'col5']


def extract_numeric(value):
    try:
        return float(''.join(filter(str.isdigit, str(value))))
    except ValueError:
        return float('nan') 

for column in columns_to_clean:
    df[column] = df[column].apply(extract_numeric)
print(df)


df = df[(df['col3'].astype(str).apply(len) >= 10) | (df['col4'].astype(str).apply(len) >= 10)]

df = df.reset_index(drop=True)


df['col3'] = df['col3'].astype(str)


df['col3'] = df['col3'].apply(lambda x: '0' if len(x) < 10 else x)

df['col3'] = pd.to_numeric(df['col3'])
def extract_last_10_digits(value):
    return str(value)[-12:]


df['col3'] = df['col3'].apply(extract_last_10_digits)
df['col4'] = df['col4'].apply(extract_last_10_digits)


df['col4']=df['col4'].replace('nan',0)

df['col5']= df['col3'].astype(float) + df['col4'].astype(float)




df['col2','col3','col4'].drop(inplace=True)
column1_values = df['Company Name'].astype(str)
column2_values = df['Company Name1'].astype(str)


for index, row in df.iterrows():
    for word in column2_values:
        if word in column1_values.iloc[index]:
            df.at[index, 'Company Name1'] = word
            break 


df.to_excel('final.xlsx', index=False)