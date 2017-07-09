$(document).ready(function() {
    document.getElementById("mctrl").innerHTML='<div id="audi"><div id="musc">&#61441;</div><audio id="aud" loop="" preload="metadata"><source id="sou" type="audio/mpeg" src="http://link.itiyun.com/fm/douban/iTiYue.mp3"></audio><div id="mbtn"><div id="play" class="audc">&#61515;</div><div id="change" class="audc">&#61473;</div><div id="down" class="audc">&#61479;</div><div id="up" class="audc">&#61480;</div></div></div></div><div id="holder">';
    var souli='http://link.itiyun.com/fm/douban/iTiYue.mp3'
    var audio = document.getElementById("aud");
    var source = document.getElementById("sou");
    source.src=souli;
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
        source.src=souli;
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
        return;};
        $('#mctrl').css({'position':'relative','top':'0','width':'initial'});
    });
});