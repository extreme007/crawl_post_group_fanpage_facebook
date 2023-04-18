import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import pyotp
import json
from tqdm import tqdm

# Đoạn script này dùng để khởi tạo 1 chrome profile
def initDriverProfile(profile):
    CHROMEDRIVER_PATH = './chromedriver.exe'
    WINDOW_SIZE = "375,812"
    mobile_emulation = {
        "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
    }

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # chrome_options.add_argument("user-data-dir=/home/extreme/.config/google-chrome/" + str(profile))  # Path to your chrome profile
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-gpu') if os.name == 'nt' else None  # Windows workaround
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-feature=IsolateOrigins,site-per-process")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--ignore-certificate-error-spki-list")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-blink-features=AutomationControllered")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")  # open Browser in maximized mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_argument('disable-infobars')

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              options=chrome_options
                              )
    driver.set_page_load_timeout(60)
    return driver


def checkLiveClone(driver):
    try:
        driver.get("https://mbasic.facebook.com/")
        time.sleep(2)
        driver.get("https://mbasic.facebook.com/")
        time.sleep(1)
        elementLive = driver.find_elements_by_name("view_post")
        if (len(elementLive) > 0):
            print("Live")
            return True

        return False
    except:
        print("view fb err")


def getCodeFrom2FA(code):
    totp = pyotp.TOTP(str(code).strip().replace(" ", "")[:32])
    time.sleep(2)
    return totp.now()


def confirm2FA(driver):
    time.sleep(1)
    btnRadioClick = driver.find_element(By.CSS_SELECTOR,
        "input[value='dont_save']").click()
    time.sleep(1)
    continueBntSubmit = driver.find_element(By.CSS_SELECTOR,"#checkpointSubmitButton-actual-button").click()


def loginBy2FA(driver, username, password, code):
    # changeMacAdrress()
    # changeIp4G()
    # readIp()

    driver.get("https://mbasic.facebook.com/login/?next&ref=dbl&fl&refid=8")
    sleep(2)
    userNameElement = driver.find_element(By.CSS_SELECTOR,"#m_login_email")
    userNameElement.send_keys(username)
    time.sleep(1)
    passwordElement = driver.find_element(By.XPATH,"//*[@id='password_input_with_placeholder']/input")
    passwordElement.send_keys(password)
    time.sleep(1)
    btnSubmit = driver.find_element(By.CSS_SELECTOR,"#login_form > ul > li:nth-child(3) > input")
    btnSubmit.click()
    faCodeElement = driver.find_element(By.CSS_SELECTOR,"#approvals_code")
    faCodeElement.send_keys(str(getCodeFrom2FA(code)))
    time.sleep(1)
    btn2fa = driver.find_element(By.CSS_SELECTOR,"#checkpointSubmitButton-actual-button")
    btn2fa.click()
    confirm2FA(driver)
    try:
        btn2fa = driver.find_element(By.CSS_SELECTOR,"#checkpointSubmitButton-actual-button")
        if (btn2fa):
            btn2fa.click()
            btn2faContinue = driver.find_element(By.CSS_SELECTOR,"#checkpointSubmitButton-actual-button")
            if (btn2faContinue):
                btn2faContinue.click()
                confirm2FA(driver)
    except Exception as e:
        print(e.msg)            
    # end login

fileIds = 'post_ids.csv'
def readData(fileName):
    f = open(fileName, 'r', encoding='utf-8')
    data = []
    for i, line in enumerate(f):
        try:
            line = repr(line)
            line = line[1:len(line) - 3]
            data.append(line)
        except:
            print("err")
    return data

def writeFileTxt(fileName, content):
    with open(fileName, 'a', encoding="utf-8") as f1:
        f1.write(content + '\n')

