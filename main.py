import requests
from datetime import datetime
import os
import time
import json

# https://recruiting.ultipro.com/BIO1009BIPH/JobBoard/62507471-7936-4fae-aad4-d0bf9ffa0787/?q=&o=postedDateDesc

def write_json(data,filename): 
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def date_difference(date1, date2):
    date1 = datetime.strptime(date1, "%Y-%m-%d")
    date2 = datetime.strptime(date2, "%Y-%m-%d")
    return abs((date2 - date1).days)


def write_data(data, filename, method): 
    with open(filename, method) as text_file:
        text_file.write(data)

def read_file(filename):
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines

def read_json(filename): 

    f = open(filename, encoding='utf-8')

    data = json.load(f)

    f.close()
    return data


def get_all_counts(): 
    f = open("./files/all_count", "r")
    all_count_str = f.read() 
    all_count_list = all_count_str.split(" ")
    total_post = int(all_count_list[0])
    total_filled = int(all_count_list[1])
    total_repost = int(all_count_list[2])
    return total_post, total_filled, total_repost 


def bot():
    todays_date = datetime.now().strftime("%Y-%m-%d")
    total_post, total_filled, total_repost = get_all_counts()
    files = str(todays_date)+ ".txt"

    cookies = {
        '__RequestVerificationToken': '06IHF7HbhJprhFr96c5WhD0An-pqrB3lliX66OUAx8yib6dCIa5fyDTvtoGRy8hya0ePF788z4L6LhOjQUo6Jy9y2pY1',
        '_pendo_accountId.bab997fe-1554-4e4a-6760-3afebac71371': '7c9a00d1-07fd-4b87-a015-c2e011ecb13c',
        '_pendo_visitorId.bab997fe-1554-4e4a-6760-3afebac71371': '_PENDO_T_cxCCszkX9hQ',
        '_pendo_meta.bab997fe-1554-4e4a-6760-3afebac71371': '1994487483',
        '_ga': 'GA1.2.92643912.1633022897',
        '_gid': 'GA1.2.363993801.1633022897',
        '_gat': '1',
        'nonce': '19Fzc9cdY_iP5Ox1iYM36IUEza5YHN4VLOoGYpdZsHA',
    }

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'X-RequestVerificationToken': '9GVZ425MeFPYMATO1wadUmQ9o7E4jgFD6YOUWAd1mQW72B_bYFrVvY5bgfK8in8yOjgtDWWJiLZAgPPU_IHpIiFxURhm33t18kT8InC1bPJnyoWZlW6_XlxfOreupSXZxSaBbA2',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://recruiting.ultipro.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://recruiting.ultipro.com/BIO1009BIPH/JobBoard/62507471-7936-4fae-aad4-d0bf9ffa0787/?q=&o=postedDateDesc',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    data = '{"opportunitySearch":{"Top":200,"Skip":0,"QueryString":"","OrderBy":[{"Value":"postedDateDesc","PropertyName":"PostedDate","Ascending":false}],"Filters":[{"t":"TermsSearchFilterDto","fieldName":4,"extra":null,"values":[]},{"t":"TermsSearchFilterDto","fieldName":5,"extra":null,"values":[]},{"t":"TermsSearchFilterDto","fieldName":6,"extra":null,"values":[]}]},"matchCriteria":{"PreferredJobs":[],"Educations":[],"LicenseAndCertifications":[],"Skills":[],"hasNoLicenses":false,"SkippedSkills":[]}}'

    response = requests.post('https://recruiting.ultipro.com/BIO1009BIPH/JobBoard/62507471-7936-4fae-aad4-d0bf9ffa0787/JobBoardView/LoadSearchResults', headers=headers, cookies=cookies, data=data)


    data_json = response.json()["opportunities"]
    # data_json.append({'Title':"Tushar", "PostedDate": "2021-07-29Tg"})


    # declare all lists 
    all_posts_today = []
    new_posts = []
    repost = []
    repost_temp = []
    remove_list = []
    refil_posts = []
    new_post_temp = []


    
    all_posts_yesterday = read_json('./files/all_posts.json')
    all_posts_yesterday_temp = all_posts_yesterday.copy()

    filled_post = read_json("./files/filled_post.json")


    
    remove_list = []


    for each_data in data_json:
        each_post_data = each_data["Title"]
        post_date = each_data["PostedDate"]
        each_date = post_date.split("T")[0].strip()

        todays_post_dict = {"post":each_post_data, "date":each_date}

        all_posts_today.append(todays_post_dict)

        if todays_post_dict in all_posts_yesterday:
            all_posts_yesterday_temp.remove(todays_post_dict)
        elif todays_post_dict in filled_post:
            repost.append(todays_post_dict)

            total_repost += 1
            remove_list.append(todays_post_dict)
        else: 
            new_post_temp.append(todays_post_dict)
    print("remove:", remove_list)
    for each_new_post_temp in new_post_temp:

        new = True
        for each_post_yesterday in all_posts_yesterday_temp: 

            if each_post_yesterday['post'] == each_new_post_temp['post']:
                new = False
                if each_post_yesterday['date'] != each_new_post_temp['date']:
                    repost.append(each_new_post_temp)

                    total_repost += 1
                    repost_temp.append(each_post_yesterday)
                    break
                else: 
                    pass 
            
            else: 
                continue
        if new: 
            new_posts.append(each_new_post_temp)
            total_post += 1

    if remove_list: 
        for each_fill in filled_post: 
            if each_fill in remove_list: 
                filled_post.remove(each_fill)
                total_filled -= 1

    for each_post_yesterday in all_posts_yesterday:
        if each_post_yesterday not in all_posts_today and each_post_yesterday not in repost_temp:
            refil_posts.append(each_post_yesterday)
            filled_post.append(each_post_yesterday)
            total_filled += 1

    for each_fill in filled_post:
        each_fill_date = each_fill['date']
        date_count = date_difference(each_fill_date, todays_date)
        if date_count > 42:
            filled_post.remove(each_fill)




    '''
    Writing the files
    '''

    # check if file exists
    path = f"./{todays_date}.txt"
    if os.path.exists(path):
        os.remove(path)

    # write all posts and filled posts
    write_json(all_posts_today, "./files/all_posts.json")
    write_json(filled_post, "./files/filled_post.json")
    


    new_posts_length = len(new_posts)
    filled_posts_length =len(refil_posts)


    # write posts to current text file 
    write_data(f"its ya boy back with another jobs update\n\n", files, "a")
    write_data(f"Positions Posted: {new_posts_length}\n", files, "a")
    if new_posts_length !=0: 
        new_posts_post_only =[]
        for each_new_post in new_posts:
            new_posts_post_only.append(each_new_post['post'])
        new_post_string = f"{new_posts_post_only}".replace("[", "").replace("]", "").replace("'", "").strip()
        print(new_post_string)
        write_data(f"Positions Posted: {new_post_string}\n", files, "a")

    write_data(f"\nPositions Filled: {filled_posts_length}\n", files, "a")
    if filled_posts_length !=0:
        filled_post_only =[]
        for each_fill_post in refil_posts:
            filled_post_only.append(each_fill_post['post'])
        filled_post_string = f"{filled_post_only}".replace("[", "").replace("]", "").replace("'", "").strip()
        print(filled_post_string)
        write_data(f"Positions Filled: {filled_post_string}\n", files, "a")

    write_data(f"\nPositions Reposted: {len(repost)}\n", files, "a")
    if len(repost) !=0:
        repost_post_only =[]
        for each_repost in repost:
            repost_post_only.append(each_repost['post'])
        repost_post_string = f"{repost_post_only}".replace("[", "").replace("]", "").replace("'", "").strip()
        print(repost_post_string)
        write_data(f"Positions Reposted: {repost_post_string}\n", files, "a")

    # upadate all count db
    all_count_new_str = f"{total_post} {total_filled} {total_repost}"
    write_data(all_count_new_str, "./files/all_count", "w")

    # write total count to todays file 
    write_data(f"\nSince 2/17/2022", files, "a")
    write_data(f"\nTotal Positions Posted: {total_post}\n", files, "a")
    write_data(f"Total Positions Filled: {total_filled}\n", files, "a")
    write_data(f"Total Positions Reposted: {total_repost}\n", files, "a")
    

bot()
print("\nScraping Complete!\n")
print("Please check the txt file that is generated!\n")


