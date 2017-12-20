$(document).ready(function() {
    document.getElementById("mctrl").innerHTML='<div id="audi"><div id="musc">&#61441;</div><audio id="aud" loop="" preload="metadata"><source id="sou" type="audio/mpeg"></audio><div id="mbtn"><div id="play" class="audc">&#61515;</div><div id="change" class="audc">&#61473;</div><div id="down" class="audc">&#61479;</div><div id="up" class="audc">&#61480;</div></div></div>';
    var solist=['https://mr1.doubanio.com/795979fbab374c99cefb867df17d45f0/0/fm/song/p2022252_128k.mp4','https://mr3.doubanio.com/71e80854b44452d0be3cc26eaab55d7d/0/fm/song/p741911_128k.mp3']
    var souli='//link.itiyun.com/fm/douban/iTiYue.mp3'
    var audio = document.getElementById("aud");
    var source = document.getElementById("sou");
    source.src=solist[parseInt(2*Math.random())];
    audio.volume = 0.4;
    audio.load();
    $("#play").click(function(){
        event.stopPropagation();
        if(audio.paused)
        {
            audio.play();
            document.getElementById("play").innerHTML = "&#61517;";
            return;
        }
        audio.pause();
        document.getElementById("play").innerHTML = "&#61515;";
    });
    $("#change").click(function(){
        event.stopPropagation();
        source.src=solist[parseInt(2*Math.random())];;
        audio.load();
        audio.play();
        document.getElementById("play").innerHTML = "&#61517;";
    });
    $("#down").click(function(){
        event.stopPropagation();
        audio.volume -= 0.1;
    });
    $("#up").click(function(){
        event.stopPropagation();
        audio.volume += 0.1;
    });
    var acti = 1;
    $("#musc").click(function(){
        if (acti == 1){
            $("#musc").css({left:'0',marginLeft:'0'});
            $("#mbtn").fadeIn();
            acti = 0;
            return};
            $("#musc").css({left:'50%',marginLeft:'-1em'});
            $("#mbtn").fadeOut();
            acti = 1;
    });
    nbh=$('#mctrl').offset().top;
    $(window).scroll( function() {
        if($(window).scrollTop()>nbh){
            $('#mctrl').css({'position':'fixed','top':'10%','width':$("#holder").width()});
            $("#holder").height($('#mctrl').height());
        return;};
        $('#mctrl').css({'position':'relative','top':'0','width':'initial'});
        $("#holder").height(0);
    });
});