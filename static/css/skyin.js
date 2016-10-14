function scroll( fn ) {  
    var beforeScrollTop = Math.abs(document.body.scrollTop),  
        fn = fn || function() {};  
    window.addEventListener("scroll", function() {  
        var afterScrollTop = Math.abs(document.body.scrollTop),  
            delta = afterScrollTop - beforeScrollTop;  
        if( delta === 0 ) return false;  
        fn( delta > 0 ? "down" : "up" );  
        beforeScrollTop = afterScrollTop;  
    }, false);  
}




$(document).ready(function() {
    $("#nav").click(function(){
        $(this).css("opacity","0.9");
    });
    $("#nav").hover(function(){
        $(this).css("opacity","0.9");
    },function(){
        $(this).css("opacity","0.25");
    });
    scroll(function(dire) {
        if( dire == "down" )
        {
            $("#nav").hide();
            $("#nav").css("opacity","0.25");
        }
        if( dire == "up" )
        {
            $("#nav").show();
        }
    }); 
    $("#navc").click(function(){
        $("#navs").toggle(200);
    });
    $("#navc").hover(function(){
        $("#navc").css("color","#222");
    },function(){
        $("#navc").css("color","#fff");
    });
    var hei = $(window).height();
    var wid = $(window).width();
    var canvas = document.getElementById("cvs");
    var colorr = ['#40E0D0','#B0C4DE','#00BFFF','#8470FF','#EEEE00','#FF8C00'];
    if(canvas.getContext){
        canvas.width = wid; 
        canvas.height = hei;
        lst = 0.8*hei*Math.random()+0.2*hei;
        rst = 0.8*hei*Math.random();
        var ctx = canvas.getContext("2d");
        ctx.lineWidth = 1; 
        lft=2*Math.random()
        rft=2*Math.random()
        for (var i=0;i<6;i++){
        ctx.beginPath();
        lst = lst - lft*0.2*hei*Math.random()-0.05*hei;
        rst = rst + rft*0.2*hei*Math.random()+0.05*hei;
        ctx.strokeStyle = colorr[Math.floor(6*Math.random())];
        ctx.moveTo(0, lst);
        ctx.lineTo(wid, rst);
        ctx.stroke();
        ctx.closePath();
        }
    };
    $("#cvs").click(function () {
        if(canvas.getContext){
            hei = $(window).height();
            wid = $(window).width();
            canvas.width = wid; 
            canvas.height = hei;
            lst = 0.8*hei*Math.random()+0.2*hei;
            rst = 0.8*hei*Math.random();
            var ctx = canvas.getContext("2d");
            ctx.lineWidth = 1; 
            lft=2*Math.random()
            rft=2*Math.random()
            for (var i=0;i<6;i++){
            ctx.beginPath();
            lst = lst - lft*0.2*hei*Math.random()-0.05*hei;
            rst = rst + rft*0.2*hei*Math.random()+0.05*hei;
            ctx.strokeStyle = colorr[Math.floor(6*Math.random())];
            ctx.moveTo(0, lst);
            ctx.lineTo(wid, rst);
            ctx.stroke();
            ctx.closePath();
            }
        }
    });
});


$(document).ready(function() {
    var souli='http://link.itiyun.com/fm/douban/iTiYue.mp3'
    var audio = document.getElementById("aud");
    var source = document.getElementById("sou");
    source.src=souli;
    audio.volume = 0.4;
    audio.load();
    $("#pp").click(function(){
        event.stopPropagation();
        if(audio.paused)
        {
            audio.play();
            document.getElementById("pp").innerHTML = "&#61517;";
            return;
        }
        audio.pause();
        document.getElementById("pp").innerHTML = "&#61515;";
    });
    $("#cm").click(function(){
        event.stopPropagation();
        source.src=souli;
        audio.load();
        audio.play();
        document.getElementById("pp").innerHTML = "&#61517;";
    });
    $("#vd").click(function(){
        event.stopPropagation();
        audio.volume -= 0.1;
    });
    $("#vu").click(function(){
        event.stopPropagation();
        audio.volume += 0.1;
    });
        var acti = 1;
    $("#musc").click(function(){
        if (acti == 1){
            $("#musc").animate({left:'0',marginLeft:'-10px'});
            $("#ply").fadeIn();
            acti = 0;
            return};
            $("#musc").animate({left:'50%',marginLeft:'-40px'});
            $("#ply").fadeOut();
            acti = 1;
    });
    var audt=$('#audi').offset().top;
    var audl=$('#audi').offset().left;
    $(window).scroll( function() {
        if($(window).scrollTop()>audt){
            $('#audi').css({'top':$(window).scrollTop()-audt+40});
        return;};
        $('#audi').css({'top':'0'});
    });
});




$(document).ready(function() {
    $("rep").click(function(){
        reid = $(this).attr("id");
        $("#comment").attr("placeholder","回复刚才的评论，刷新页面撤销");
        $("#reply").attr("value",reid);
    });
    $("#subm").click(function(){
        check=true;
    });
});

function confirm() {
    if(check==true)
    {
    return true;
    }
    return false;

};