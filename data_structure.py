
# 資料結構跟名稱統一在這邊規範
# basic 的命名方式
例子: 3_t1-1_1_c_l_f_2_0_(n)
例子: 3_     t1-         1_             1_                c_           l_            f_            2_              0_          (n)
公式: {map}_{road_type}-{road_id}_{is_traffic_light}_{actor_type}_{actor_action}_{my_action}_{interaction}_{violated_rule}_{scenario_num}
1. map 就是地圖，比如 3 == Town03
2. road_type 為道路結構，'i': '4-way intersection', 't': '3-way intersection'. 's': 'straight', 'r': 'roundabout'
    t後面會接123，其中 23 的差別在於車子進入點不同，1 的可以左轉右轉、2 的可以直走或右轉、 3 的可以值走或左轉
3. road_id: town1~town10 每個路口的id，以ego car的初始區域為根據
4. is_traffic_light: 場景中是否有交通號誌，straight/圓環一定沒有 (交通號誌==紅綠燈，stop sign 沒有標記，因為只有沒幾個地方有所以需要的話再去對照圖看路口 id 就好)
5. actor_type: 
    Interacted actors' type  :'c': 'car', 't': 'truck', 'b': 'bike', 'm': 'motor', 'p': 'pedestrian'
    但是 tag 中只會出現 pcbe, 因為 e 代表自己、m都標成b、t 都標成 c 。阿都有了 my_action 了為甚麼還需要 e 這個 actor type.....
6. actor_action: Interacted actors' action 
    Vehicle: 'f': 'forward', 'l': 'left_turn', 'r': 'right_turn', 'sl': 'slide_left','sr': 'slide_right', 'u': 'u-turn'
    Pedestrian: 'c': 'crossing crosswalks', 'j': 'jaywalking'    
    non-interactive/obstacle為 0
7. my_action: Ego car's action type
    同上面的 6-Vehicle
8. interaction (notion 葉面下面的 How to play the scenarios? 這個區塊有細節)
    '0': False,  '1':  True (interactive, ego要等別人)
9.violated_regulation: The kind of violated regulation
10. 最後的括號是指 如果有蒐集到重複名字的 會是_1 _2...等等



# 0. tags 資料結構
    # 注意  tag 中的 actor_type 只會出現 pcbe, 因為 e 代表自己、m都標成b、t 都標成 c
    # 出發跟結尾可能是同一個，比如直行車車的 S-> S 
tags = [
    {'object': 'b', 'start': 'Z4', 'end': 'Z2'}, 
    {'object': 'e', 'start': 'Z1', 'end': 'Z2'}
    ]


# 1. 搜尋輸入的資料結構
    # tags 的部分就照樣塞進來
    # 卡，town 跟 variant 還沒做
search_input = {
    "road_type": "crossroads", 
    "tags_usage_type": "just contain this tags",# 卡，這個如果要用 漢銘code 的話感覺可以不用，直接給他一個排序就好 包含剛好 -> 包含全部 -> 包含部分
    "town": "",
    "variant":"",
    "tags":[
        {"object":"P+", "start":"C1". "end":"C2"},
        {"object":"P", "start":"C4". "end":"C1"},
        {"object":"P", "start":"C3". "end":"C2"},
    ]
}

# 2. search history 資料結構
    # 1. 就是把很多個 1 包起來
    # 2. 道路類型 : 4way-intersection, 3way-1,3way-2,Straight,Roundabout
    # 3. tags使用方式包含三種:恰包含這些tags、包含全部但不限於這些 tags、包含 tags 中任意一種即可
    # 4. 假設有 N 比搜尋紀錄，可以生成N 個小標題(第幾筆、路口類型、tags使用方式)+ N 個表格(所有的 tags)
    # 5. Python enumerate built-in function is not part of Jinja2 template engine. 所以要用這編寫的做法: {{ loop.index0 }} {{ val }}
        # https://stackoverflow.com/questions/27035728/flask-cannot-import-enumerate-undefinederror-enumerate-is-undefined
        # 而不能用  {% for index, value in enumerate(search_history) %}

