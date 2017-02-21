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




$(document).ready(function(){
    $("#imgc").click(function(){
        var re=/src="(.*?)"/ig;
        var data=document.getElementsByClassName('wangEditor-txt')[0].innerHTML;
        var pos=data.match(re);
        document.getElementById('imgbox').innerHTML='';
        console.log(pos);
        for(var aimg in pos){document.getElementById('imgbox').innerHTML+='<div class="ibox" style="display:inline-block;height:100px;width:160px;margin:10px;overflow:hidden"><img id="d" width="100%" height="100%" '+pos[aimg]+'/></div>';}
    });
    $("#imgd").click(function(){
        document.getElementById('imgbox').innerHTML='';
        $("#img0").val("");
    });
    $("#imgbox").on("click","img",function(){
        var addi = '<center><img src="'+$(this).attr("src")+'" /></center>';
        $("#img0").val(addi);
    });
    $("arti img").click(function(){
        $("#mask").fadeIn(200);
        var imgsrc = $(this).attr("src");
        document.getElementById("mask").innerHTML='<span style="height:100%;display:inline-block;vertical-align:middle"></span><a target="_blank" href="'+imgsrc+'"><img style="vertical-align:middle;max-width:90%;margin-top:-15px" onmousewheel="return mwimg(this)" title="点击查看原图" src="'+imgsrc+'"></a>';
    });
    $("#mask").click(function(){
        $("#mask").fadeOut(200);
    });
    $("#cd").click(function(){
        pid = $(this).attr("pid");
        $.post("/del/"+pid,
        {type:0,pid:pid},
        function(data,status){
          window.location.href='/';
        });
    });
    $("#codel").click(function(){
        pid = $(this).attr("pid");
        $.post("/del/"+pid,
        {type:1,pid:pid},
        function(data,status){
          location.reload();
        });
    });
    $("#ibd").click(function(){
        $("#bd").toggle(200);
    });
    $("button.sm.cd").click(function(){
        $("#commdel").toggle(200);
        $("#codel").attr("pid",$(this).attr("pid"));
    });
    $("#qd").click(function(){
        $("#bd").hide(200);
    });
    $("#coqui").click(function(){
        $("#commdel").hide(200);
    });
});


$(document).ready(function() {
    $("#nav").click(function(){
        $(this).css("opacity","0.9");
    });
    $("#nav").hover(function(){
        $(this).css("opacity","0.9");
    },function(){
        $(this).css("opacity","0.4");
    });
    scroll(function(dire) {
        if( dire == "down" )
        {
            $("#nav").hide();
            $("#nav").css("opacity","0.4");
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
        for (var i=0;i<5;i++){
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
            for (var i=0;i<5;i++){
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
    audt=$('#audi').offset().top;
    $(window).scroll( function() {
        if($(window).scrollTop()>audt){
            $('#muscrl').css({'position':'fixed'});
        return;};
        $('#muscrl').css({'position':'static'});
        audt=$('#audi').offset().top;
        if($(window).scrollTop()<20){$('#nav').css({'opacity':'1'});};
    });
});

window.onresize=function(){audt=$('#audi').offset().top;};


$(document).ready(function() {
    $("rep").click(function(){
        reid = $(this).attr("id");
        $("#comment").attr("placeholder","回复刚才的评论，刷新页面撤销");
        $("#reply").attr("value",reid);
    });
    $("#subm").click(function(){
    if(document.form.title.value=="")
    {
    alert("忘写标题啦!");
    return false;
    } 
    check=true;
    });
});

function confirm() {
    return check;

};

function siteTime(){
window.setTimeout("siteTime()", 1000);
var days = 3600000 * 24
var today = new Date()
var t1 = Date.UTC(2016,8,21,18,24,41)
var t2 = Date.UTC(today.getFullYear(),today.getMonth(),today.getDate(),today.getHours(),today.getMinutes(),today.getSeconds())
var diff = t2-t1
var diffDays = Math.floor((diff/days))
var diffHours = Math.floor((diff-(diffDays)*days)/3600000)
var diffMinutes = Math.floor((diff-(diffDays)*days-diffHours*3600000)/60000)
var diffSeconds = Math.floor((diff-(diffDays)*days-diffHours*3600000-diffMinutes*60000)/1000)
document.getElementById("bt").innerHTML="\u672c\u535a\u5ba2\u5df2\u4e0d\u7a33\u5b9a\u8fd0\u884c "+diffDays+" \u5929 "+diffHours+" \u65f6 "+diffMinutes+" \u5206 "+diffSeconds+" \u79d2"
}
siteTime()