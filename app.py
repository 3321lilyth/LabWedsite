from crypt import methods
from flask import Flask, render_template, request, redirect, url_for
import os, json
import copy
app = Flask(__name__)

#####################################################################################
##                                   讀取本地資料或資料庫                            ##
#####################################################################################
# 卡，密碼記得用 hash
users = [
    {'name': 'lily', 'account': 'lily', 'passwd': 'lilyyy'},
    {'name': 'mic', 'account': 'mic', 'passwd': 'miccc'},
    {'name': 'vicky', 'account': 'vicky', 'passwd': 'vickyyy'}
]
account = "111"
nav = "searchPage"

# 反正影片不多我也先不用資料庫，那就直接每一個資料夾內爆搜ㄅ，搜到正確的 tags 之後就把對應的影片內容顯示出來
videos = [] 
videos_basic = os.listdir('static/videos') # 取得資料夾內所有檔名
VID = 0
for basic in videos_basic:
    variants = os.listdir('static/videos/'+basic+'/variant_scenario')
    for variant in variants:
        tags = []
        with open('static/videos/'+basic+'/variant_scenario/' + variant +'/retrieve_gt.txt', "r") as f:
            txt = f.read()
            if "None" not in txt: # 沒有錯有的裡面是空的^^ 我真是謝謝你                
                # 字串處理，存成字典的 list [{"物件": , "起點": , "終點": }, {}, ...]
                tag_list = txt.split() # 用空白切割每一個 tag
                for tag in tag_list:
                    dictionary = {
                        "object": tag.split(":")[0],
                        "start": tag.split(":")[1].split("-")[0], #每個 tag 中，冒號右邊的是路徑
                        "end": tag.split(":")[1].split("-")[1], #每個 tag 中，冒號右邊的是路徑
                    }
                    tags.append(dictionary)
        f.close
        basic_sp = basic.split('_')

        # 把圖檔串成影片，卡，之後再查有沒有辦法不要輸出 mp4 檔案，單純在網頁撥放就好
        # 卡，這邊其實不只 top view，只是目前只 copy 這些，之後再加
        basic_video_path = 'static/videos/'+basic
        if not os.path.isfile(basic_video_path+"/x264.mp4"):
            os.system("ffmpeg -i " + basic_video_path + "/sample.mp4 -an -vcodec libx264 -crf 23 "+ basic_video_path + "/x264.mp4")
               
        ins_top_img_dict = 'static/videos/'+basic+'/variant_scenario/' + variant +'/instance_segmentation/ins_top'
        if not os.path.isfile(ins_top_img_dict+"/out.mp4"):
            os.system("ffmpeg -framerate 20 -pattern_type glob -i '"+ins_top_img_dict+"/*.png' -c:v libx264 "+ins_top_img_dict+"/out.mp4")
        
        rgb_front_img_dist = 'static/videos/'+basic+'/variant_scenario/' + variant +'/rgb/front'
        if not os.path.isfile(rgb_front_img_dist+"/out.mp4"):
            os.system("ffmpeg -framerate 20 -pattern_type glob -i '"+rgb_front_img_dist+"/*.png' -c:v libx264 "+rgb_front_img_dist+"/out.mp4")
        
        bev_img_dist = 'static/videos/'+basic+'/variant_scenario/' + variant +'/bev'
        if not os.path.isfile(bev_img_dist+"/x264.mp4"):
            os.system("ffmpeg -i " + bev_img_dist + "/video.mp4 -an -vcodec libx264 -crf 23 "+ bev_img_dist + "/x264.mp4")


        video = {
            "VID": VID,
            "basic_labal": basic,
            "town": basic_sp[0],
            "road_type": basic_sp[1].split("-")[0],
            "road_id": basic_sp[1].split("-")[1],
            "is_traffic_light": basic_sp[2],
            "actor_type": basic_sp[3], 
            "actor_action": basic_sp[4], 
            "my_action": basic_sp[5],
            "interaction": basic_sp[6],
            "violated_regulation": basic_sp[7],
            "repeat_num": basic_sp[8] if len(basic_sp) == 9 else 0, 
            "basic_video_path": '/'+basic_video_path +'/x264.mp4',

            "tags": tags,

            "variant": variant,
            "variant_video_path": '/'+ins_top_img_dict+"/out.mp4",
            "rgb_front_video_path": '/'+rgb_front_img_dist+'/out.mp4',

            "bev_video_path": '/'+bev_img_dist+'/x264.mp4',
        }
        videos.append(video)
        VID = VID + 1