search_historys = [
    {
    "road_type": "crossroads", 
    "tags_usage_type": "just contain this tags",
    "town": "",
    "variant":"",
    "tags":[
        {"object":"P+", "start":"C1". "end":"C2"},
        {"object":"P", "start":"C4". "end":"C1"},
        {"object":"P", "start":"C3". "end":"C2"},
    ]
    },
    {
    "road_type": "crossroads", 
    "tags_usage_type": "just contain this tags",
    "town": "",
    "variant":"",
    "tags":[
        {"object":"P+", "start":"C1". "end":"C2"},
        {"object":"P", "start":"C4". "end":"C1"},
        {"object":"P", "start":"C3". "end":"C2"},
    ]
    },

]

# 使用者資訊 資料結構
user_info = {
    "name" = "",
    "account" = "",
    "passwd" = "", # 記得用 hash
    "confirm passwd" = "",
    "phone" = ,
    "email" = ""
}

# 影片相關資料，這個肯定是要再補的
    #  每個 variant 的 instance_segmentation裡面有很多個view，只是傑奇只有抓top過來
video_info = {
    "VID" = 1,

    "basic_labal" = "1_t1-1_1_m_f_r_1_rl",
    "town" = "1", # 就算右邊是數字也存成字串
    "road_type" = "t1",
    "road_id" = "1",
    "is_traffic_light" = "1",
    "actor_type" = "m",  # 存成簡寫就好
    "actor_action" = "f", 
    "my_action" = "r",
    "interaction" = "1",
    "violated_regulation" = "rl",
    "repeat_num" = "0",
    "basic_video_path"= "/static/videos/1_t1-1_1_m_f_r_1_rl/sample_x264.mp4", #注意後端就要接好，前端才可以直接拿來用

    "tags" = [
        {'object': 'b', 'start': 'Z4', 'end': 'Z2'}, 
        {'object': 'e', 'start': 'Z1', 'end': 'Z2'},
    ],
    
    "varient" = "WetNoon_low_",
    "variant_video_path"= "/static/videos/1_t1-1_1_m_f_r_1_rl/sample_x264.mp4", #注意後端就要接好，前端才可以直接拿來用
    "rgb_front_video_path":
    
    "bev_video_path" = "",
    
}

# search result, VID 跟 path
    # 就是 video_info 的串列
latest_search_results=[
    {
        "VID":1, # 進資料庫再說
        "basic_labal":"1_t1-1_1_m_f_r_1_rl",
        ...懶
        "varient":"WetNoon_low_",
        "variant_video_path":"/static/videos/1_t1-1_1_m_f_r_1_rl/sample_x264.mp4", #注意後端就要接好，前端才可以直接拿來用
        "tags":[
            {'object': 'b', 'start': 'Z4', 'end': 'Z2'}, 
            {'object': 'e', 'start': 'Z1', 'end': 'Z2'},
        ],
        "bev_video_path":""
    },
    {
        "VID":2,
        "basic_labal":"1_t1-1_1_m_f_r_1_rl",
        ...懶
        "varient":"WetNoon_low_",
        "variant_video_path":"/static/videos/1_t1-1_1_m_f_r_1_rl/sample_x264.mp4", #注意後端就要接好，前端才可以直接拿來用
        "tags":[
            {'object': 'b', 'start': 'Z4', 'end': 'Z2'}, 
            {'object': 'e', 'start': 'Z1', 'end': 'Z2'},
        ],
        "bev_video_path": ""
    },

]

# 推車裡的東西跟搜尋結果一模一樣
cart = [
    {
        "VID":1,
        "basic_labal":"1_t1-1_1_m_f_r_1_rl",
        ...
        "varient":"WetNoon_low_",
        "variant_video_path":"/static/videos/1_t1-1_1_m_f_r_1_rl/sample_x264.mp4", #注意後端就要接好，前端才可以直接拿來用
        "tags":[
            {'object': 'b', 'start': 'Z4', 'end': 'Z2'}, 
            {'object': 'e', 'start': 'Z1', 'end': 'Z2'},
        ],
        "bev_video_path":""
    },
    {
        "VID":2,
        "basic_labal":"1_t1-1_1_m_f_r_1_rl",
        ...
        "varient":"WetNoon_low_",
        "variant_video_path":"/static/videos/1_t1-1_1_m_f_r_1_rl/sample_x264.mp4", #注意後端就要接好，前端才可以直接拿來用
        "tags":[
            {'object': 'b', 'start': 'Z4', 'end': 'Z2'}, 
            {'object': 'e', 'start': 'Z1', 'end': 'Z2'},
        ],
        "bev_video_path": ""
    },

]