def getPostsGroup(driver, idGroup, numberId):
    # joinGroup(driver, idGroup)
    sleep(2)
    try:
        driver.get('https://mbasic.facebook.com/groups/' + str(idGroup))
        file_exists = os.path.exists(fileIds)
        if (not file_exists):
            writeFileTxt(fileIds, '')

        sumLinks = readData(fileIds)
        while (len(sumLinks) < numberId):
            likeBtn = driver.find_elements(By.XPATH,'//*[contains(@id, "like_")]')
            if len(likeBtn):
                for id in likeBtn:
                    idPost = id.get_attribute('id').replace("like_", "")
                    if (idPost not in sumLinks):
                        sumLinks.append(idPost)
                        writeFileTxt(fileIds, idPost)
                        print(idPost)
            nextBtn = driver.find_element(By.XPATH,'//a[contains(@href, "?bacr")]')
            if (nextBtn):
                sleep(6)
                nextBtn.click()
            else:
                print('Next btn does not exist !')
                break
    except Exception as e:
        print(e.msg)

def getPostsPage(driver, idGroup, numberId):
    sleep(2)
    try:
        driver.get('https://mbasic.facebook.com/profile.php?id='+ str(idGroup) + '&v=timeline')
        file_exists = os.path.exists(fileIds)
        if (not file_exists):
            writeFileTxt(fileIds, '')

        sumLinks = readData(fileIds)
        while (len(sumLinks) < numberId):
            likeBtn = driver.find_elements(By.XPATH,'//*[contains(@id, "like_")]')
            if len(likeBtn):
                for id in likeBtn:
                    idPost = id.get_attribute('id').replace("like_", "")
                    if (idPost not in sumLinks):
                        sumLinks.append(idPost)
                        writeFileTxt(fileIds, idPost)
                        print(idPost)
            nextBtn = driver.find_element(By.XPATH,'//a[contains(@href, "?cursor")]')
            if (nextBtn):
                sleep(6)
                nextBtn.click()
            else:
                print('Next btn does not exist !')
                break
    except Exception as e:
        print(e.msg)

def clonePostContent(driver, postId = "1902017913316274"):
    try:
        driver.get("https://m.facebook.com/" + str(postId))
        sleep(1)
        parrentImage = driver.find_elements(By.XPATH,"//div[@data-gt='{\"tn\":\"E\"}']")
        if (len(parrentImage) == 0):
            parrentImage = driver.find_elements(By.XPATH,"//div[@data-ft='{\"tn\":\"E\"}']")
        contentElement = driver.find_elements(By.XPATH,"//div[@data-gt='{\"tn\":\"*s\"}']")
        if (len(contentElement) == 0):
            contentElement = driver.find_elements(By.XPATH,"//div[@data-ft='{\"tn\":\"*s\"}']")

        #get Content if Have
        if (len(contentElement)):
            if(len(contentElement) > 1):
                content = contentElement[1].text
            else:
                content = contentElement[0].text
        #get Image if have
        linksArr = []
        if (len(parrentImage)>0):
            childsImage = parrentImage[0].find_elements(By.XPATH,".//*")
            for childLink in childsImage:
                linkImage = childLink.get_attribute('href')
                if (linkImage != None):
                    linksArr.append(linkImage.replace("m.facebook", "mbasic.facebook"))
        linkImgsArr = []
        if (len(linksArr)):
            linkImgsArr = []
            try:
                for link in linksArr:
                    driver.get(link)
                    linkImg = driver.find_element(By.XPATH,'//*[@id="MPhotoContent"]/div[1]/div[2]/span/div/span/a[1]')
                    linkImgsArr.append(linkImg.get_attribute('href'))
            except Exception:
                pass

        postData = {"post_id": postId, "content" : "", "images": []}

        if (len(linkImgsArr)):
            postData["images"] = linkImgsArr
        if (contentElement):
            postData["content"] = content
        print(postData)
        return postData
    except Exception as e:
        print(e.msg)
        return False


def writeFileTxtPost(fileName, content, idPost, pathImg="/img/"):
    pathImage = os.getcwd() + pathImg + str(idPost)
    with open(os.path.join(pathImage, fileName), 'a', encoding="utf-8") as f1:
        f1.write(content + os.linesep)