# 後端就要把 path 組出來值皆傳進去，我在前端才好用
latest_search_results = []
search_historys = []
cart = []
search_input = {
    "tags" : [],
    "road_type" : "",
    "variant" : "",
    "town" : "",
}







#####################################################################################
##                                   首頁 + 登入 + 註冊相關 + 解說葉面               ##
#####################################################################################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loginPage')
def showLoginPage():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        account = request.form.get('account')
        passwd = request.form.get('passwd')
        # 卡，這邊要連接資料庫驗證帳密，並且補一下登入失敗的彈出視窗
        for user in users:
            if user['account']== account and user['passwd'] == passwd:
                return redirect(url_for('showUserPage',account = account, nav='searchPage'))  # 登入成功的話跳轉到使用者首頁
        # 卡，這邊要弄一個彈出視窗
        return render_template('login.html')

    else:
        return render_template('login.html')

@app.route('/registerPage')
def showRegisterPage():
    return render_template('register.html')

@app.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        # 這邊要連接資料庫做 insert user，還要確認各個 input 是否有誤(用 AJAX 也行)
        name = request.form.get('name')
        account = request.form.get('account')
        passwd = request.form.get('passwd')
        passwd_confirm = request.form.get('passwd_confirm')
        phone = request.form.get('phone')
        email = request.form.get('email')
        if passwd != passwd_confirm:
            # 彈出視窗s提醒
            return
        # 還有很多其他的判斷看你資料庫的程式碼ㄅ
        return redirect(url_for('loginPage'))  # 註冊成功的話跳轉到登入葉面
    else:
        return render_template('register.html')

@app.route('/guidePage', methods = ['GET'])
def showGuidePage():
	return render_template('guide_page.html')
    #url_for 的回傳值是找到function名稱為'參數'的把對方所指向的路由顯示出來



