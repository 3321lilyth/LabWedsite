
/* search page*/
$(function () {
    //提交 tag 做 ajax 即時畫面更新
    let current_tags = [];
    let moving_object = "";
    let road_type="i";
    let town=0; //卡，還沒弄
    let variant = ""; //卡，還沒空
    let current_tag = document.getElementById("current_tag");
    
    
    function start_end_for_pedestrian(){
        let el = document.getElementById("start_ul");
        if (road_type == 'i'){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#start').val('C1'); $('#start').html('C1');">C1</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('C2'); $('#start').html('C2');">C2</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('C3'); $('#start').html('C3');">C3</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('C4'); $('#start').html('C4');">C4</a></li>
            `
        }else if (road_type == 't1'){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#start').val('C1'); $('#start').html('C1');">C1</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('C4'); $('#start').html('C4');">C4</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('CF'); $('#start').html('CF');">CF</a></li>
            `
        }else if (road_type == 't2'|| road_type == 't3'){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#start').val('C3'); $('#start').html('C3');">C3</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('C4'); $('#start').html('C4');">C4</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('CR'); $('#start').html('CR');">CR</a></li>
            `
        }else if (road_type == 's' ){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#start').val('JL'); $('#start').html('JL');">JL</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('JR'); $('#start').html('JR');">JR</a></li>
            `
        }else if (road_type == 'r'){
            el.html('none')
        }

        let el2 = document.getElementById("end_ul");
        if (road_type == 'i'){
            el2.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#end').val('C1'); $('#end').html('C1');">C1</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('C2'); $('#end').html('C2');">C2</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('C3'); $('#end').html('C3');">C3</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('C4'); $('#end').html('C4');">C4</a></li>
            `
        }else if (road_type == 't1'){
            el2.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#end').val('C1'); $('#end').html('C1');">C1</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('C4'); $('#end').html('C4');">C4</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('CF'); $('#end').html('CF');">CF</a></li>
            `
        }else if (road_type == 't2'|| road_type == 't3'){
            el2.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#end').val('C3'); $('#end').html('C3');">C3</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('C4'); $('#end').html('C4');">C4</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('CR'); $('#end').html('CR');">CR</a></li>
            `
        }else if (road_type == 's'){
            el2.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#end').val('JL'); $('#end').html('JL');">JL</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('JR'); $('#end').html('JR');">JR</a></li>
            `
        }else if (road_type == 'r'){
            el2.html('none')
        }
    }
    function start_for_ego(){
        let el = document.getElementById("start_ul");

        if (road_type == 'i' || road_type == 't1' ){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#start').val('Z1'); $('#start').html('Z1');">Z1</a></li>
            `
        }else if (road_type == 't2'){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#start').val('Z3'); $('#start').html('Z3');">Z3</a></li>
            `
        }else if (road_type == 't3'){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#start').val('Z1'); $('#start').html('Z1');">Z1</a></li>
            `
        }else if (road_type == 's' ){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#start').val('S'); $('#start').html('S');">S</a></li>
            `
        }else if (road_type == 'r'){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#start').val('RL'); $('#start').html('RL');">RL</a></li>
            <li><a class="dropdown-item" href="#"  onclick="$('#start').val('RI'); $('#start').html('RI');">RI</a></li>
            `
        }
    }
    function start_for_other_cars(){
        let el = document.getElementById("start_ul");
        if (road_type == 'i'){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#start').val('Z1'); $('#start').html('Z1');">Z1</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('Z2'); $('#start').html('Z2');">Z2</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('Z3'); $('#start').html('Z3');">Z3</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('Z4'); $('#start').html('Z4');">Z4</a></li>
            `
        }else if (road_type == 't1'){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#start').val('Z1'); $('#start').html('Z1');">Z1</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('Z2'); $('#start').html('Z2');">Z2</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('Z4'); $('#start').html('Z4');">Z4</a></li>
            `
        }else if (road_type == 't2'|| road_type == 't3'){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#start').val('Z1'); $('#start').html('Z1');">Z1</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('Z3'); $('#start').html('Z3');">Z3</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('Z4'); $('#start').html('Z4');">Z4</a></li>
            `
        }else if (road_type == 's' ){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#start').val('SL'); $('#start').html('SL');">SL</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('S'); $('#start').html('S');">S</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#start').val('SR'); $('#start').html('SR');">SR</a></li>
            `
        }else if (road_type == 'r'){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#start').val('RL'); $('#start').html('RL');">RL</a></li>
            <li><a class="dropdown-item" href="#"  onclick="$('#start').val('RI'); $('#start').html('RI');">RI</a></li>
            `
        }
    }
    function end_for_all_cars(){
        let el = document.getElementById("end_ul");
        if (road_type == 'i'){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#end').val('Z1'); $('#end').html('Z1');">Z1</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('Z2'); $('#end').html('Z2');">Z2</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('Z3'); $('#end').html('Z3');">Z3</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('Z4'); $('#end').html('Z4');">Z4</a></li>
            `
        }else if (road_type == 't1'){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#end').val('Z1'); $('#end').html('Z1');">Z1</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('Z2'); $('#end').html('Z2');">Z2</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('Z4'); $('#end').html('Z4');">Z4</a></li>
            `
        }else if (road_type == 't2'|| road_type == 't3'){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#end').val('Z1'); $('#end').html('Z1');">Z1</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('Z3'); $('#end').html('Z3');">Z3</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('Z4'); $('#end').html('Z4');">Z4</a></li>
            `
        }else if (road_type == 's' ){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#end').val('SL'); $('#end').html('SL');">SL</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('S'); $('#end').html('S');">S</a></li>
            <li><a class="dropdown-item " href="#"  onclick="$('#end').val('SR'); $('#end').html('SR');">SR</a></li>
            `
        }else if (road_type == 'r'){
            el.innerHTML = `
            <li><a class="dropdown-item active" href="#"  onclick="$('#end').val('RL'); $('#end').html('RL');">RL</a></li>
            <li><a class="dropdown-item" href="#"  onclick="$('#end').val('RI'); $('#end').html('RI');">RI</a></li>
            `
        }
    }
    function clear_page(){
        $('#object').html('Moving Object ')
        $('#start').html('Start Point ')
        $('#end').html('End Point ')
        $('#object').val('')
        $('#start').val('')
        $('#end').val('')
        current_tag.innerHTML = ``;
        current_tags = [];
    }
    
    $('#v-pills-4way-intersection-tab').click(function(){
        road_type = 'i'
        clear_page();
    })
    $('#v-pills-3way-intersection-1-tab').click(function(){
        road_type = 't1'
        clear_page();
    })
    $('#v-pills-3way-intersection-2-tab').click(function(){
        road_type = 't2'
        clear_page();
    })
    $('#v-pills-3way-intersection-3-tab').click(function(){
        road_type = 't3'
        clear_page();
    })
    $('#v-pills-3way-straight-tab').click(function(){
        road_type = 's'
        clear_page();
    })
    $('#v-pills-4way-straight-tab').click(function(){
        road_type = 's'
        clear_page();
    })
    $('#v-pills-5way-straight-tab').click(function(){
        road_type = 's'
        clear_page();
    })
    $('#v-pills-Roundabout-tab').click(function(){
        road_type = 'r'
        clear_page();
    })


    $('#Ego').click(function(){
        $('#object').val('e');
        $('#object').html('Ego Car');
        start_for_ego();
        end_for_all_cars();
        $('#start').val('');
        $('#start').html('Start Point ');
        $('#end').val('');
        $('#end').html('End Point ');
    });
    $('#Pedestrian').click(function(){
        $('#object').val('p');
        $('#object').html('Pedestrian');
        start_end_for_pedestrian(); 
        $('#start').val('');
        $('#start').html('Start Point ');
        $('#end').val('');
        $('#end').html('End Point ');
    });
    $('#Car').click(function(){
        $('#object').val('c');
        $('#object').html('Regular Car or Truck');
        start_for_other_cars();
        end_for_all_cars();
        $('#start').val('');
        $('#start').html('Start Point ');
        $('#end').val('');
        $('#end').html('End Point ');
    });
    $('#Bike').click(function(){
        $('#object').val('b');
        $('#object').html('Bike or Motor');
        start_for_other_cars();
        end_for_all_cars();
        $('#start').val('');
        $('#start').html('Start Point ');
        $('#end').val('');
        $('#end').html('End Point ');
    });


    $('#add_tag').click(function(){
        // 卡，我不知道這邊要不要檢查起點不等於終點，說不定他的違規就是在路上不動?
        object = $( '#object').val()
        start = $( '#start').val()
        end = $( '#end').val()
        
        if (object == '' || start == '' || end == ''){
            alert('please choose all fields')
        }else{
            current_tags.push({
                "object": object,
                "start":start,
                "end": end,
            });            
            current_tag.innerHTML = current_tag.innerHTML +`
                <tr>
                    <td>${object}</td>
                    <td>${start}</td>
                    <td>${end}</td>
                </tr>
                `;
            $('#object').html('Moving Object ')
            $('#start').html('Start Point ')
            $('#end').html('End Point ')
            $('#object').val('')
            $('#start').val('')
            $('#end').val('')
        
        }
    });


    $('#search_btn').click(function(){
        $('#search_btn_road_type').val(road_type)
        $('#search_btn_tags').val(JSON.stringify(current_tags))

        //卡，之後還要傳+清空 town 跟 variant

        current_tag.innerHTML = "";
        road_type = 'i';
        current_tags = [];

        // $.ajax({
        //     url: '/search',
        //     data: JSON.stringify({
        //         "road_type": road_type,
        //         "tags":current_tags,
        //         //卡，這邊之後要再加 variant 跟 town
        //     }),
        //     type: 'POST',
        //     success: function(data){
        //         console.log(road_type);
        //         console.log(current_tags);
        //         current_tag.innerHTML = "";
        //         road_type = '';
        //         current_tags = [];
        //     },
        //     error: function(xhr){
        //         alert(JSON.stringify(xhr));
        //     },
        //     // dataType : 'json', // 預期從server接收的資料型態
        //     dataType: "text/html; charset=utf-8",
        //     contentType : 'application/json; charset=utf-8', // 要送到server的資料型態
        // });
    });
});