def writeJson(data,path):
    json_object = json.dumps(data, indent = 4,ensure_ascii=False)
    with open(path, 'w',encoding='utf-8') as json_file:
        json_file.write(json_object)

def readJson(path):
    with open(path, 'r',encoding="utf8") as f:
        return json.load(f)  

def download_file(url, localFileNameParam = "", idPost = "123456", pathName = "/data/"):
    try:
        # if not os.path.exists(pathName.replace('/', '')):
        #     os.mkdir(pathName.replace('/', ''))

        local_filename = url.split('/')[-1]
        if local_filename:
            local_filename = localFileNameParam

        # with requests.get(url, stream=True) as r:
        #     pathImage = os.getcwd() + pathName + str(idPost)

        #     if (os.path.exists(pathImage) == False):
        #         os.mkdir(pathImage)

        #     with open(os.path.join(pathImage, local_filename), 'wb') as f:
        #         shutil.copyfileobj(r.raw, f)

        response = requests.get(url, stream=True)
        if response.status_code == 202 or response.status_code == 200:
            extension = str('.'+ response.headers['content-type'].split("/")[1])
            fileNameEx = local_filename + extension

            total_size_in_bytes= int(response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(desc=f"=======> Download Image {fileNameEx}:", total=total_size_in_bytes, unit='iB', unit_scale=True, unit_divisor=block_size,leave=False)
            with open(f"{pathName}/{idPost}/{fileNameEx}", 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()
 
    except Exception as e:
        print(e.msg)


def joinGroup(driver, idGoup):
    try:
        driver.get("https://mbasic.facebook.com/groups/" + idGoup)
        sleep(1)
        isJoined = driver.find_element(By.XPATH,'//a[contains(@href, "cancelgroup")]')
        if (isJoined):
            sleep(1)
            driver.find_element(By.CSS_SELECTOR,"#root > div.bj > form > input.bu.bv.bw").click()
            sleep(1)
            textea = driver.find_elements_by_tag_name("textarea")

            if (textea):
                for el in textea:
                    sleep(1)
                    el.send_keys("oki admin ")
            sleep(1)
            btnSubmit = driver.find_element(By.CSS_SELECTOR,"#group-membership-criteria-answer-form > div > div > input")

            if (btnSubmit):
                btnSubmit.click()
                sleep(1)
        else:
            print("joined")
    except Exception as e:
        print(e.msg)


def crawlPostData(driver, postIds, type = 'page'):
    folderPath = "data_crawl/"
    for id in postIds:
        dataCrawled = readData('post_crawl.csv')
        if id in dataCrawled:
            continue

        try:
            time.sleep(1)
            dataPost = clonePostContent(driver, id)
            dataImage = []
            if (dataPost != False):
                if (type == 'group'):
                    for img in dataPost["images"]:
                        driver.get(img)
                        dataImage.append(driver.current_url)
                else:
                    dataImage = dataPost["images"]

                postId = str(dataPost['post_id'])
                # postContent = str(dataPost['content'])

                if (os.path.exists(f'{folderPath}/{postId}') == False):
                    os.mkdir(f'{folderPath}/{postId}')
                stt = 0
                for img in dataImage:
                    stt += 1
                    download_file(img, str(stt), postId, folderPath)
                writeFileTxt('post_crawl.csv', str(id))
                # writeFileTxtPost('content.csv', postContent, postId, folderPath)
                writeJson(dataPost,f"{folderPath}/{postId}/content.json")
        except Exception as e:
            print(e)


driver = initDriverProfile(None)
isLogin = checkLiveClone(driver)  # Check live
print(isLogin)
userName = 'haivodoi.nha@gmail.com'
passWord = 'haivodoi@2022'
twoFa= 'CLDUGA4T53OSQHKNEJI7Q2GHRSFXPYFH'

if (isLogin == False or isLogin == None):
    loginBy2FA(driver, userName, passWord, twoFa)

getPostsGroup(driver, '1532601343427140', 10)
# getPostsPage(driver, '100055060129632', 10)

postIds = readData(fileIds)
crawlPostData(driver, postIds, 'group')
driver.close()