#####################################################################################
##                                   使用者各個頁                                ##
#####################################################################################
@app.route('/showUserPage/<account>/<nav>')  # 卡，這邊最後要加上  methods=['POST'] 才可以避免直接打網址登入別人網頁，我現在是為了 debug 方便
def showUserPage( account, nav):
    # 卡，每次渲染都重新挖一次 search history 和 latest result 和 cart
    search_historys = [
        {"road_type":"crossroads", "tags_usage_type":"just contain this tags", "tags":[
            {"object":"P+", "start":"C1", "end":"C2"},
            {"object":"P", "start":"C4", "end":"C1"},
            {"object":"P", "start":"C3", "end":"C2"}
        ]},
        {"road_type":"straight", "tags_usage_type":"just contain this tags", "tags":[
            {"object":"P+", "start":"C1", "end":"C2"},
            {"object":"P", "start":"C4", "end":"C1"},
            {"object":"P", "start":"C3", "end":"C2"}
        ]},
        {"road_type":"straight", "tags_usage_type":"just contain this tags", "tags":[
            {"object":"P+", "start":"C1", "end":"C2"},
            {"object":"P", "start":"C4", "end":"C1"},
            {"object":"P", "start":"C3", "end":"C2"}
        ]},
        {"road_type":"straight", "tags_usage_type":"just contain this tags", "tags":[
            {"object":"P+", "start":"C1", "end":"C2"},
            {"object":"P", "start":"C4", "end":"C1"},
            {"object":"P", "start":"C3", "end":"C2"}
        ]},
        {"road_type":"straight", "tags_usage_type":"just contain this tags", "tags":[
            {"object":"P+", "start":"C1", "end":"C2"},
            {"object":"P", "start":"C4", "end":"C1"},
            {"object":"P", "start":"C3", "end":"C2"}
        ]},

    ]
    # latest_search_results = [
    #     {
    #         "VID":1,
    #         "basic_labal":"1_t1-1_1_m_f_r_1_rl",
    #         "varient":"WetNoon_low_",
    #         "variant_video_path":"/static/videos/1_t1-1_1_m_f_r_1_rl/sample_x264.mp4", #注意後端就要接好，前端才可以直接拿來用
    #         "tags":[
    #             {'object': 'b', 'start': 'Z4', 'end': 'Z2'}, 
    #             {'object': 'e', 'start': 'Z1', 'end': 'Z2'},
    #         ],
    #         "bev_video_path":""
    #     },
    #     {
    #         "VID":2,
    #         "basic_labal":"1_t1-1_1_m_f_r_1_rl",
    #         "varient":"WetNoon_low_",
    #         "variant_video_path":"/static/videos/1_t1-1_1_m_f_r_1_rl/sample_x264.mp4", #注意後端就要接好，前端才可以直接拿來用
    #         "tags":[
    #             {'object': 'b', 'start': 'Z4', 'end': 'Z2'}, 
    #             {'object': 'e', 'start': 'Z1', 'end': 'Z2'},
    #         ],
    #         "bev_video_path": ""
    #     },
    #     {
    #         "VID":2,
    #         "basic_labal":"1_t1-1_1_m_f_r_1_rl",
    #         "varient":"WetNoon_low_",
    #         "variant_video_path":"/static/videos/1_t1-1_1_m_f_r_1_rl/sample_x264.mp4", #注意後端就要接好，前端才可以直接拿來用
    #         "tags":[
    #             {'object': 'b', 'start': 'Z4', 'end': 'Z2'}, 
    #             {'object': 'e', 'start': 'Z1', 'end': 'Z2'},
    #         ],
    #         "bev_video_path": ""
    #     },
    #     {
    #         "VID":2,
    #         "basic_labal":"1_t1-1_1_m_f_r_1_rl",
    #         "varient":"WetNoon_low_",
    #         "variant_video_path":"/static/videos/1_t1-1_1_m_f_r_1_rl/sample_x264.mp4", #注意後端就要接好，前端才可以直接拿來用
    #         "tags":[
    #             {'object': 'b', 'start': 'Z4', 'end': 'Z2'}, 
    #             {'object': 'e', 'start': 'Z1', 'end': 'Z2'},
    #         ],
    #         "bev_video_path": ""
    #     },
    #     {
    #         "VID":2,
    #         "basic_labal":"1_t1-1_1_m_f_r_1_rl",
    #         "varient":"WetNoon_low_",
    #         "variant_video_path":"/static/videos/1_t1-1_1_m_f_r_1_rl/sample_x264.mp4", #注意後端就要接好，前端才可以直接拿來用
    #         "tags":[
    #             {'object': 'b', 'start': 'Z4', 'end': 'Z2'}, 
    #             {'object': 'e', 'start': 'Z1', 'end': 'Z2'},
    #         ],
    #         "bev_video_path": ""
    #     },
    #     {
    #         "VID":2,
    #         "basic_labal":"1_t1-1_1_m_f_r_1_rl",
    #         "varient":"WetNoon_low_",
    #         "variant_video_path":"/static/videos/1_t1-1_1_m_f_r_1_rl/sample_x264.mp4", #注意後端就要接好，前端才可以直接拿來用
    #         "tags":[
    #             {'object': 'b', 'start': 'Z4', 'end': 'Z2'}, 
    #             {'object': 'e', 'start': 'Z1', 'end': 'Z2'},
    #         ],
    #         "bev_video_path": ""
    #     },
    #     {
    #         "VID":2,
    #         "basic_labal":"1_t1-1_1_m_f_r_1_rl",
    #         "varient":"WetNoon_low_",
    #         "variant_video_path":"/static/videos/1_t1-1_1_m_f_r_1_rl/sample_x264.mp4", #注意後端就要接好，前端才可以直接拿來用
    #         "tags":[
    #             {'object': 'b', 'start': 'Z4', 'end': 'Z2'}, 
    #             {'object': 'e', 'start': 'Z1', 'end': 'Z2'},
    #         ],
    #         "bev_video_path": ""
    #     },
    #     {
    #         "VID":2,
    #         "basic_labal":"1_t1-1_1_m_f_r_1_rl",
    #         "varient":"WetNoon_low_",
    #         "variant_video_path":"/static/videos/1_t1-1_1_m_f_r_1_rl/sample_x264.mp4", #注意後端就要接好，前端才可以直接拿來用
    #         "tags":[
    #             {'object': 'b', 'start': 'Z4', 'end': 'Z2'}, 
    #             {'object': 'e', 'start': 'Z1', 'end': 'Z2'},
    #         ],
    #         "bev_video_path": ""
    #     },

    # ]
    # latest_search_results = videos
    cart = []
    search_input = {} # 清空上次輸入的 tag
    # print (request.url_rule)
    # 這邊到時候要去資料庫(或本地)撈資料(latest_search_results + history + cart )，然後一樣將變數當成參數傳進去
    return render_template('userHomePage.html', account = account, nav = nav, users = users,  # 之後要改成單一 user 喔
        latest_search_results = latest_search_results, search_historys = search_historys, cart = cart)



