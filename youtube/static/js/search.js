var search_result = function(){
    t = $('#search_text').text;
    host = '192.168.2.1:8878';
    console.log('hellow');
    
    function div_click(href){
        $.ajax({
            url:"http://"+host+"/audioes",
            data:{
                url:'https://www.youtube.com'+href
            },
            })
            .done(function(resp){
                keys = Object.keys(resp);
                control = $('#audio-player')
                for (i=0; i<keys.length; i++){
                    source = $('<source>');
                    source.attr('src', resp[keys[i]]['url']);
                    source.attr('type', resp[keys[i]]['type']);
                    control.append(source);
                }
            })
            .fail(function(resp){
                alert('disconneted')
            });
    };

    function make_search_box(top_tag, title, href, image){
        result_wrap = $('<div class="result_wrap">');
        image_wrap = $('<div class="image_wrap">');
        text_wrap = $('<div class="text_wrap">');
        result_wrap.append(image_wrap);
        result_wrap.append(text_wrap);
        image_tag = $('<img class="search_images"/>').attr('src', image);
        image_wrap.append(image_tag);
        p_tag = $('<p class="title">')
        p_tag.text(title);
        p_tag.attr('onclick', div_click(href));
        text_wrap.append(p_tag)
        top_tag.append(result_wrap);
    };

    $.ajax({
        url:'http://'+host+'/search',
        data:{
            'search_bar':'crow song',
        }
    })
    .done(function(resp){
        result_wrap = $('#search_result_wrap');
        titles = resp['titles'];
        console.log(typeof(titles));
        images = resp['images'];
        hrefs = resp['hrefs'];
        for (i=0; i<titles.length; i++){
            top_tag = $('#search_result_wrap');
            make_search_box(top_tag, titles[i], hrefs[i], images[i]);
        }
        })
    .fail(function(resp){
        alert('server connet fail');
        });
    
};