@app.route('/search', methods=['POST'])
def search():
    # 這邊到時候要去資料庫(或本地)撈資料，然後一樣將變數當成參數傳進去 
    if request.method == "POST":
        # 紀錄一下我原本的寫法: 前端適用 ajax 丟 json 過來，所以我這邊用 json 接。但是我發線前端如果用 ajax 的話，就會要求後端要回傳東西給他
        # 而不能重新導向一個頁面網址，就算我前端有設定回傳的 dataType: "text/html; charset=utf-8", 也一樣。他只會把整個 html 當成 text 然後 alert 出來給你看 :(
        # data = request.get_json(force=True)
        # print(data)
        search_input = {}
        search_input['road_type'] = request.form.get('search_btn_road_type') # 這裡面要填標籤的 name
        search_input['tags'] = request.form.get('search_btn_tags') # 這裡面要填標籤的 name
        search_input['tags'] = json.loads(search_input['tags']) # string(json) to list
        # search_input['variant'] ="" # 卡，之後用
        # search_input['town'] =""# 卡，之後用
        search_historys.append(search_input) # 加進最後一筆搜尋紀錄，更新
        
        # 搜尋(卡，我先找完全 match road_type + tag 的，其他的搜尋根據之後再加。然後用漢銘code 排序的也是之後再加)
        latest_search_results.clear()
        print(search_input['tags'])
        for video in videos:
            print(video['road_type'], search_input['road_type'])
            
            flag = 1
            for target_tag in search_input['tags']:
                if video['tags'].count(target_tag) == 0 : # 代表這支影片沒有我要找的 tag
                    flag = 0 
                if video['road_type']  != search_input['road_type']:
                    flag = 0
            if flag == 1:
                latest_search_results.append(copy.deepcopy(video))

        if latest_search_results != []:
            # show detail 裡面的資訊在這邊改成使用這看得懂的
            for latest_search_result in latest_search_results:
                if latest_search_result['road_type'] == "i": latest_search_result['road_type'] = "4-way intersection"
                elif latest_search_result['road_type'] == "t1" or latest_search_result['road_type'] == "t2" or latest_search_result['road_type'] == "t3" : latest_search_result['road_type'] = "3-way intersection"
                elif latest_search_result['road_type'] == "s": latest_search_result['road_type'] = "straight"
                elif latest_search_result['road_type'] == "r": latest_search_result['road_type'] = "roundabout"

                if latest_search_result['actor_type'] == "p": latest_search_result['actor_type'] = "pedestrian"
                elif latest_search_result['actor_type'] == "c": latest_search_result['actor_type'] = "normal car"
                elif latest_search_result['actor_type'] == "t": latest_search_result['actor_type'] = "truck"
                elif latest_search_result['actor_type'] == "b": latest_search_result['actor_type'] = "bike"
                elif latest_search_result['actor_type'] == "m": latest_search_result['actor_type'] = "motor"
                elif latest_search_result['actor_type'] == "e": latest_search_result['actor_type'] = "ego Car"

                if latest_search_result['actor_action'] == "f": latest_search_result['actor_action'] = "forward"
                elif latest_search_result['actor_action'] =="l": latest_search_result['actor_action'] = "left turn"
                elif latest_search_result['actor_action'] == "r": latest_search_result['actor_action'] = "right turn"
                elif latest_search_result['actor_action'] == "sl": latest_search_result['actor_action'] = "slide left"
                elif latest_search_result['actor_action'] == "sr": latest_search_result['actor_action'] = "slide right"
                elif latest_search_result['actor_action'] == "u": latest_search_result['actor_action'] = "u-turn"
                elif latest_search_result['actor_action'] == "c": latest_search_result['actor_action'] = "crosing crosswalks"
                elif latest_search_result['actor_action'] == "j": latest_search_result['actor_action'] = "jaywalking"
                if latest_search_result['actor_action'] == "f": latest_search_result['actor_action'] = "forward"
                
                if latest_search_result['my_action'] =="l": latest_search_result['my_action'] = "left turn"
                elif latest_search_result['my_action'] == "r": latest_search_result['my_action'] = "right turn"
                elif latest_search_result['my_action'] == "sl": latest_search_result['my_action'] = "slide left"
                elif latest_search_result['my_action'] == "sr": latest_search_result['my_action'] = "slide right"
                elif latest_search_result['my_action'] == "u": latest_search_result['my_action'] = "u-turn"
                elif latest_search_result['my_action'] == "f": latest_search_result['my_action'] = "forward"
            print(len(latest_search_results))
            print(len(videos))
        
        return redirect(url_for('showUserPage',account = account, nav='search_result'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
